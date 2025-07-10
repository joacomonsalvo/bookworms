# models/user_model.py

from BookWorms.models.dbbroker import DBBroker


supabase = DBBroker()


class User:
    @staticmethod
    def create_user(email: str, username: str, password: str):
        return supabase.create_user(email, username, password)

    @staticmethod
    def get_user_by_username(username: str):
        return supabase.get_user_by_username(username)

    @staticmethod
    def get_user_by_id(user_id: int):
        return supabase.get_user_by_id(user_id)

    @staticmethod
    def supabase_client():
        return supabase.supabase
