import reflex as rx

config = rx.Config(
    app_name="BookWorms",
    plugins=[
        rx.plugins.SitemapPlugin(),
        rx.plugins.TailwindV4Plugin(),
    ],
)