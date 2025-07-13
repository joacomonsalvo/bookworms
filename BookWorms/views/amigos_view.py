import reflex as rx

from BookWorms.state.auth_state import AuthState
from BookWorms.state.amigos_state import AmigosState
from BookWorms.views.feed_view import navbar


def render_user_card(user) -> rx.Component:
    return rx.card(
        rx.vstack(
            rx.heading(user["user"], size="5"),
            rx.text(f"Email: {user['username']}"),
            rx.button(
                "Eliminar amigo", 
                color_scheme="red", 
                size="2",
                on_click=lambda: AmigosState.eliminar_amigo(
                    AmigosState.get_current_user_id(),
                    user['id']
                )
            ),
        ),
        margin_y="1rem",
    )


def amigos_view() -> rx.Component:
    return rx.cond(
        AuthState.is_logged_in,
        rx.vstack(
            navbar(),

            rx.heading("Amigos", size="6", padding_top="1rem"),

            rx.foreach(
                AmigosState.resultados,
                render_user_card),

            rx.cond(
                AmigosState.resultados,
                rx.fragment(),
                rx.text("No se encontraron amigos.", color="gray")
            ),

            padding="2rem",
            on_mount=AmigosState.get_friends_and_redirect,
        ),
        rx.script("window.location.href = '/login'")
    )
