import reflex as rx
from app.state import State


def create_activity() -> rx.Component:
    return rx.box(
        rx.vstack(
            rx.heading("Create Activity"),
            rx.form(
                rx.vstack(
                    rx.input(
                        placeholder="Title",
                        value=State.activity_title,
                        on_change=State.set_activity_title,
                    ),
                    rx.text_area(
                        placeholder="Description",
                        value=State.activity_description,
                        on_change=State.set_activity_description,
                    ),
                    rx.select(
                        ["Other", "Outdoor", "Food", "Shopping", "Sports"],
                        placeholder="Category",
                        value=State.activity_category,
                        on_change=State.set_activity_category,
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
                            type="date",
                            placeholder="Date",
                            value=State.activity_date,
                            on_change=State.set_activity_date,
                        ),
                        rx.input(
                            type="time",
                            placeholder="Time",
                            value=State.activity_time,
                            on_change=State.set_activity_time,
                        ),
                    ),
                    rx.input(
                        placeholder="Max participants (optional)",
                        value=State.activity_max_participants,
                        on_change=State.set_activity_max_participants,
                    ),
                    rx.button("Create activity", type="submit"),
                    spacing="3",
                    align="stretch",
                ),
                on_submit=State.create_activity,
            ),
            padding="8",
            max_width="800px",
            margin_x="auto",
        ),
    )
