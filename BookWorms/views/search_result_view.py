import reflex as rx
from BookWorms.state.search_state import SearchState

def render_search_result(item) -> rx.Component:
    # convertir Var a dict
    data = getattr(item, "_var_data", item)
    # si es un libro
    if "titulo" in data:
        return rx.card(
            rx.vstack(
                rx.heading(data["titulo"], size="5"),
                rx.text(f"ISBN: {data.get('isbn','–')}"),
                rx.text(f"Autor: {data.get('autor','–')}"),
                rx.text(f"Editorial: {data.get('editorial','–')}"),
                rx.text(data.get('sinopsis','–')),
                rx.button("Agregar a lista privada", color_scheme="green", size="sm")
            ),
            margin_y="1rem",
        )
    # si es un usuario
    return rx.card(
        rx.vstack(
            rx.heading(data.get("user","–"), size="5"),
            rx.text(f"Email: {data.get('email','–')}"),
        ),
        margin_y="1rem",
    )

'''def search_results_view() -> rx.Component:
    return rx.vstack(
        rx.heading("Resultados de búsqueda", size="6", padding_top="1rem"),
        rx.cond(
            # si hay resultados
            SearchState.resultados != [],
            rx.foreach(SearchState.resultados, render_search_result),
            # si no encontró nada
            rx.text("No se encontraron resultados.", color="gray")
        ),
        padding="2rem",
    )'''
'''def search_result_page() -> rx.Component:
    return rx.vstack(
        rx.heading("Resultado"),
    padding="2rem",
    )'''

def search_result_page() -> rx.Component:
    return rx.vstack(
        rx.heading("Resultados de búsqueda", size="6", padding_top="1rem"),
        rx.cond(
            # si hay resultados
            SearchState.resultados != [],
            rx.foreach(SearchState.resultados, render_search_result),
            # si no encontró nada
            rx.text("No se encontraron resultados.", color="gray")
        ),
        padding="2rem",
    )