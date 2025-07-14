import reflex as rx
from BookWorms.state.auth_state import AuthState
from BookWorms.models.post_model import Post
from BookWorms.views.navbar import navbar


class NewPostState(AuthState):
    title: str = ""
    text: str = ""
    error: str = ""
    max_length: int = 560

    def set_title(self, value: str):
        self.title = value[:100]  # Optional: limit title length

    def set_text(self, value: str):
        self.text = value[:self.max_length]

    def cancel(self):
        self.title = ""
        self.text = ""
        self.error = ""
        return rx.redirect("/feed")

    def publish(self):
        if not self.title.strip() or not self.text.strip():
            self.error = "El título y el texto no pueden estar vacíos."
            return
        if len(self.text) > self.max_length:
            self.error = f"El texto no puede superar los {self.max_length} caracteres."
            return
        user_id = self.current_user_id
        try:
            user_id = int(user_id)
        except Exception:
            self.error = f"No se pudo identificar el usuario. Valor: {user_id}"
            return rx.redirect("/login")
        success = Post.create_post(self.title.strip(), self.text.strip(), user_id)
        if not success:
            self.error = "Error al publicar. Intenta de nuevo."
            return
        self.title = ""
        self.text = ""
        self.error = ""
        return rx.redirect("/feed")


def new_post_view() -> rx.Component:
    # Redirect to login if not logged in
    return rx.cond(
        AuthState.is_logged_in,
        rx.center(
            rx.vstack(
                rx.heading("Nuevo Posteo", size="6"),
                rx.input(
                    placeholder="Título",
                    value=NewPostState.title,
                    on_change=NewPostState.set_title,
                    width="100%",
                    max_width="400px",
                ),
                rx.input(
                    placeholder="¿Qué estás leyendo o pensando?",
                    value=NewPostState.text,
                    on_change=NewPostState.set_text,
                    width="100%",
                    max_width="400px",
                    type_="textarea",
                    rows=8,
                    max_length=NewPostState.max_length,
                ),
                rx.text(
                    NewPostState.text.length().to(str) + f"/{NewPostState.max_length} caracteres",
                    font_size="1",
                    color="gray"
                ),
                rx.text(NewPostState.error, color="red"),
                rx.hstack(
                    rx.button("Cancelar", color_scheme="gray", on_click=NewPostState.cancel),
                    rx.button("Publicar", color_scheme="blue", on_click=NewPostState.publish),
                ),
                spacing="4",
                width="100%",
                max_width="400px",
                padding="2rem",
                border_radius="xl",
                box_shadow="md",
                bg="var(--chakra-colors-chakra-body-bg)",
            ),
            min_height="100vh"
        ),
        rx.script("window.location.href = '/login'")
    ) 