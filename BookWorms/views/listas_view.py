'''import reflex as rx

from BookWorms.state.auth_state import AuthState
from BookWorms.state.listas_state import ListasState

def listas_view() -> rx.Component:
    return rx.center(
        rx.vstack(
            # Botón para volver al Feed1
            rx.hstack(
                rx.link(
                    "← Volver al Feed",
                    href="/feed",
                    size="5",
                    color="teal.400",
                    _hover={"color": "teal.200"},
                ),
                width="100%",
                mb="4",
            ),

            # Cabecera
            rx.heading("Página de Listas", size="9", padding_top="1.5rem"),
            rx.text(
                f"Usuario actual: {AuthState.current_username}",
                color="gray.400",
                mb="4",
            ),

            # Debug: cantidad de listas
            rx.hstack(
                rx.text("Públicas cargadas:"),
                rx.text(ListasState.public_lists.length()),
                spacing="2",
            ),
            rx.hstack(
                rx.text("Privadas cargadas:"),
                rx.text(ListasState.private_lists.length()),
                spacing="2",
                mb="4",
            ),

            rx.cond(
                ListasState.is_modal_open,
                rx.box(
                    # 1) Child posicional: centro tu cuadro
                    rx.center(
                        rx.box(
                            # a) El contenido interior (header, body, footer)
                            rx.heading(ListasState.selected_list["titulo"], size="6", mb="4"),
                            rx.hstack(
                                rx.button(
                                    "Eliminar",
                                    color_scheme="red",
                                    on_click=ListasState.delete_list
                                ),
                                rx.button(
                                    "Cerrar",
                                    on_click=ListasState.close_modal
                                ),
                                spacing="4",
                                justify="end",
                            ),
                            # b) Props de estilo del cuadro interior
                            bg="gray.800",
                            p="1.5rem",
                            border_radius="0.5rem",
                            max_w="500px",
                        ),
                    ),
                    # 2) Luego todos los props con nombre del overlay
                    position="fixed",
                    top=0,
                    left=0,
                    w="100vw",
                    h="100vh",
                    bg="rgba(0,0,0,0.5)",
                    z_index=1000,
                ),
                None,
            ),

            # Contenedor de dos columnas
            rx.hstack(
                # Listas Públicas
                rx.vstack(
                    rx.heading("Listas Públicas", size="8", mb="4"),
                    rx.foreach(
                        ListasState.public_lists,
                        lambda lista: rx.box(
                            rx.heading(lista["titulo"], size="4", mb="2", padding_bottom="0.5rem"),
                            rx.button(
                                "Ver Lista",
                                size="3",
                                on_click=lambda lst=lista: ListasState.open_modal(lst),
                            ),
                            p="4",
                            bg="gray.800",
                            border="3px solid",
                            border_color="gray.700",
                            border_radius="0.5rem",
                            box_shadow="md",
                            mb="6",
                            width="100%",
                            padding="1rem",
                        ),
                    ),
                    spacing="4",
                    px="4",
                ),

                # Listas Privadas
                rx.vstack(
                    rx.heading("Listas Privadas", size="8", mb="4"),
                    rx.foreach(
                        ListasState.private_lists,
                        lambda lista: rx.box(
                            rx.heading(lista["titulo"], size="4", mb="2", padding_bottom="0.5rem"),
                            rx.button(
                                "Ver Lista",
                                size="3",
                                on_click=lambda lst=lista: ListasState.open_modal(lst),
                            ),
                            p="4",
                            bg="gray.800",
                            border="3px solid",
                            border_color="gray.700",
                            border_radius="0.5rem",
                            box_shadow="md",
                            mb="6",
                            width="100%",
                            padding="1rem",
                        ),
                    ),
                    spacing="4",
                    px="4",
                ),

                spacing="8",
                width="100%",
                align="start",
            ),
        ),
        min_height="100vh",
        bg="gray.900",
        on_mount=ListasState.load_all,
    )'''

#-------------------------------------------------------------------------------------------------------------

import reflex as rx

from BookWorms.state.auth_state import AuthState
from BookWorms.state.listas_state import ListasState


