import reflex as rx

config = rx.Config(
    app_name="app",
)

class AppConfig(rx.Config):
    pass

config = AppConfig(
    app_name = "app",
    db_url="sqlite:///reflex.db",
)

