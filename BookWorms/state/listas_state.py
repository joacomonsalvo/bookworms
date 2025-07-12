'''from typing import List, Dict, Optional
import reflex as rx
from BookWorms.models.dbbroker import DBBroker
from BookWorms.state.auth_state import AuthState


class ListasState(rx.State):
    # Modal and storage fields
    selected_list: Optional[Dict] = None
    is_modal_open: bool = False

    # Lists
    public_lists: List[Dict] = []
    private_lists: List[Dict] = []
    # Estado de listas
    public_lists: List[Dict] = []
    private_lists: List[Dict] = []
    # Modal
    selected_list: Optional[Dict] = None
    is_modal_open: bool = False

    @rx.event
    def load_all(self):
        """
        Carga listas públicas y privadas.
        Utiliza el user_id reactivo dentro del evento.
        """
        db = DBBroker()
        # Públicas
        res_pub = (
            db.supabase
            .table("listas_publicas")
            .select("id, titulo")
            .order("created_at", desc=True)
            .execute()
        )
        self.public_lists = res_pub.data or []
        # Privadas (filtro en SQL con Var desempaquetada)
        #user_id = AuthState.get_current_user_id(AuthState)
        res_priv = (
            db.supabase
            .table("listas_privadas")
            .select("id, titulo")
            #.eq("user_id", user_id)
            .order("created_at", desc=True)
            .execute()
        )
        self.private_lists = res_priv.data or []

    @rx.event
    def open_modal(self, lista: Dict):
        """
        Abre el modal con la lista seleccionada.
        """
        self.selected_list = lista
        self.is_modal_open = True

    @rx.event
    def close_modal(self):
        """
        Cierra el modal y limpia la selección.
        """
        self.is_modal_open = False
        self.selected_list = None

    @rx.event
    def delete_list(self):
        """
        Elimina la lista seleccionada de Supabase.
        Luego recarga las listas y cierra el modal.
        """
        if not self.selected_list:
            return
        db = DBBroker()
        db.supabase.table("listas_" + self.selected_list.get("type", "privadas")) \
            .delete() \
            .eq("id", self.selected_list["id"]) \
            .execute()
        # Refrescar
        self.load_all()
        self.close_modal()'''

#-----------------------------------------------------------------------------------------------

import reflex as rx
from postgrest import APIError
from BookWorms.models.dbbroker import DBBroker

class ListasState(rx.State):
    # Listas cargadas
    public_lists: list = []
    private_lists: list = []

    # Modal
    selected_list: dict = {}
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
        """Carga todas las listas públicas y privadas."""
        broker = DBBroker().supabase
        try:
            resp_pub = broker.from_("listas_publicas").select("*").execute()
            self.public_lists = resp_pub.data or []
            resp_priv = broker.from_("listas_privadas").select("*").execute()
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
        self.selected_list = None
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

    def delete_list(self) -> None:
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
