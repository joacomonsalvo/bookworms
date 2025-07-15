import reflex as rx
from BookWorms.state.reportes_state import ReportesState


def reportes_view() -> rx.Component:
    return rx.vstack(

        rx.link("← Volver al Feed", href="/feed", size="4", color="teal.400", _hover={"color": "teal.200"},
                padding="1rem"),
        rx.heading("Página de Reportes", size="9", padding_top="1.5rem", mb="4", padding_bottom="2.5rem"),

        # 3) Texto fijo “Seleccionar reporte:”
        rx.text("Seleccionar reporte:", size="4", mb="2"),

        # 4) Desplegable siempre visible
        rx.select(
            items=["Reporte de libros más leídos", "Reporte de libros por leer", "Reporte de usuarios más seguidos", ],
            value=ReportesState.selected_report, on_change=ReportesState.set_selected_report, mb="4",
        ),

        # 5) Botón Aceptar: elegimos cuál handler según el valor de la Var
        rx.cond(
            ReportesState.selected_report == "Reporte de libros más leídos",
            rx.button("Aceptar", color_scheme="blue", size="2",
                      on_click=ReportesState.load_libros_leidos),
            rx.cond(
                ReportesState.selected_report == "Reporte de libros por leer",
                rx.button("Aceptar", color_scheme="blue", size="2",
                          on_click=ReportesState.load_libros_por_leer),
                rx.button("Aceptar", color_scheme="blue", size="2",
                          on_click=ReportesState.load_usuarios_seguidos),
            ),
        ),

        rx.box(
            rx.vstack(
                rx.cond(
                    # Si es reporte de usuarios, iteramos username
                    ReportesState.selected_report == "Reporte de usuarios más seguidos",
                    rx.foreach(
                        ReportesState.report_data,
                        lambda row, i: rx.text(
                            f"{i + 1}. {row.username} — {row.veces} veces", size="5"
                        )
                    ),
                    # Else: reporte de libros (título)
                    rx.foreach(
                        ReportesState.report_data,
                        lambda row, i: rx.text(
                            f"{i + 1}. {row.titulo} — {row.veces} veces", size="5"
                        )
                    )
                ),
                padding="1rem",
            ),
            # position="fixed", w="100vw", h="100vh", bg="rgba(0,0,0,2)", z_index=1000, border_radius="1rem",
            # top="50%", left="50%", transform="translate(-50%, -50%)",
            border="1px solid",  # grosor y estilo de borde
            border_color="gray.500",  # color del borde
            border_radius="1rem",  # esquinas redondeadas
            padding="0.75rem",  # espacio interno
            bg="gray.800",  # color de fondo opcional
            max_width="600px",  # opcional: ancho máximo
            margin_top="1.5rem",
            position="fixed", top="50%", left="50%", transform="translate(-50%, -50%)",
        ),
        rx.text(""),
        padding_left="1rem", spacing="3",
    )
