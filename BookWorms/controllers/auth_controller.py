from BookWorms.models.user_model import User
from BookWorms.utils.security import hash_password, verify_password


class AuthController:

    @staticmethod
    def register_user(email: str, username: str, password: str) -> tuple[bool, str]:
        if len(password) < 8:
            return False, "Password must be at least 8 characters."

        if User.get_user_by_username(username):
            return False, "Username already exists."

        user = User.create_user(email, username, password)
        if not user:
            return False, "Failed to create user."
        return True, "Registration successful."

    @staticmethod
    def login_user(username: str, password: str) -> tuple[bool, str, dict]:
        user = User.get_user_by_username(username)

        if not user:
            return False, "Invalid credentials.", {}

        if not verify_password(password, user[0]['passw']):
            return False, "Invalid credentials.", {}

        return True, "Login successful.", user[0]
