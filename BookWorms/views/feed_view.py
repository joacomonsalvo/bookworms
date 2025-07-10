import reflex as rx
from BookWorms.state.auth_state import AuthState
from BookWorms.models.post_model import Post  # Deberás crear este archivo/modelo


def navbar() -> rx.Component:
    return rx.hstack(
        rx.text("BookWorms Feed", font_size="8", font_weight="bold"),
        rx.spacer(),
        rx.input(placeholder="Buscar...", width="200px"),
        rx.button("Buscar", color_scheme="blue"),
        rx.link("Amigos", href="/friends", ml="4"),
        rx.link("Listas", href="/lists", ml="4"),
        rx.link("Nuevo Posteo", href="/new_post", ml="4"),
        rx.link("Ajustes", href="/settings", ml="4"),
        rx.button("🚪 Cerrar Sesión", color_scheme="red", on_click=AuthState.open_logout_dialog, ml="4"),
        padding="1rem",
        border_bottom="1px solid #ccc",
        align="center",
        width="100%",
    )


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
                rx.button("👍 Like", size="2"),
                rx.button("💬 Comentar", size="2"),
                rx.spacer(),
                rx.text(f"Autor: {post['author']}", font_size="1", color="gray"),
                rx.cond(
                    AuthState.current_username == post["author"],
                    rx.button("🗑️ Eliminar", size="2", color_scheme="red", on_click=FeedState.show_delete_dialog(post["id"])),
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


class FeedState(rx.State):
    posts: list[dict] = []
    show_delete_confirm: bool = False
    post_to_delete: int | None = None

    def load_posts(self):
        self.posts = Post.get_all_posts()

    def show_delete_dialog(self, post_id: int):
        """Show delete confirmation dialog"""
        self.post_to_delete = post_id
        self.show_delete_confirm = True

    def confirm_delete_with_user_id(self, user_id: int):
        """Confirm and delete the post with user ID"""
        if self.post_to_delete is not None:
            success = Post.delete_post(self.post_to_delete, user_id)
            if success:
                self.load_posts()  # Reload posts after deletion
        self.show_delete_confirm = False
        self.post_to_delete = None

    def confirm_delete(self):
        """Confirm and delete the post"""
        if self.post_to_delete is not None:
            # Get the current user ID from AuthState
            current_user_id = AuthState.get_current_user_id()
            if current_user_id is not None:
                success = Post.delete_post(self.post_to_delete, current_user_id)
                if success:
                    self.load_posts()  # Reload posts after deletion
        self.show_delete_confirm = False
        self.post_to_delete = None

    def cancel_delete(self):
        """Cancel delete operation"""
        self.show_delete_confirm = False
        self.post_to_delete = None

    def get_current_user_id(self) -> int | None:
        """Get the current user ID from AuthState"""
        return AuthState.current_user_id


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
                    rx.text("¿Estás seguro de que quieres eliminar esta publicación? Esta acción no se puede deshacer."),
                    rx.hstack(
                        rx.button("Cancelar", on_click=FeedState.cancel_delete),
                        rx.button("Eliminar", color_scheme="red", on_click=FeedState.confirm_delete_with_user_id(AuthState.current_user_id), ml="3"),
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




