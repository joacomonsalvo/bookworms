import reflex as rx
from BookWorms.state.auth_state import AuthState
from BookWorms.state.comments_state import CommentsState
from BookWorms.views.navbar import navbar


def post_card(post: dict) -> rx.Component:
    return rx.card(
        rx.vstack(
            rx.hstack(
                rx.heading(post["titulo"], size="4"),
                rx.spacer(),
                rx.text(post["fecha"], font_size="2", color="gray"),
            ),
        ),
        padding="1rem",
        margin_y="1rem",
        width="100%",
        box_shadow="md",
        border_radius="xl"
    )


def comment_item(comment: dict) -> rx.Component:
    """Componente para mostrar un comentario individual"""
    def handle_delete(comment_id: int):
        return CommentsState.delete_comment(comment_id)
    
    # Convert comment_id to string for comparison
    commenter_id = str(comment.get("commenter_id", ""))
    
    return rx.box(
        rx.hstack(
            rx.vstack(
                rx.text(comment.get("author", "Usuario desconocido"), font_weight="bold"),
                rx.text(comment.get("comentario", "")),
                align_items="start",
                width="100%"
            ),
            rx.spacer(),
            rx.cond(
                (AuthState.is_logged_in) & (AuthState.current_user_id.to(str) == commenter_id),
                rx.button(
                    "🗑️",
                    size="1",
                    variant="ghost",
                    on_click=lambda: handle_delete(comment["id"]),
                ),
                None
            ),
            width="100%",
            padding="0.5rem",
            border_bottom="1px solid #eee",
        ),
        width="100%"
    )


def comments_view() -> rx.Component:
    """Vista principal de comentarios"""
    
    def render_content():
        """Renderiza el contenido principal de la vista de comentarios"""
        return rx.vstack(
            navbar(),
            rx.hstack(
                rx.link(
                    rx.button(
                        rx.icon(tag="arrow_big_left"),
                        variant="ghost"
                    ),
                    href="/feed"
                ),
                rx.heading("Comentarios", size="6"),
                width="100%",
                padding_bottom="1em",
                border_bottom="1px solid #e2e8f0"
            ),
            
            # Mostrar la publicación
            rx.box(
                rx.cond(
                    CommentsState.post,
                    post_card(CommentsState.post),
                    rx.box(
                        rx.spinner(),
                        rx.text("Cargando publicación..."),
                        text_align="center",
                        width="100%"
                    )
                ),
                width="100%",
                max_width="800px",
                padding_x="1rem"
            ),
            
            # Formulario para agregar comentario
            rx.cond(
                AuthState.is_logged_in,
                rx.vstack(
                    rx.text("Agregar comentario", font_weight="bold"),
                    rx.hstack(
                        rx.input(
                            placeholder="Escribe tu comentario...",
                            value=CommentsState.comment_text,
                            on_change=CommentsState.set_comment_text,
                            flex=1,
                            is_disabled=CommentsState.is_loading
                        ),
                        rx.button(
                            "Comentar",
                            on_click=CommentsState.add_comment,
                            is_loading=CommentsState.is_loading,
                            is_disabled=CommentsState.is_loading | (CommentsState.comment_text == "")
                        ),
                        width="100%"
                    ),
                    width="100%",
                    padding_top="1em"
                ),
                rx.box(
                    rx.link(
                        "Inicia sesión para comentar",
                        href="/login",
                        color="blue.500",
                        text_decoration="underline"
                    ),
                    padding_y="1em"
                )
            ),
            
            # Lista de comentarios
            rx.box(
                rx.vstack(
                    rx.cond(
                        CommentsState.is_loading & (CommentsState.comments.length() == 0),
                        rx.vstack(
                            rx.spinner(),
                            rx.text("Cargando comentarios..."),
                            spacing="2"
                        ),
                        rx.cond(
                            CommentsState.comments.length() > 0,
                            rx.foreach(CommentsState.comments, comment_item),
                            rx.text("No hay comentarios aún. ¡Sé el primero en comentar!", color="gray")
                        )
                    ),
                    width="100%",
                    align_items="start"
                ),
                width="100%",
                max_width="800px",
                padding_x="1rem"
            ),
            
            padding_bottom="2rem",
            min_height="100vh",
            spacing="4"
        )
    
    # Verificar autenticación y renderizar contenido
    return rx.fragment(
        rx.cond(
            AuthState.is_logged_in,
            render_content(),
            rx.script("window.location.href = '/login'")
        )
    )


def comments_page() -> rx.Component:
    """Página de comentarios que incluye el estado de autenticación"""
    return rx.box(
        comments_view(),
        on_mount=[
            AuthState.load_auth_from_storage,
            lambda: CommentsState.load_comments()
        ],
    )
