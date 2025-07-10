import os
from dotenv import load_dotenv
from supabase import create_client
from BookWorms.utils.security import hash_password


class DBBroker:
    def __init__(self):
        dotenv_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), ".env")
        load_dotenv(dotenv_path)

        #SUPABASE_URL = os.getenv("SUPABASE_URL")
        #SUPABASE_KEY = os.getenv("SUPABASE_KEY")
        SUPABASE_URL = 'https://gpxgzundtgiefumaybfg.supabase.co'
        SUPABASE_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImdweGd6dW5kdGdpZWZ1bWF5YmZnIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTIwMDgzNjAsImV4cCI6MjA2NzU4NDM2MH0.EpxS2a35JiiZQlobD2R13_bMFEucwKsQ4CWK3A-0d0k'
        self.supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

    def create_user(self, email: str, username: str, password: str):
        password_hash = hash_password(password)

        result = self.supabase.table("usuarios").insert({
            "email": email,
            "user": username,
            "passw": password_hash
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
        print("🔍 dbbroker.buscar_libros – patrón:", pattern)

        result = (
            self.supabase
            .table("libros")
            .select("*")
            .ilike("titulo", pattern)
            .execute()
        )
        print("🔎 dbbroker.buscar_libros – resultado:", result.data)
        return result.data or []

    '''def buscar_usuarios(self, username):
        result = self.supabase.table("usuarios") \
            .select("*") \
            .ilike("user", f"%{username}%") \
            .execute()
        return result.data'''

    def buscar_usuarios(self, username: str):
        pattern = f"%{username.lower()}%"
        print("🔍 Buscando usuarios con patrón:", pattern)
        result = self.supabase.table("usuarios")\
            .select("*")\
            .ilike("user", pattern)\
            .execute()
        print("🔎 Resultado raw de Supabase:", result.data)
        return result.data or []

