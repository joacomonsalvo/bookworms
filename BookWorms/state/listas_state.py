import reflex as rx
from postgrest import APIError
from BookWorms.models.dbbroker import DBBroker
from BookWorms.state.auth_state import AuthState


class ListasState(rx.State):
    # Listas cargadas
    public_lists: list = []
    private_lists: list = []

    # Modal
    selected_list: dict = {}  # inicializado como dict vacío para evitar NoneType
    selected_list_type: str = "publica"
    is_modal_open: bool = False

    # Libros de la lista seleccionada
    selected_list_books: list = []
    new_book_id: str = ""

    @rx.var
    def public_count(self) -> int:
        return len(self.public_lists)

    @rx.var
    def private_count(self) -> int:
        return len(self.private_lists)

    def load_all(self) -> None:
        """Carga todas las listas públicas y las listas privadas del usuario actual."""
        broker = DBBroker().supabase
        try:
            # publicas
            resp_pub = broker.from_("listas_publicas").select("*").execute()
            self.public_lists = resp_pub.data or []

            # privadas
            db = DBBroker()
            username = db.get_last_current_user()
            user_id = db.get_user_by_username(str(username))[0]['id']
            es_admin = db.get_user_es_admin_by_id(user_id)

            resp_priv = broker.from_("listas_privadas").select("*").eq("user_id", user_id).execute()
            self.private_lists = resp_priv.data or []

        except APIError as e:
            print("Error al cargar listas:", e)

    def open_modal(self, lista: dict, tipo: str) -> None:
        """Abre modal y carga libros de la lista, indicando si es 'publica' o 'privada'."""
        # Establecer lista y tipo
        self.selected_list = lista
        self.selected_list_type = tipo
        self.is_modal_open = True
        # Cargar libros correspondientes
        self.load_list_books(lista.get("id"), tipo)

    def close_modal(self) -> None:
        """Cierra modal y limpia estado."""
        self.selected_list = {}
        self.is_modal_open = False
        self.selected_list_books = []
        self.new_book_id = ""

    def load_list_books(self, lista_id: int, tipo: str) -> None:
        """Carga los libros de la lista desde tabla intermedia."""
        broker = DBBroker().supabase
        table = "lista_publica_libros" if tipo == "publica" else "lista_privada_libros"
        fk = "lista_publica_id" if tipo == "publica" else "lista_privada_id"
        try:
            resp = (
                broker.from_(table)
                .select("libro:libros(*)")
                .eq(fk, lista_id)
                .execute()
            )
            self.selected_list_books = [item["libro"] for item in resp.data] if resp.data else []
        except APIError as e:
            print("Error al cargar libros:", e)

    def set_new_book_id(self, value: str) -> None:
        """Actualiza el ID ingresado para agregar libro."""
        self.new_book_id = value

    def add_book_to_list(self) -> None:
        """Agrega el libro dado por ID a la lista activa."""
        if not self.selected_list:
            return
        broker = DBBroker().supabase
        lista_id = self.selected_list.get("id")
        tipo = self.selected_list_type
        table = "lista_publica_libros" if tipo == "publica" else "lista_privada_libros"
        fk = "lista_publica_id" if tipo == "publica" else "lista_privada_id"
        try:
            broker.from_(table).insert({fk: lista_id, "libro_id": int(self.new_book_id)}).execute()
            self.load_list_books(lista_id, tipo)
            self.new_book_id = ""
        except (APIError, ValueError) as e:
            print("Error al agregar libro:", e)

    def remove_book_from_list(self, libro_id: int) -> None:
        """Elimina un libro de la lista activa por su ID."""
        if not self.selected_list:
            return
        broker = DBBroker().supabase
        lista_id = self.selected_list.get("id")
        tipo = self.selected_list_type
        table = "lista_publica_libros" if tipo == "publica" else "lista_privada_libros"
        fk = "lista_publica_id" if tipo == "publica" else "lista_privada_id"
        try:
            (
                broker.from_(table)
                .delete()
                .eq(fk, lista_id)
                .eq("libro_id", libro_id)
                .execute()
            )
            self.load_list_books(lista_id, tipo)
        except APIError as e:
            print("Error al eliminar libro:", e)

    def delete_list(self, user_id: int) -> None:
        """Elimina la lista seleccionada y recarga las listas."""
        if not self.selected_list:
            return
        broker = DBBroker().supabase
        lista_id = self.selected_list.get("id")
        tipo = self.selected_list_type
        table = "listas_publicas" if tipo == "publica" else "listas_privadas"
        try:
            broker.from_(table).delete().eq("id", lista_id).execute()
            self.close_modal()
            self.load_all()
        except APIError as e:
            print("Error al eliminar lista:", e)

    def add_book_by_id(self, libro_id: int) -> None:
        """Agrega a la lista activa el libro cuyo ID viene por parámetro."""
        if not self.selected_list:
            return
        broker = DBBroker().supabase
        lista_id = self.selected_list.get("id")
        tipo = self.selected_list_type
        table = "lista_publica_libros" if tipo == "publica" else "lista_privada_libros"
        fk = "lista_publica_id" if tipo == "publica" else "lista_privada_id"
        try:
            broker.from_(table).insert({fk: lista_id, "libro_id": libro_id}).execute()
            self.load_list_books(lista_id, tipo)
        except APIError as e:
            print("Error al agregar libro por búsqueda:", e)

    # Aca va la seccion de crear listas
    new_list_modal_open: bool = False
    new_list_title: str = ""
    new_list_type: str = "publica"

    def open_new_list_modal(self):
        self.new_list_modal_open = True

    def close_new_list_modal(self):
        self.new_list_modal_open = False
        self.new_list_title = ""
        self.new_list_type = "publica"

    def create_list(self) -> None:
        """
        Crea una nueva lista (pública o privada) asociada al usuario actual,
        cierra el modal y recarga las listas.
        """
        if not self.new_list_title:
            return

        broker = DBBroker().supabase
        db = DBBroker()
        username = db.get_last_current_user()
        user_id = db.get_user_by_username(str(username))[0]['id']

        is_public = self.new_list_type.lower() == "publica"
        table = "listas_publicas" if is_public else "listas_privadas"

        # Solo agregamos user_id cuando es privada
        data = {"titulo": self.new_list_title}
        if not is_public:
            data["user_id"] = user_id

        try:
            broker.from_(table).insert(data).execute()
            self.close_new_list_modal()
            self.load_all()
        except APIError as e:
            print("Error al crear lista:", e)
