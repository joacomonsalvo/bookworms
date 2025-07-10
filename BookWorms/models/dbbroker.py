import os
from dotenv import load_dotenv
from supabase import create_client
from BookWorms.utils.security import hash_password


class DBBroker:
    def __init__(self):
        dotenv_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), ".env")
        load_dotenv(dotenv_path)

        SUPABASE_URL = os.getenv("SUPABASE_URL")
        SUPABASE_KEY = os.getenv("SUPABASE_KEY")
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
