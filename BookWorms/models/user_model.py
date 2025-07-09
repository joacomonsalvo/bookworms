# models/user_model.py

from typing import Optional
from BookWorms.utils.security import hash_password
from supabase import create_client
import os

SUPABASE_URL = "https://gpxgzundtgiefumaybfg.supabase.co"  #os.getenv("SUPABASE_URL")
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImdweGd6dW5kdGdpZWZ1bWF5YmZnIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTIwMDgzNjAsImV4cCI6MjA2NzU4NDM2MH0.EpxS2a35JiiZQlobD2R13_bMFEucwKsQ4CWK3A-0d0k"  #os.getenv("SUPABASE_SERVICE_KEY")
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)


class User:
    @staticmethod
    def create_user(email: str, username: str, password: str) -> Optional[dict]:
        password_hash = hash_password(password)

        result = supabase.table("usuarios").insert({
            "email": email,
            "user": username,
            "passw": password_hash
        }).execute()

        return result.data[0]



    @staticmethod
    def get_user_by_username(username: str) -> Optional[dict]:
        result = supabase.table("usuarios").select("*").eq("user", username).execute()
        
        return result.data


