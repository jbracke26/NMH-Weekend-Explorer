import reflex as rx
from app.state import State


def create_activity() -> rx.Component:
    return rx.box(
        rx.vstack(
            rx.heading("Create Activity"),
            rx.input(
                placeholder="Title",
                value=State.activity_title,
                on_change=State.set_activity_title,
            ),
            rx.text_area(
                placeholder="Description",
                value=State.activity_description,
                on_change=State.set_activity_description,
                min_height="120px",
            ),
            rx.select(
                ["Outdoor", "Food", "Shopping", "Sports", "Other"],
                placeholder="Category",
                value=State.activity_category,
                on_change=State.set_activity_category,
                width="40%",
            ),
            rx.input(
                placeholder="Location",
                value=State.activity_location,
                on_change=State.set_activity_location,
            ),
            rx.input(
                placeholder="Distance, for example '15 min walk'",
                value=State.activity_distance,
                on_change=State.set_activity_distance,
            ),
            rx.hstack(
                rx.input(
                    type_="date",
                    value=State.activity_date,
                    on_change=State.set_activity_date,
                    width="50%",
                ),
                rx.input(
                    type_="time",
                    value=State.activity_time,
                    on_change=State.set_activity_time,
                    width="40%",
                ),
                spacing="4",
                width="100%",
            ),
            rx.input(
                placeholder="Max participants (optional)",
                value=State.activity_max_participants,
                on_change=State.set_activity_max_participants,
            ),
            rx.button(
                "Create activity",
                on_click=State.create_activity,
                margin_top="4",
            ),
            padding="8",
            max_width="800px",
            margin_x="auto",
        ),
    )
