# state/auth_state.py

import reflex as rx
from BookWorms.controllers.auth_controller import AuthController


class AuthState(rx.State):
    username: str
    password: str
    email: str = ""
    message: str = ""
    is_logged_in: bool = False

    def register(self):
        success, msg = AuthController.register_user(self.email, self.username, self.password)
        self.message = msg
        if success:
            self.reset_fields()

    def login(self):
        success, msg = AuthController.login_user(self.username, self.password)
        self.message = msg
        self.is_logged_in = success
        if success:
            self.reset_fields()

    def reset_fields(self):
        self.email = ""
        self.username = ""
        self.password = ""
