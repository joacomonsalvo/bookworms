import reflex as rx

config = rx.Config(
    app_name="BookWorms",
    plugins=[
        rx.plugins.SitemapPlugin(),
        rx.plugins.TailwindV4Plugin(),
    ],
    pages={
        "/":       "BookWorms.views.feed_view.feed_page",
        "/feed":   "BookWorms.views.feed_view.feed_page",
        "/search": "BookWorms.views.search_result_view.search_result_page",
    },
)
