import reflex as rx
from BookWorms.state.search_state import SearchState

def render_search_result(item) -> rx.Component:
    '''
    data = getattr(item, "_var_data", item) or {}
    if "titulo" in data:
        return rx.card(
            rx.vstack(
                rx.heading(data["titulo"], size="5"),
                rx.text(f"ISBN: {data.get('isbn','–')}"),
                rx.text(f"Autor: {data.get('autor','–')}"),
                rx.text(f"Editorial: {data.get('editorial','–')}"),
                rx.text(data.get("sinopsis","–")),
                rx.button("Agregar a lista privada", color_scheme="green", size="sm"),
            ),
            margin_y="1rem",
        )
    elif "user" in data:
        return rx.card(
            rx.vstack(
                rx.heading(data["user"], size="5"),
                rx.text(f"Email: {data.get('email','–')}"),
            ),
            margin_y="1rem",
        )
    else:
        # no debería llegar aquí si hay datos correctos
        return rx.text("No se reconoce el elemento", color="red")
        '''
'''
def search_result_page() -> rx.Component:
    return rx.vstack(
        rx.heading("Resultados de búsqueda", size="6", padding_top="1rem"),
        rx.cond(
            SearchState.resultados,
            rx.foreach(SearchState.resultados, render_search_result),
            rx.text("No se encontraron resultados.", color="gray"),
        ),
        padding="2rem",
        on_mount=SearchState.buscar,   # ← aquí forzamos la búsqueda al entrar
    )'''

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
