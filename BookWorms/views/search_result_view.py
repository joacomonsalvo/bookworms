import reflex as rx
from BookWorms.state.search_state import SearchState


def render_book_card(book) -> rx.Component:
    return rx.card(
        rx.vstack(
            rx.heading(book["titulo"], size="5"),
            rx.text(f"ISBN: {book['isbn']}"),
            rx.text(f"Autor: {book['autor']}"),
            rx.text(f"Editorial: {book['editorial']}"),
            rx.text(book["sinopsis"]),
            rx.button("Agregar a lista privada", color_scheme="green", size="2"),
        ),
        margin_y="1rem",
    )


def render_user_card(user) -> rx.Component:
    return rx.card(
        rx.vstack(
            rx.heading(user["user"], size="5"),
            rx.text(f"Email: {user['email']}"),
        ),
        margin_y="1rem",
    )


def search_result_page() -> rx.Component:
    return rx.vstack(
        # 1) ESTE LINK VA AQUÍ, justo al principio de la página:
        rx.link(
            "← Volver a la página principal",
            href="/feed",  # vuelve al feed
            color_scheme="blue",
            font_size="2",
            margin_bottom="1rem"
        ),

        # 2) Después tu título de resultados
        rx.heading("Resultados de búsqueda", size="6", padding_top="1rem"),

        # Si la query empieza con "@", renderiza usuarios, si no, libros
        rx.cond(
            SearchState.query.startswith("@"),
            # quitamos la arroba y recorremos usuarios
            rx.foreach(
                SearchState.resultados,
                render_user_card
            ),
            # caso contrario, recorremos libros
            rx.foreach(
                SearchState.resultados,
                render_book_card
            ),
        ),

        # Mensaje si no hay nada
        rx.cond(
            SearchState.resultados,
            rx.fragment(),  # nada
            rx.text("No se encontraron resultados.", color="gray")
        ),

        padding="2rem",
        on_mount=SearchState.search_and_redirect,  # o SearchState.buscar
    )
