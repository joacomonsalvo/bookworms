import reflex as rx
from BookWorms.state.ab_libro_state import ABLibroState
from BookWorms.views.navbar import navbar


def ab_libros_view() -> rx.Component:
    return rx.center(
        rx.vstack(
            navbar(),
            rx.heading("AB Libro", size="8"),
            rx.text("Selecciona una opción:", font_size="6"),
            rx.hstack(
                rx.button(
                    "Alta",
                    on_click=lambda: ABLibroState.set_modo(value="Alta"),
                    color_scheme="green",
                    width="100px"
                ),
                rx.button(
                    "Baja",
                    on_click=lambda: ABLibroState.set_modo(value="Baja"),
                    color_scheme="red",
                    width="100px"
                ),
                spacing="4"
            ),
            rx.cond(
                ABLibroState.modo == "Alta",
                rx.vstack(
                    rx.input(
                        placeholder="Título",
                        on_change=ABLibroState.set_titulo,
                        width="300px"
                    ),
                    rx.input(
                        placeholder="ISBN",
                        on_change=ABLibroState.set_isbn,
                        width="300px"
                    ),
                    rx.input(
                        placeholder="Autor",
                        on_change=ABLibroState.set_autor,
                        width="300px"
                    ),
                    rx.input(
                        placeholder="Editorial",
                        on_change=ABLibroState.set_editorial,
                        width="300px"
                    ),
                    rx.text_area(
                        placeholder="Sinopsis",
                        on_change=ABLibroState.set_sinopsis,
                        width="300px"
                    ),
                    spacing="3",
                    align="center"
                ),
                rx.input(
                    placeholder="ISBN",
                    on_change=ABLibroState.set_isbn,
                    width="300px"
                )
            ),
            rx.button(
                "Ejecutar",
                on_click=ABLibroState.ejecutar_accion,
                color_scheme="blue",
                width="300px",
            ),
            spacing="5",
            align="center",
            width="100%",
        ),
        padding="6"
    )
