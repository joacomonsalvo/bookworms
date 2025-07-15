import reflex as rx
from BookWorms.controllers.auth_controller import AuthController
from BookWorms.models.dbbroker import DBBroker
from BookWorms.controllers.auth_controller import hash_password


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
    es_admin: bool = False
    change_pass_dialog_open: bool = False
    new_password: str = ""
    confirm_password: str = ""

    def register(self):
        success, msg = AuthController.register_user(self.email, self.username, self.password)
        self.message = msg
        if success:
            self.reset_fields()

    def save_auth_to_storage(self):
        self.local_storage["is_logged_in"] = self.is_logged_in
        self.local_storage["current_user_id"] = self.current_user_id
        self.local_storage["current_username"] = self.current_username
        self.local_storage["es_admin"] = self.es_admin

    def load_auth_from_storage(self):
        if self.local_storage.get("is_logged_in") and self.local_storage.get("current_user_id") and self.local_storage.get("current_username"):
            self.is_logged_in = True
            self.current_user_id = int(self.local_storage.get("current_user_id"))
            self.current_username = self.local_storage.get("current_username")

    def login(self):
        success, msg, user_data = AuthController.login_user(self.username, self.password)

        db = DBBroker()
        db.insert_current_user(self.username)
        db.insert_current_user_es_admin(self.username, self.es_admin)

        self.message = msg
        self.is_logged_in = success

        if success:
            self.current_user_id = user_data['id']
            self.current_username = user_data['user']
            self.is_admin = db.es_admin(username=self.username)
            self.es_admin = user_data["es_admin"]

            self.save_auth_to_storage()
            self.reset_fields()

            self.change_pass_dialog_open = False
            self.show_logout_confirm = False
            self.cancel_change_password()

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
        self.message = ""
        self.es_admin = False
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

    @rx.event
    def change_password(self):
        if not self.new_password or not self.confirm_password:
            self.message = "Debes completar ambos campos."
            return
        if len(self.new_password) < 8 or len(self.confirm_password) < 8:
            self.message = "Ingrese mas de 8 caracteres."
            return
        if self.new_password != self.confirm_password:
            self.message = "Las contraseñas deben coincidir."
            return
        self.message = ""
        DBBroker().supabase.table("usuarios") \
            .update({"passw": hash_password(self.new_password)}) \
            .eq("id", self.current_user_id) \
            .execute()
        AuthState.set_change_pass_dialog_open(False)
        return rx.redirect("/login")

    @staticmethod
    def change_password_confirm_logout():
        AuthState.is_logged_in = False
        AuthState.current_user_id = None
        AuthState.current_username = ""
        AuthState.message = ""
        AuthState.es_admin = False
        return rx.redirect("/login")

    @rx.event
    def cancel_change_password(self):
        self.change_pass_dialog_open = False
        self.new_password = ""
        self.confirm_password = ""
        self.message = ""
