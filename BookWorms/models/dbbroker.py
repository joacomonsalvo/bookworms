import os
from dotenv import load_dotenv
from supabase import create_client
from BookWorms.utils.security import hash_password


class DBBroker:
    def __init__(self):
        dotenv_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), ".env")
        load_dotenv(dotenv_path)

        self.supabase = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_KEY"))

    def create_user(self, email: str, username: str, password: str):
        password_hash = hash_password(password)

        result = self.supabase.table("usuarios").insert({
            "email": email,
            "user": username,
            "passw": password_hash,
            "amigos": [],
            "es_admin": False
        }).execute()

        return result.data[0]

    def get_user_by_username(self, username: str):
        result = self.supabase.table("usuarios").select("*").eq("user", username).execute()

        return result.data

    def get_user_by_id(self, user_id: int):
        result = self.supabase.table("usuarios").select("*").eq("id", user_id).execute()

        return result.data[0] if result.data else None

    def buscar_libros(self, texto: str):
        # Armar patrón ILIKE
        pattern = f"%{texto}%"
        # print("🔍 dbbroker.buscar_libros – patrón:", pattern)

        result = (
            self.supabase
            .table("libros")
            .select("*")
            .ilike("titulo", pattern)
            .execute()
        )
        # print("🔎 dbbroker.buscar_libros – resultado:", result.data)
        return result.data or []

    def buscar_usuarios(self, username: str):
        pattern = f"%{username.lower()}%"
        # print("🔍 Buscando usuarios con patrón:", pattern)
        result = self.supabase.table("usuarios") \
            .select("*") \
            .ilike("user", pattern) \
            .execute()
        # print("🔎 Resultado raw de Supabase:", result.data)
        return result.data or []

    def agregar_amigo(self, user_id: int, amigo_id: int):
        result = self.supabase.table("usuarios").select("amigos").eq("id", user_id).single().execute()
        amigos = result.data["amigos"]

        amigos_int = list(map(int, amigos)) if amigos else []

        if amigo_id not in amigos_int:
            amigos_int.append(amigo_id)

        amigos_str = list(map(str, amigos_int))

        self.supabase.table("usuarios").update({
            "amigos": amigos_str}).eq("id", user_id).execute()

    def eliminar_amigo(self, user_id: int, amigo_id: int):
        result = self.supabase.table("usuarios").select("amigos").eq("id", user_id).single().execute()
        amigos = result.data["amigos"]

        amigos_int = list(map(int, amigos)) if amigos else []

        if amigo_id in amigos_int:
            amigos_int.remove(amigo_id)

        amigos_str = list(map(str, amigos_int))

        self.supabase.table("usuarios").update({
            "amigos": amigos_str}).eq("id", user_id).execute()

    def get_amigos_from_user_id(self, user_id: str) -> list:
        """"
        Dado un ID de usuario, devuelve los nombres de usuario de sus amigos.
        """
        result = self.supabase.table("usuarios").select("amigos").eq("id", user_id).single().execute()
        amigos = result.data["amigos"]

        amigos_int = list(map(int, amigos)) if amigos else []
        lista_amigos = []

        for i in amigos_int:
            amigo = self.get_user_by_id(i)["user"]
            lista_amigos.append(amigo)

        return lista_amigos

    def insert_current_user(self, current_user: str):
        result = self.supabase.table("current_user").insert({
            "current_user": current_user
        }).execute()

        return result.data

    def get_last_current_user(self):
        result = self.supabase.table("current_user") \
            .select("current_user") \
            .order("id", desc=True) \
            .limit(1) \
            .execute()

        return result.data[0]["current_user"] if result.data else None

    def alta_libro(self, titulo, isbn, autor, editorial, sinopsis):
        self.supabase.table("libros").insert({
            "titulo": titulo,
            "isbn": int(isbn),
            "autor": autor,
            "editorial": editorial,
            "sinopsis": sinopsis
        }).execute()

    def baja_libro(self, isbn):
        self.supabase.table("libros").delete().eq("isbn", int(isbn)).execute()

    def es_admin(self, username):
        result = self.supabase.table("usuarios").select("*").eq("user", username).execute()
        result = result.data[0]["es_admin"]

        if result:
            return True
        else:
            return False

    def handle_like(self, post_id):
        last_username = self.supabase.table("current_user") \
            .select("current_user") \
            .order("id", desc=True) \
            .limit(1) \
            .execute().data[0]["current_user"]
        user_id = self.supabase.table("usuarios").select("*").eq("user", last_username).execute().data[0]['id']

        likes = self.supabase.table("publicaciones").select("*").eq("id", post_id).single().execute().data["likes"]
        likes_int = list(map(int, likes)) if likes else []

        if user_id in likes_int:
            likes_int.remove(user_id)
        else:
            likes_int.append(user_id)

        likes_str = list(map(str, likes_int))

        self.supabase.table("publicaciones").update({
            "likes": likes_str}).eq("id", post_id).execute()
