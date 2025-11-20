import reflex as rx
from app.state import State
from app.routes import register_routes

app = rx.App()

register_routes(app)
