import reflex as rx
from app.states.state import State
from reflex_google_auth import google_login, google_oauth_provider
from app.config import Config
from app.design import COLORS

_config = Config()
GOOGLE_CLIENT_ID = _config.GOOGLE_CLIENT_ID or ""


def header() -> rx.Component:
    return rx.hstack(
        rx.link(
            rx.heading("Weekend Explorer", size="5"),
            href="/",
            text_decoration="none",
            _hover={"opacity": "0.8"},
        ),
        rx.spacer(),
        rx.hstack(
            rx.link("Home", href="/", size="3", _hover={"opacity": "0.7"}),
            rx.link("Explore", href="/explore", size="3", _hover={"opacity": "0.7"}),
            rx.link("Map", href="/map", size="3", _hover={"opacity": "0.7"}),
            rx.link("Create", href="/create", size="3", _hover={"opacity": "0.7"}),
            rx.link(
                "My Activities",
                href="/my-activities",
                size="3",
                _hover={"opacity": "0.7"},
            ),
            rx.cond(
                State.is_admin,
                rx.link(
                    "Admin",
                    href="/admin",
                    size="3",
                    color=COLORS["primary"],
                    _hover={"opacity": "0.7"},
                ),
                rx.fragment(),
            ),
            spacing="5",
        ),
        rx.spacer(),
        rx.box(
            rx.cond(
                State.is_authenticated,
                rx.hstack(
                    rx.text(State.current_user_name, size="3"),
                    rx.avatar(src=State.current_user_picture, size="2", radius="full"),
                    rx.button(
                        "Logout", on_click=State.logout, size="2", variant="soft"
                    ),
                    spacing="3",
                    align="center",
                ),
                rx.cond(
                    ~State.hide_header_login,
                    rx.vstack(
                        rx.hstack(
                            rx.text("Student", size="2"),
                            google_oauth_provider(
                                google_login(
                                    on_success=State.on_student_login_success,
                                ),
                                client_id=GOOGLE_CLIENT_ID,
                            ),
                            align="center",
                            spacing="2",
                        ),
                        rx.hstack(
                            rx.text("Teacher", size="2"),
                            google_oauth_provider(
                                google_login(
                                    on_success=State.on_teacher_login_success,
                                ),
                                client_id=GOOGLE_CLIENT_ID,
                            ),
                            align="center",
                            spacing="2",
                        ),
                        spacing="2",
                        align="start",
                    ),
                    rx.box(),
                ),
            ),
            min_width="200px",
            display="flex",
            justify_content="flex-end",
        ),
        width="100%",
        padding="4",
        border_bottom=f"1px solid {COLORS['border']}",
        align="center",
        position="sticky",
        top="0",
        z_index="100",
        background=COLORS["bg"],
    )


def layout(content: rx.Component, **kwargs) -> rx.Component:
    return rx.vstack(
        header(),
        # Message display
        rx.cond(
            State.message != "",
            rx.box(
                rx.hstack(
                    rx.text(
                        State.message,
                        size="2",
                        color=rx.cond(
                            State.message_type == "error",
                            "red",
                            rx.cond(
                                State.message_type == "success",
                                "green",
                                "blue"
                            )
                        ),
                        weight="medium",
                    ),
                    rx.button(
                        "×",
                        on_click=lambda: State.set_message(""),
                        size="1",
                        variant="ghost",
                        color="gray",
                    ),
                    justify="between",
                    align="center",
                    width="100%",
                ),
                width="100%",
                max_width="1200px",
                margin="0 auto",
                padding="3",
                background=rx.cond(
                    State.message_type == "error",
                    "var(--red-3)",
                    rx.cond(
                        State.message_type == "success",
                        "var(--green-3)",
                        "var(--blue-3)"
                    )
                ),
                border_radius="6px",
                margin_top="2",
            ),
        ),
        rx.box(
            content,
            width="100%",
            padding="4",
            max_width="1200px",
            margin="0 auto",
        ),
        width="100%",
        min_height="100vh",
        background=COLORS["bg_secondary"],
        **kwargs,
    )
