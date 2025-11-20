import reflex as rx
from app.state import State
from app.config import Config

config = Config()

def get_google_auth_url():
    google_auth_url = "https://accounts.google.com/o/oauth2/v2/auth"
    params = {
        "client_id": config.GOOGLE_CLIENT_ID,
        "redirect_uri": config.GOOGLE_REDIRECT_URI,
        "response_type": "code",
        "scope": "openid email profile",
        "access_type": "online",
    }
    query_string = "&".join([f"{k}={v}" for k, v in params.items()])
    return f"{google_auth_url}?{query_string}"

def index():
    return rx.container(
        rx.heading("Weekend Explorer", size="9", margin_bottom="4"),
        rx.cond(
            State.is_authenticated,
            rx.vstack(
                rx.heading(f"Welcome, {State.current_user_name}!", size="7", margin_bottom="4"),
                rx.cond(
                    State.current_user_picture != "",
                    rx.image(
                        src=State.current_user_picture,
                        alt="Profile Picture",
                        width="100px",
                        height="100px",
                        border_radius="50%",
                    ),
                ),
                rx.text(f"Email: {State.current_user_email}", size="4"),
                rx.cond(
                    State.is_admin,
                    rx.badge("Admin", color_scheme="red"),
                ),
                rx.spacer(height="4"),
                rx.button(
                    "Logout",
                    on_click=State.logout,
                    size="3",
                    color_scheme="red",
                ),
                rx.cond(
                    State.message != "",
                    rx.callout(
                        State.message,
                        icon="info",
                        color_scheme=State.message_type,
                        width="100%",
                    ),
                ),
                spacing="4",
                width="100%",
                align="center",
            ),
            rx.vstack(
                rx.text("Please log in with your Google account to continue.", size="5", color="gray", margin_bottom="4"),
                rx.link(
                    rx.button(
                        "Login with Google",
                        size="3",
                        color_scheme="blue",
                    ),
                    href=get_google_auth_url(),
                    is_external=True,
                ),
                rx.cond(
                    State.message != "",
                    rx.callout(
                        State.message,
                        icon="info",
                        color_scheme=State.message_type,
                        width="100%",
                    ),
                ),
                spacing="4",
                align="center",
            ),
        ),
        max_width="800px",
        padding="6",
        center_content=True,
    )
