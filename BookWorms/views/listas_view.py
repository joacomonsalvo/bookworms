import reflex as rx
from BookWorms.state.auth_state import AuthState
from BookWorms.state.listas_state import ListasState
from BookWorms.state.search_state import SearchState


def listas_view() -> rx.Component:
    return rx.center(
        rx.vstack(
            # Botón para volver al Feed y crear nueva lista
            rx.hstack(
                rx.link(
                    "← Volver al Feed",
                    href="/feed",
                    size="4",
                    color="teal.400",
                    _hover={"color": "teal.200"},
                ),
                rx.button(
                    "Nueva Lista",
                    color_scheme="blue",
                    on_click=ListasState.open_new_list_modal,
                    size="2",
                ),
                # rx.button(
                #    "Cargar listas",
                #    #on_click=lambda: ListasState.load_all(AuthState.current_user_id),
                #    on_click=lambda *_, uid=AuthState.current_user_id: ListasState.load_all(uid),
                #    margin_bottom="1rem",
                # ),
                width="100%",
                mb="4",
                justify="between",
            ),

            # Cabecera
            rx.heading("Página de Listas", size="9", padding_top="1.5rem"),
            # rx.text(
            # f"Usuario actual: {AuthState.current_username}",
            # color="gray.400",
            # mb="4",
            # ),

            # Modal para crear nueva lista
            rx.cond(
                ListasState.new_list_modal_open,
                rx.box(
                    rx.center(
                        rx.box(
                            rx.heading("Crear Nueva Lista", size="6", mb="4"),
                            rx.input(
                                placeholder="Título de la lista",
                                value=ListasState.new_list_title,
                                on_change=lambda v: ListasState.set_new_list_title(v),
                                mb="2",
                            ),
                            rx.select(
                                items=["publica", "privada"],
                                value=ListasState.new_list_type,
                                on_change=lambda v: ListasState.set_new_list_type(v),
                                mb="4",
                            ),
                            rx.hstack(
                                rx.button(
                                    "Crear",
                                    color_scheme="green",
                                    # on_click=lambda *_, uid=AuthState.current_user_id: ListasState.create_list(uid),
                                    on_click=ListasState.create_list,
                                    size="3",
                                ),
                                rx.button(
                                    "Cancelar",
                                    on_click=ListasState.close_new_list_modal,
                                    size="3",
                                ),
                                spacing="4",
                            ),
                            bg="gray.800",
                            p="1.5rem",
                            border_radius="0.5rem",
                            max_w="400px",
                        )
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
                                    # on_click=ListasState.delete_list,
                                    on_click=lambda *_, uid=AuthState.current_user_id: ListasState.delete_list(uid),
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

                            # Buscador de libros dentro del modal
                            rx.vstack(
                                # Input y botón Buscar
                                rx.hstack(
                                    rx.input(
                                        placeholder="Buscar libro...",
                                        value=SearchState.query,
                                        on_change=lambda v: SearchState.set_query(v),
                                        width="60%",
                                    ),
                                    rx.button(
                                        "Buscar",
                                        on_click=SearchState.search_books,
                                        size="3",
                                    ),
                                    spacing="2",
                                    padding_top="1rem",
                                ),
                                # Resultados de búsqueda
                                rx.vstack(
                                    rx.heading("Resultados de búsqueda", size="5", padding_top="1rem"),
                                    rx.foreach(
                                        SearchState.resultados.to(list[dict]),
                                        lambda libro: rx.hstack(
                                            rx.text(f"{libro['titulo']} — {libro['autor']}"),
                                            rx.button(
                                                "Agregar a la lista",
                                                on_click=lambda *_, bid=libro["id"]: ListasState.add_book_by_id(bid),
                                                size="2",
                                            ),
                                            spacing="2",
                                        ),
                                    ),
                                ),
                                # Botón para limpiar búsqueda
                                rx.button(
                                    "Limpiar búsqueda",
                                    on_click=SearchState.clear_search,
                                    size="3",
                                    padding_top="0.5rem",
                                    pb="1.5rem",
                                ),
                                # Listado de libros ya en la lista
                                rx.vstack(
                                    rx.heading("Libros en la lista", size="5", padding_top="1rem"),
                                    rx.foreach(
                                        ListasState.selected_list_books.to(list[dict]),
                                        lambda libro: rx.hstack(
                                            rx.text(f"{libro['titulo']} — {libro['autor']}"),
                                            rx.button(
                                                "Eliminar libro",
                                                on_click=lambda *_, bid=libro['id']: ListasState.remove_book_from_list(
                                                    bid),
                                                size="2",
                                            ),
                                            spacing="2",
                                        ),
                                    ),
                                ),
                            ),

                            bg="gray.800",
                            p="1.5rem",
                            border_radius="0.5rem",
                            max_w="500px",
                        )
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
        pt="1rem",
        min_height="80vh",
        bg="gray.900",
        # on_mount=rx.run(ListasState.load_all, AuthState.current_user_id),
        on_mount=ListasState.load_all,
        # on_click=lambda *_, uid=AuthState.current_user_id: ListasState.create_list(uid),
    )
