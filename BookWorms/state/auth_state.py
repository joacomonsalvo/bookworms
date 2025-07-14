import reflex as rx
from BookWorms.controllers.auth_controller import AuthController
from BookWorms.models.dbbroker import DBBroker


class AuthState(rx.State):
    username: str
    password: str
    email: str = ""
    message: str = ""
    is_logged_in: bool = False
    current_user_id: int | None = None
    current_username: str = ""
    show_logout_confirm: bool = False
    local_storage: dict = {}
    is_admin: bool = False

    def register(self):
        success, msg = AuthController.register_user(self.email, self.username, self.password)
        self.message = msg
        if success:
            self.reset_fields()

    def save_auth_to_storage(self):
        self.local_storage["is_logged_in"] = self.is_logged_in
        self.local_storage["current_user_id"] = self.current_user_id
        self.local_storage["current_username"] = self.current_username

    def load_auth_from_storage(self):
        if self.local_storage.get("is_logged_in") and self.local_storage.get("current_user_id") and self.local_storage.get("current_username"):
            self.is_logged_in = True
            self.current_user_id = int(self.local_storage.get("current_user_id"))
            self.current_username = self.local_storage.get("current_username")

    def login(self):
        success, msg, user_data = AuthController.login_user(self.username, self.password)

        db = DBBroker()
        db.insert_current_user(self.username)

        self.message = msg
        self.is_logged_in = success
        if success:
            self.current_user_id = user_data['id']
            self.current_username = user_data['user']
            self.is_admin = db.es_admin(username=self.username)
            self.save_auth_to_storage()
            self.reset_fields()
            del db
            return rx.redirect("/feed")

    def reset_fields(self):
        self.email = ""
        self.username = ""
        self.password = ""

    def open_logout_dialog(self):
        """Show logout confirmation dialog"""
        self.show_logout_confirm = True

    def confirm_logout(self):
        """Confirm and logout the user"""
        self.is_logged_in = False
        self.current_user_id = None
        self.current_username = ""
        self.show_logout_confirm = False
        self.message = ""  # Clear any existing messages
        self.local_storage.clear()
        return rx.redirect("/login")

    def cancel_logout(self):
        """Cancel logout operation"""
        self.show_logout_confirm = False

    def clear_message(self):
        """Clear any existing messages"""
        self.message = ""

    def get_current_user_id(self) -> int | None:
        """Get the current user ID as an actual value"""
        return self.current_user_id
