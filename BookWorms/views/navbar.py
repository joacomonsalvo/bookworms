import reflex as rx
from BookWorms.state.search_state import SearchState
from BookWorms.state.auth_state import AuthState


def navbar() -> rx.Component:
    return rx.hstack(
        rx.text("BookWorms Feed", font_size="8", font_weight="bold"),
        rx.spacer(),
        rx.input(
            placeholder="Buscar...",
            width="200px",
            on_change=SearchState.set_query
        ),
        rx.button(
            "Buscar",
            color_scheme="blue",
            on_click=[  # Sólo seteamos la query y navegamos
                SearchState.buscar,  # Guarda self.resultados en el estado
                rx.redirect("/search")  # Cambia a /search
            ]
        ),
        rx.link("Feed", href="/feed", ml=4),
        rx.link("Amigos", href="/amigos", ml="4"),
        rx.link("Listas", href="/listas", ml="4"),
        rx.link("Reportes", href="/reportes", ml="4"),
        rx.link("Nuevo Posteo", href="/new_post", ml="4"),
        rx.cond(
            AuthState.is_admin,
            rx.button("AB Libro", size="2", color_scheme="green",
                      on_click=rx.redirect("/ab_libro")),
            rx.text("")
        ),
        rx.button("Cambiar Contraseña", on_click=AuthState.set_change_pass_dialog_open(True), ml="4"),
        rx.button("Cerrar Sesión", color_scheme="red", on_click=AuthState.open_logout_dialog, ml="4"),
        padding="1rem",
        border_bottom="1px solid #ccc",
        align="center",
        width="100%",
    )
