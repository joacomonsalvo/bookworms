import reflex as rx

from BookWorms.state.auth_state import AuthState
from BookWorms.state.amigos_state import AmigosState
from BookWorms.views.navbar import navbar


def render_user_card(user) -> rx.Component:
    return rx.card(
        rx.vstack(
            rx.heading(user["username"], size="6"),
            rx.button(
                "Eliminar amigo", 
                color_scheme="red", 
                size="2",
                on_click=lambda: AmigosState.eliminar_amigo(
                    amigo_username=user['username']
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
