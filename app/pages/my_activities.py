import reflex as rx
from app.states.state import State
from app.layout import layout
from app.config import Config
from reflex_google_auth import google_login, google_oauth_provider

_config = Config()
GOOGLE_CLIENT_ID = _config.GOOGLE_CLIENT_ID or ""


def my_activity_card(activity: dict) -> rx.Component:
    return rx.link(
        rx.card(
            rx.vstack(
                rx.heading(activity["title"], size="4"),
                rx.text(
                    activity["description"],
                    size="2",
                    no_of_lines=2,
                ),
                rx.hstack(
                    rx.badge(
                        rx.cond(
                            activity["creator_id"] == State.current_user_id,
                            "Created",
                            "Joined",
                        ),
                        color_scheme=rx.cond(
                            activity["creator_id"] == State.current_user_id,
                            "green",
                            "blue",
                        ),
                    ),
                    rx.spacer(),
                    rx.text(
                        f"{activity.get('date', '')} {activity.get('time', '')}",
                        size="2",
                        color="gray.500",
                    ),
                    width="100%",
                ),
                align="start",
                spacing="2",
            ),
            width="100%",
            _hover={"box_shadow": "lg"},
        ),
        href=f"/activity/{activity['id']}",
        text_decoration="none",
        width="100%",
    )


def my_activities() -> rx.Component:
    return layout(
        rx.cond(
            State.is_authenticated,
            rx.vstack(
                rx.heading("My Activities", size="6", margin_bottom="4"),
                rx.cond(
                    State.my_activities_list,
                    rx.grid(
                        rx.foreach(
                            State.my_activities_list,
                            my_activity_card,
                        ),
                        columns="3",
                        spacing="4",
                        width="100%",
                    ),
                    rx.text("You haven't created or joined any activities yet."),
                ),
                width="100%",
                spacing="4",
            ),
            # Login Prompt if not authenticated
            rx.center(
                rx.vstack(
                    rx.heading("Please Login", size="6"),
                    rx.text("You need to be logged in to view your activities."),
                    rx.cond(
                        GOOGLE_CLIENT_ID != "",
                        google_oauth_provider(
                            google_login(
                                on_success=State.on_google_login_success,
                            ),
                            client_id=GOOGLE_CLIENT_ID,
                        ),
                        rx.text("Google OAuth not configured.", color="red"),
                    ),
                    spacing="4",
                    align="center",
                ),
                padding="10",
                width="100%",
            ),
        ),
        on_mount=[State.load_activities, State.set_hide_header_login(True)],
        on_unmount=State.set_hide_header_login(False),
    )
