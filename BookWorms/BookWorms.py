# app.py

import reflex as rx
from rxconfig import config

from BookWorms.views.login_view import login_view
from BookWorms.views.signup_view import signup_view
from BookWorms.views.feed_view import feed_page


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
app.add_page(index, route="/", title="Home")
app.add_page(signup_view, route="/signup", title="Sign Up")
app.add_page(login_view, route="/login", title="Login")
app.add_page(feed_page, route="/feed", title="Feed")
