import reflex as rx
from BookWorms.state.auth_state import AuthState
from BookWorms.state.listas_state import ListasState
from BookWorms.state.search_state import SearchState


def listas_view() -> rx.Component:
    return rx.vstack(
        # Contenedor principal en vertical
        rx.vstack(
            # 1) Botón para volver al Feed y botones de listas agrupados a la derecha
            rx.hstack(
                rx.link("← Volver al Feed", href="/feed", size="4", color="teal.400", _hover={"color": "teal.200"}, ),
                rx.hstack(
                    rx.button("Nueva Lista", color_scheme="blue", on_click=ListasState.open_new_list_modal, size="2", ),
                    spacing="1",
                ),
                width="100%", justify="between", align_items="center", mb="4",
            ),

            # 2) Cabecera con título
            rx.heading("Página de Listas", size="9", padding_top="1.5rem", mb="4", padding_bottom="2.5rem",
                       ),

            # 3) Modal para crear nueva lista
            rx.cond(ListasState.new_list_modal_open,
                    rx.box(
                        rx.center(
                            rx.box(
                                rx.heading("Crear Nueva Lista", size="6", mb="4", padding_bottom="1rem"),
                                rx.input(placeholder="Título de la lista", value=ListasState.new_list_title,
                                         on_change=lambda v: ListasState.set_new_list_title(v), mb="2"),

                                rx.cond(
                                    AuthState.es_admin,
                                    rx.select(items=["publica", "privada"], value=ListasState.new_list_type,
                                              on_change=lambda v: ListasState.set_new_list_type(v), mb="4"),

                                    rx.select(items=["privada"], value=ListasState.new_list_type,
                                              on_change=lambda v: ListasState.set_new_list_type(v), mb="4"),
                                ),
                                rx.hstack(
                                    rx.button("Crear", color_scheme="green", on_click=ListasState.create_list,
                                              size="3"),
                                    rx.button("Cancelar", on_click=ListasState.close_new_list_modal, size="3"),
                                    padding_top="1rem", spacing="4",
                                ),
                                bg="grey.800", p="1.5rem", border_radius="0.5rem", max_w="400px", padding_top="1rem",
                                padding_bottom="1rem", padding_left="1rem", padding_right="1rem",
                            )
                        ),
                        position="fixed", w="100vw", h="100vh", bg="rgba(0,0,0,2)", z_index=1000, border_radius="1rem",
                        top="50%", left="50%", transform="translate(-50%, -50%)",
                    ),
                    None,
                    ),

            # 4) Modal de detalle de lista
            rx.cond(ListasState.is_modal_open,
                    rx.box(
                        rx.center(
                            rx.box(
                                rx.heading(ListasState.selected_list.get("titulo", "Lista"), size="6", mb="4", ),

                                # Botones Cerrar y Eliminar Lista
                                rx.hstack(
                                    rx.cond(
                                        (ListasState.selected_list_type == "privada") | (
                                                ListasState.selected_list_type == "publica") & AuthState.es_admin,
                                        rx.button("Eliminar Lista", color_scheme="red", on_click=lambda *_,
                                                                                                        uid=AuthState.current_user_id: ListasState.delete_list(
                                            uid), size="3"),
                                    ),
                                    rx.button("Cerrar", on_click=ListasState.close_modal, size="3", ),
                                    spacing="4", justify="start", padding_top="1rem", padding_bottom="1rem",
                                ),

                                # Buscador de libros dentro del modal
                                rx.vstack(

                                    # Input y botón Buscar
                                    rx.cond(
                                        (ListasState.selected_list_type == "publica") & ~AuthState.es_admin,
                                        rx.text(""),
                                        rx.hstack(
                                            rx.input(placeholder="Buscar libro...", value=SearchState.query,
                                                     on_change=lambda v: SearchState.set_query(v), width="60%"),
                                            rx.button("Buscar", on_click=SearchState.search_books, size="3", ),
                                            spacing="2", padding_top="1rem",
                                        ),
                                    ),
                                    # Resultados de búsqueda
                                    rx.cond(
                                        (ListasState.selected_list_type == "publica") & ~AuthState.es_admin,
                                        rx.text(""),
                                        rx.vstack(
                                            rx.heading("Resultados de búsqueda", size="5", padding_top="1rem"),
                                            rx.foreach(
                                                SearchState.resultados.to(list[dict]),
                                                lambda libro:
                                                rx.hstack(rx.text(f"{libro['titulo']} — {libro['autor']}"),
                                                          rx.button("Agregar a la lista", on_click=lambda *_, bid=libro[
                                                              "id"]: ListasState.add_book_by_id(bid), size="2"),
                                                          spacing="2",
                                                          ),
                                            ),
                                        ),
                                    ),
                                    # Botón para limpiar búsqueda
                                    rx.cond(
                                        (ListasState.selected_list_type == "publica") & ~AuthState.es_admin,
                                        rx.text(""),
                                        rx.button("Limpiar búsqueda", on_click=SearchState.clear_search, size="3",
                                                  padding_top="0.5rem", pb="1.5rem", ),
                                    ),
                                    # Listado de libros ya en la lista
                                    rx.vstack(
                                        rx.heading("Libros en la lista", size="5", padding_top="1rem"),
                                        rx.foreach(
                                            ListasState.selected_list_books.to(list[dict]),
                                            lambda libro: rx.hstack(
                                                rx.text(f"{libro['titulo']} — {libro['autor']}"),
                                                rx.cond(
                                                    (ListasState.selected_list_type == "publica") & ~AuthState.es_admin,
                                                    rx.text(""),
                                                    rx.button("Eliminar libro", on_click=lambda *_, bid=libro[
                                                        'id']: ListasState.remove_book_from_list(bid), size="2", ),
                                                ),
                                                spacing="2",
                                            ),
                                        ),
                                    ),
                                ),
                                bg="gray.800", p="1.5rem", border_radius="0.5rem", max_w="500px", padding_bottom="1rem",
                            ),
                        ),
                        position="fixed", top="50%", left="50%", w="100vw", h="100vh", bg="rgba(0,0,0,2)", z_index=1000,
                        border_radius="1rem", padding_top="1rem", padding_left="1rem", padding_right="1rem",
                        padding_bottom="1rem", transform="translate(-50%, -50%)",
                    ),
                    None,
                    ),

            # 5) Contenedor de dos columnas con listas públicas y privadas
            rx.vstack(

                # Listas Públicas
                rx.vstack(
                    rx.heading("Listas Públicas", size="8", mb="4", align_self="start"),
                    rx.hstack(
                        rx.foreach(
                            ListasState.public_lists.to(list[dict]),
                            lambda lista: rx.box(
                                rx.heading(lista.get("titulo"), size="4", mb="2", padding_bottom="0.5rem"),
                                rx.button(
                                    "Ver Lista",
                                    size="3",
                                    on_click=lambda *_: ListasState.open_modal(lista, "publica"),
                                ),
                                p="4", bg="gray.800", border="3px solid", border_color="gray.700",
                                border_radius="0.5rem", box_shadow="md", mb="6", width="100%", padding="1rem",
                                min_width="300px", max_width="300px"
                            ),
                        ),
                        spacing="4", px="4", flex_wrap="wrap", justify="start",
                    ),
                ),

                # Listas Privadas
                rx.vstack(
                    rx.heading("Listas Privadas", size="8", mb="4", align_self="start"),
                    rx.hstack(
                        rx.foreach(
                            ListasState.private_lists.to(list[dict]),
                            lambda lista: rx.box(
                                rx.heading(lista.get("titulo"), size="4", mb="2", padding_bottom="0.5rem"),
                                rx.button(
                                    "Ver Lista",
                                    size="3",
                                    on_click=lambda *_: ListasState.open_modal(lista, "privada"),
                                ),
                                p="4", bg="gray.800", border="3px solid", border_color="gray.700",
                                border_radius="0.5rem", box_shadow="md", mb="6", width="100%", padding="1rem",
                                min_width="300px", max_width="300px",
                            ),
                        ),
                        spacing="4", px="4",
                    ),
                ),
                spacing="9", width="100%", flex_wrap="wrap", justify="start",
            ),
            width="100%", padding_right="2rem", padding_left="2rem",
        ),
        pt="2rem", pb="2rem", px="2rem", min_height="100vh", bg="gray.900", on_mount=ListasState.load_all,
        padding_top="2rem", width="100%",
    )
