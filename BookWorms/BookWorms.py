import reflex as rx

from BookWorms.views.login_view import login_view
from BookWorms.views.signup_view import signup_view
from BookWorms.views.feed_view import feed_page
from BookWorms.views.new_post_view import new_post_view
from BookWorms.views.comments_view import comments_page
from BookWorms.state.comments_state import CommentsState
from BookWorms.views.search_result_view import search_result_page
from BookWorms.views.amigos_view import amigos_view
from BookWorms.views.listas_view import listas_view
from BookWorms.views.ab_libro_view import ab_libros_view
from BookWorms.views.reportes_view import reportes_view


def index() -> rx.Component:
    """Basic landing page with links to auth pages."""
    return rx.center(
        rx.vstack(
            rx.heading("📚 BookWorms", size="9"),
            rx.text("Welcome to the BookWorms app."),
            rx.link(rx.button("Sign Up"), href="/signup"),
            rx.link(rx.button("Log In"), href="/login"),
            spacing="4",
        ),
        min_height="100vh"
    )


app = rx.App()
app.add_page(index, route="/", title="Home - BookWorms")
app.add_page(signup_view, route="/signup", title="Sign Up - BookWorms")
app.add_page(login_view, route="/login", title="Login - BookWorms")
app.add_page(feed_page, route="/feed", title="Feed - BookWorms")
app.add_page(new_post_view, route="/new_post", title="Nuevo Posteo - BookWorms")
app.add_page(search_result_page, route="/search", title="Resultado Busqueda - BookWorms")
app.add_page(listas_view, route="/listas", title="Listas - BookWorms")
app.add_page(amigos_view, route="/amigos", title="Amigos - BookWorms")
app.add_page(ab_libros_view, route="/ab_libro", title="AB Libro - BookWorms")
app.add_page(reportes_view, route="/reportes", title="Reportes - BookWorms")
# Add comments page with route parameter
app.add_page(
    comments_page, 
    route="/comments/[post_id]",
    title="Comentarios - BookWorms",
    on_load=CommentsState.load_comments
)
