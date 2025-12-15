import reflex as rx
from app.states.state import State
from app.layout import layout


def edit_activity() -> rx.Component:
    return layout(
        rx.cond(
            State.is_authenticated,
            rx.center(
                rx.card(
                    rx.vstack(
                        rx.heading("Edit Activity", size="6", margin_bottom="4"),
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
                        rx.hstack(
                            rx.link(
                                rx.button(
                                    "Cancel",
                                    variant="outline",
                                    size="3",
                                    width="100%",
                                ),
                                href=rx.cond(
                                    State.editing_activity_id,
                                    f"/activity/{State.editing_activity_id}",
                                    "/explore",
                                ),
                            ),
                            rx.button(
                                "Update Activity",
                                on_click=State.update_activity,
                                size="3",
                                width="100%",
                                color_scheme="teal",
                            ),
                            spacing="4",
                            width="100%",
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
            # Redirect to home if not authenticated
            rx.center(
                rx.vstack(
                    rx.heading("Please Login", size="6"),
                    rx.text("You need to be logged in to edit activities."),
                    rx.link(
                        rx.button("Back to Home"),
                        href="/",
                    ),
                    spacing="4",
                    align="center",
                ),
                padding="10",
                width="100%",
            ),
        ),
        on_mount=State.load_activity_for_edit,
    )