def listas_view() -> rx.Component:
    return rx.center(
        rx.vstack(
            # Botón para volver al Feed
            rx.hstack(
                rx.link(
                    "← Volver al Feed",
                    href="/feed",
                    size="5",
                    color="teal.400",
                    _hover={"color": "teal.200"},
                ),
                width="100%",
                mb="4",
            ),

            # Cabecera
            rx.heading("Página de Listas", size="9", padding_top="1.5rem"),
            rx.text(
                f"Usuario actual: {AuthState.current_username}",
                color="gray.400",
                mb="4",
            ),

            # Modal de detalle de lista
            rx.cond(
                ListasState.is_modal_open,
                rx.box(
                    rx.center(
                        rx.box(
                            rx.heading(
                                ListasState.selected_list.get("titulo", "Lista"),
                                size="6",
                                mb="4",
                            ),
                            # Botones Cerrar y Eliminar Lista
                            rx.hstack(
                                rx.button(
                                    "Eliminar Lista",
                                    color_scheme="red",
                                    on_click=ListasState.delete_list,
                                    size="3",
                                ),
                                rx.button(
                                    "Cerrar",
                                    on_click=ListasState.close_modal,
                                    size="3",
                                ),
                                spacing="4",
                                justify="end",
                            ),

                            # Sección de libros usando rx.foreach
                            rx.vstack(
                                rx.heading("Libros en la lista", size="5", padding_top="1rem"),
                                rx.foreach(
                                    ListasState.selected_list_books.to(list[dict]),
                                    lambda libro: rx.hstack(
                                        rx.text(f"{libro['titulo']} — {libro['autor']}"),
                                        rx.button(
                                            "Eliminar libro",
                                            on_click=lambda _, bid=libro['id']: ListasState.remove_book_from_list(bid),
                                            size="2",
                                        ),
                                        spacing="2",
                                    ),
                                ),
                                # Formulario para agregar libro
                                rx.hstack(
                                    rx.input(
                                        placeholder="ID del libro",
                                        value=ListasState.new_book_id,
                                        on_change=lambda v: ListasState.set_new_book_id(v),
                                        width="60%",
                                    ),
                                    rx.button(
                                        "Agregar libro",
                                        on_click=lambda _: ListasState.add_book_to_list(),
                                        size="3",
                                    ),
                                    spacing="2",
                                    padding_top="1rem",
                                ),
                            ),

                            bg="gray.800",
                            p="1.5rem",
                            border_radius="0.5rem",
                            max_w="500px",
                        ),
                    ),
                    position="fixed",
                    top=0,
                    left=0,
                    w="100vw",
                    h="100vh",
                    bg="rgba(0,0,0,0.5)",
                    z_index=1000,
                ),
                None,
            ),

            # Contenedor de dos columnas con listas públicas y privadas
            rx.hstack(
                # Listas Públicas
                rx.vstack(
                    rx.heading("Listas Públicas", size="8", mb="4"),
                    rx.foreach(
                        ListasState.public_lists.to(list[dict]),
                        lambda lista: rx.box(
                            rx.heading(lista.get("titulo"), size="4", mb="2", padding_bottom="0.5rem"),
                            rx.button(
                                "Ver Lista",
                                size="3",
                                on_click=lambda *_: ListasState.open_modal(lista, "publica"),
                            ),
                            p="4",
                            bg="gray.800",
                            border="3px solid",
                            border_color="gray.700",
                            border_radius="0.5rem",
                            box_shadow="md",
                            mb="6",
                            width="100%",
                            padding="1rem",
                        ),
                    ),
                    spacing="4",
                    px="4",
                ),

                # Listas Privadas
                rx.vstack(
                    rx.heading("Listas Privadas", size="8", mb="4"),
                    rx.foreach(
                        ListasState.private_lists.to(list[dict]),
                        lambda lista: rx.box(
                            rx.heading(lista.get("titulo"), size="4", mb="2", padding_bottom="0.5rem"),
                            rx.button(
                                "Ver Lista",
                                size="3",
                                on_click=lambda *_: ListasState.open_modal(lista, "privada"),
                            ),
                            p="4",
                            bg="gray.800",
                            border="3px solid",
                            border_color="gray.700",
                            border_radius="0.5rem",
                            box_shadow="md",
                            mb="6",
                            width="100%",
                            padding="1rem",
                        ),
                    ),
                    spacing="4",
                    px="4",
                ),

                spacing="8",
                width="100%",
                align="start",
            ),
        ),
        min_height="100vh",
        bg="gray.900",
        on_mount=ListasState.load_all,
    )