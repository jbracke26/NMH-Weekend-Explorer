import reflex as rx
from app.state import State
from app.config import Config
from reflex_google_auth import google_login, google_oauth_provider


# Config を通して .env を読み込んだ上で client_id を取得
_config = Config()
GOOGLE_CLIENT_ID = _config.GOOGLE_CLIENT_ID or ""


def index():
    """シンプルなホームページ。Googleログインの前後だけを扱う。"""
    return rx.container(
        rx.cond(
            State.is_authenticated,
            # ログイン済みビュー
            rx.vstack(
                rx.heading("Weekend Explorer", size="9", margin_bottom="2"),
                rx.divider(margin_bottom="6"),
                rx.cond(
                    State.current_user_picture != "",
                    rx.image(
                        src=State.current_user_picture,
                        alt="Profile Picture",
                        width="80px",
                        height="80px",
                        border_radius="50%",
                        margin_bottom="4",
                    ),
                ),
                rx.heading(
                    f"Welcome, {State.current_user_name}!",
                    size="8",
                    margin_bottom="2",
                ),
                rx.text(
                    f"Logged in as: {State.current_user_email}",
                    size="4",
                    color="gray",
                    margin_bottom="6",
                ),
                rx.button(
                    "Logout",
                    on_click=State.logout,
                    size="3",
                    color_scheme="red",
                    variant="outline",
                ),
                rx.cond(
                    State.message != "",
                    rx.callout(
                        State.message,
                        icon="info",
                        color_scheme=State.message_type,
                        width="100%",
                        margin_top="4",
                    ),
                ),
                spacing="3",
                width="100%",
                align="center",
                padding="8",
            ),
            # 未ログインビュー
            rx.vstack(
                rx.heading("Weekend Explorer", size="9", margin_bottom="2"),
                rx.text(
                    "Welcome! Please log in with your Google account to continue.",
                    size="5",
                    color="gray",
                    margin_bottom="6",
                ),
                google_oauth_provider(
                    google_login(
                        on_success=State.on_google_login_success,
                    ),
                    client_id=GOOGLE_CLIENT_ID,
                ),
                rx.cond(
                    State.message != "",
                    rx.callout(
                        State.message,
                        icon="info",
                        color_scheme=State.message_type,
                        width="100%",
                        margin_top="4",
                    ),
                ),
                spacing="4",
                align="center",
                padding="8",
            ),
        ),
        max_width="800px",
        padding="6",
        center_content=True,
    )
