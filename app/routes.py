import reflex as rx
from app.pages import home


def register_routes(app: rx.App):
    """Register app page routes. Google login is handled via popup, so callback page is not needed."""
    app.add_page(home.index, route="/")
