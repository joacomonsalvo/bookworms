# views/login_view.py

import reflex as rx
from BookWorms.state.auth_state import AuthState

def login_view():
    return rx.center(rx.vstack(
        rx.heading("Login", size="6"),
        rx.input(placeholder="Username", on_change=AuthState.set_username),
        rx.input(placeholder="Password", type_="password", on_change=AuthState.set_password),
        rx.button("Login", on_click=AuthState.login),
        rx.text(AuthState.message, color="red"),
        on_mount=AuthState.clear_message,
    ),
        min_height="100vh"
    )
