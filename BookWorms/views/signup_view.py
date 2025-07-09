# views/signup_view.py

import reflex as rx
from BookWorms.state.auth_state import AuthState
from BookWorms.controllers.auth_controller import AuthController

class SignupState(rx.State):
    """State to handle signup form inputs and feedback."""
    email: str = ""
    username: str = ""
    password: str = ""
    message: str = ""

    def handle_submit(self):
        success, msg = AuthController.register_user(
            self.email, self.username, self.password
        )
        self.message = msg
        if success:
            return rx.redirect("/login")  # Redirect to login on success


def signup_view() -> rx.Component:
    return rx.center(
        rx.vstack(
            rx.heading("Sign Up", size="6"),
            rx.text("Create your BookWorms account"),
            rx.form(
                rx.vstack(
                    rx.input(
                        placeholder="Email",
                        value=SignupState.email,
                        on_change=SignupState.set_email,
                        is_required=True,
                    ),
                    rx.input(
                        placeholder="Username",
                        value=SignupState.username,
                        on_change=SignupState.set_username,
                        is_required=True,
                    ),
                    rx.input(
                        placeholder="Password",
                        type_="password",
                        value=SignupState.password,
                        on_change=SignupState.set_password,
                        is_required=True,
                    ),
                    rx.button("Sign Up", type_="submit"),
                ),
                on_submit=SignupState.handle_submit,
                reset_on_submit=True,
            ),
            rx.text(SignupState.message, color=rx.cond(SignupState.message.contains("error"), "red", "green")),
            rx.link("Already have an account? Login here.", href="/login"),
            spacing="4",
            width="100%",
            max_width="400px",
        ),
        min_height="100vh",
        padding="4",
    )
