import reflex as rx
from app.states.state import State
from app.layout import layout
from app.config import Config
from reflex_google_auth import google_login, google_oauth_provider

_config = Config()
GOOGLE_CLIENT_ID = _config.GOOGLE_CLIENT_ID or ""


def create_activity() -> rx.Component:
    return layout(
        rx.cond(
            State.is_authenticated,
            rx.center(
                rx.card(
                    rx.vstack(
                        rx.heading("Create New Activity", size="6", margin_bottom="4"),
                        rx.vstack(
                            rx.text(
                                "Title", weight="bold", size="2", margin_bottom="1"
                            ),
                            rx.input(
                                placeholder="e.g., Northampton Dinner Trip",
                                value=State.activity_title,
                                on_change=State.set_activity_title,
                                width="100%",
                            ),
                            width="100%",
                            align_items="start",
                        ),
                        rx.vstack(
                            rx.text(
                                "Description",
                                weight="bold",
                                size="2",
                                margin_bottom="1",
                            ),
                            rx.text_area(
                                placeholder="Describe what you'll be doing...",
                                value=State.activity_description,
                                on_change=State.set_activity_description,
                                min_height="120px",
                                width="100%",
                            ),
                            width="100%",
                            align_items="start",
                        ),
                        rx.hstack(
                            rx.vstack(
                                rx.text(
                                    "Category",
                                    weight="bold",
                                    size="2",
                                    margin_bottom="1",
                                ),
                                rx.select(
                                    ["Outdoor", "Food", "Shopping", "Sports", "Other"],
                                    placeholder="Select Category",
                                    value=State.activity_category,
                                    on_change=State.set_activity_category,
                                    width="100%",
                                ),
                                width="100%",
                                align_items="start",
                            ),
                            rx.vstack(
                                rx.text(
                                    "Max Participants",
                                    weight="bold",
                                    size="2",
                                    margin_bottom="1",
                                ),
                                rx.input(
                                    placeholder="Optional",
                                    value=State.activity_max_participants,
                                    on_change=State.set_activity_max_participants,
                                    width="100%",
                                ),
                                width="100%",
                                align_items="start",
                            ),
                            width="100%",
                            spacing="4",
                        ),
                        rx.vstack(
                            rx.text(
                                "Location", weight="bold", size="2", margin_bottom="1"
                            ),
                            rx.input(
                                placeholder="e.g., Alumni Hall",
                                value=State.activity_location,
                                on_change=State.set_activity_location,
                                width="100%",
                            ),
                            width="100%",
                            align_items="start",
                        ),
                        rx.vstack(
                            rx.text("Log Location on Map?", weight="bold", size="2", margin_bottom="1"),
                            rx.switch(
                                is_checked=State.activity_log_location,
                                on_change=State.set_activity_log_location,
                            ),
                            width="100%",
                            align_items="start",
                        ),
                        rx.cond(
                            State.activity_log_location,
                            rx.hstack(
                                rx.vstack(
                                    rx.text("Latitude", weight="bold", size="2", margin_bottom="1"),
                                    rx.input(
                                        placeholder="e.g., 42.667144",
                                        value=State.activity_latitude,
                                        on_change=State.set_activity_latitude,
                                        width="100%",
                                    ),
                                    width="100%",
                                    align_items="start",
                                ),
                                rx.vstack(
                                    rx.text("Longitude", weight="bold", size="2", margin_bottom="1"),
                                    rx.input(
                                        placeholder="e.g., -72.481655",
                                        value=State.activity_longitude,
                                        on_change=State.set_activity_longitude,
                                        width="100%",
                                    ),
                                    width="100%",
                                    align_items="start",
                                ),
                                spacing="4",
                                width="100%",
                            ),
                        ),
                        rx.vstack(
                            rx.text(
                                "Distance", weight="bold", size="2", margin_bottom="1"
                            ),
                            rx.input(
                                placeholder="e.g., 15 min walk",
                                value=State.activity_distance,
                                on_change=State.set_activity_distance,
                                width="100%",
                            ),
                            width="100%",
                            align_items="start",
                        ),
                        rx.hstack(
                            rx.vstack(
                                rx.text(
                                    "Date", weight="bold", size="2", margin_bottom="1"
                                ),
                                rx.input(
                                    type_="date",
                                    placeholder="YYYY-MM-DD",
                                    value=State.activity_date,
                                    on_change=State.set_activity_date,
                                    width="100%",
                                ),
                                width="100%",
                                align_items="start",
                            ),
                            rx.vstack(
                                rx.text(
                                    "Time", weight="bold", size="2", margin_bottom="1"
                                ),
                                rx.input(
                                    type_="time",
                                    placeholder="HH:MM",
                                    value=State.activity_time,
                                    on_change=State.set_activity_time,
                                    width="100%",
                                ),
                                width="100%",
                                align_items="start",
                            ),
                            spacing="4",
                            width="100%",
                        ),
                        rx.button(
                            "Create Activity",
                            on_click=State.create_activity,
                            size="3",
                            width="100%",
                            color_scheme="teal",
                            margin_top="6",
                        ),
                        spacing="4",
                        width="100%",
                    ),
                    width="100%",
                    max_width="600px",
                    padding="6",
                    box_shadow="lg",
                ),
                padding_y="8",
                width="100%",
            ),
            # Login Prompt if not authenticated
            rx.center(
                rx.vstack(
                    rx.heading("Please Login", size="6"),
                    rx.text("You need to be logged in to create an activity."),
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
        on_mount=State.set_hide_header_login(True),
        on_unmount=State.set_hide_header_login(False),
    )
