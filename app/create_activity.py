import reflex as rx
from app.state import ActivityState


def create_activity() -> rx.Component:
    s = ActivityState
    return rx.box(
        rx.vstack(
            rx.heading("Create a New Activity"),
            rx.text("This writes directly into activities.json."),
            rx.input(
                placeholder="Title",
                value=s.new_title,
                on_change=s.set_new_title,
            ),
            rx.textarea(
                placeholder="Short description",
                value=s.new_description,
                on_change=s.set_new_description,
                rows="3",
            ),
            rx.hstack(
                rx.select(
                    ["Outdoor", "Food", "Shopping", "Sports", "Other"],
                    value=s.new_category,
                    on_change=s.set_new_category,
                    label="Category",
                    width="33%",
                ),
                rx.input(
                    placeholder="Location",
                    value=s.new_location,
                    on_change=s.set_new_location,
                    width="33%",
                ),
                rx.input(
                    placeholder="Distance (for example 10 min walk)",
                    value=s.new_distance,
                    on_change=s.set_new_distance,
                    width="33%",
                ),
            ),
            rx.hstack(
                rx.input(
                    placeholder="Time (for example Saturday 3pm)",
                    value=s.new_time,
                    on_change=s.set_new_time,
                    width="50%",
                ),
                rx.number_input(
                    value=s.new_max_participants,
                    on_change=lambda v: s.set_new_max_participants(int(v or 0)),
                    min_=0,
                    label="Max participants",
                    width="50%",
                ),
            ),
            rx.button(
                "Save activity",
                color_scheme="green",
                on_click=s.add_activity,
            ),
            rx.link(
                rx.button("Back to Explore", variant="soft"),
                href="/explore",
            ),
            padding="8",
            max_width="800px",
            margin_x="auto",
        )
    )
