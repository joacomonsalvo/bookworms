import reflex as rx
from BookWorms.state.auth_state import AuthState
from BookWorms.state.feed_state import FeedState
from BookWorms.views.navbar import navbar


def post_card(post: dict) -> rx.Component:
    return rx.card(
        rx.vstack(
            rx.hstack(
                rx.heading(post["titulo"], size="4"),
                rx.spacer(),
                rx.text(post["fecha"], font_size="2", color="gray"),
            ),
            rx.text(post["texto"]),
            rx.hstack(
                rx.button(f"👍 {post['likes']} Likes", size="2", on_click=FeedState.like(post_id=post["id"])),
                rx.link(
                    rx.button("💬 Comentar", size="2"),
                    href=f"/comments/{post['id']}"
                ),
                rx.spacer(),
                rx.text(f"Autor: {post['author']}", font_size="1", color="gray"),
                rx.cond(
                    AuthState.current_username == post["author"],
                    rx.button("🗑️ Eliminar", size="2", color_scheme="red",
                              on_click=FeedState.show_delete_dialog(post_id=post["id"])),
                    rx.text("")
                ),
            ),
        ),
        padding="1rem",
        margin_y="1rem",
        width="100%",
        box_shadow="md",
        border_radius="xl"
    )


def render_result_card(item) -> rx.Component:
    # Asegurar que `data` es un dict válido
    data = getattr(item, "_var_data", item)
    if not isinstance(data, dict):
        data = {}

    if "titulo" in data:
        # Es un libro
        return rx.card(
            rx.vstack(
                rx.heading(data.get("titulo", "Sin título"), size="4"),
                rx.text(data.get("sinopsis", "Sinopsis no disponible")),
                rx.button("Agregar a mi lista", disabled=True)
            ),
            margin_y="1rem"
        )
    elif "user" in data:
        # Es un usuario
        return rx.card(
            rx.vstack(
                rx.heading(data.get("user", "Usuario desconocido"), size="4"),
                rx.text(data.get("email", "Email no disponible")),
            ),
            margin_y="1rem"
        )
    else:
        # Por si llega un dato inesperado
        return rx.text("Elemento no reconocido")


def feed_view() -> rx.Component:
    return rx.cond(
        AuthState.is_logged_in,
        rx.vstack(
            navbar(),
            rx.heading("Feed", size="6", padding_top="1rem"),
            rx.foreach(FeedState.posts, post_card),
            padding="2rem",
            on_mount=FeedState.load_posts
        ),
        rx.script("window.location.href = '/login'")
    )


def feed_page() -> rx.Component:
    return rx.box(
        feed_view(),
        delete_confirmation_dialog(),
        logout_confirmation_dialog(),
        on_mount=AuthState.load_auth_from_storage,
    )


def delete_confirmation_dialog() -> rx.Component:
    return rx.cond(
        FeedState.show_delete_confirm,
        rx.box(
            rx.box(
                rx.vstack(
                    rx.heading("Confirmar eliminación", size="4"),
                    rx.text(
                        "¿Estás seguro de que quieres eliminar esta publicación? Esta acción no se puede deshacer."),
                    rx.hstack(
                        rx.button("Cancelar", on_click=FeedState.cancel_delete),
                        rx.button("Eliminar", color_scheme="red",
                                  on_click=FeedState.confirm_delete_with_user_id(AuthState.current_user_id), ml="3"),
                    ),
                    spacing="4",
                    padding="2rem",
                    bg="var(--chakra-colors-chakra-body-bg)",
                    color="var(--chakra-colors-chakra-body-text)",
                    border_radius="xl",
                    box_shadow="2xl",
                    max_width="400px",
                    border="1px solid var(--chakra-colors-chakra-border-color)",
                ),
                position="fixed",
                top="50%",
                left="50%",
                transform="translate(-50%, -50%)",
                z_index="1000",
            ),
            position="fixed",
            top="0",
            left="0",
            right="0",
            bottom="0",
            bg="rgba(0, 0, 0, 0.6)",
            z_index="999",
            on_click=FeedState.cancel_delete,
        ),
        rx.text("")
    )


def logout_confirmation_dialog() -> rx.Component:
    return rx.cond(
        AuthState.show_logout_confirm,
        rx.box(
            rx.box(
                rx.vstack(
                    rx.heading("Confirmar cierre de sesión", size="4"),
                    rx.text("¿Estás seguro de que quieres cerrar sesión?"),
                    rx.hstack(
                        rx.button("Cancelar", on_click=AuthState.cancel_logout),
                        rx.button("Cerrar Sesión", color_scheme="red", on_click=AuthState.confirm_logout, ml="3"),
                    ),
                    spacing="4",
                    padding="2rem",
                    bg="var(--chakra-colors-chakra-body-bg)",
                    color="var(--chakra-colors-chakra-body-text)",
                    border_radius="xl",
                    box_shadow="2xl",
                    max_width="400px",
                    border="1px solid var(--chakra-colors-chakra-border-color)",
                ),
                position="fixed",
                top="50%",
                left="50%",
                transform="translate(-50%, -50%)",
                z_index="1000",
            ),
            position="fixed",
            top="0",
            left="0",
            right="0",
            bottom="0",
            bg="rgba(0, 0, 0, 0.6)",
            z_index="999",
            on_click=AuthState.cancel_logout,
        ),
        rx.text("")
    )
