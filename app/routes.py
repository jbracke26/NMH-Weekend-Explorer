import reflex as rx
from app.pages import home


def register_routes(app: rx.App):
    """アプリのページルーティングを登録。Googleログインはポップアップで処理するのでコールバックページは不要。"""
    app.add_page(home.index, route="/")
