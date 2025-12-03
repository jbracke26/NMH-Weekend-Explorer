import reflex as rx
from app.state import State


def my_activity_card(activity: dict) -> rx.Component:
    """Card for a single activity created by the current user."""
    return rx.card(
        rx.vstack(
            rx.link(
                rx.heading(activity.get("title", ""), size="4"),
                href=f"/activity/{activity['id']}",
                text_decoration="none",
            ),
            rx.text(activity.get("description", ""), no_of_lines=2),
            rx.text(activity.get("location", ""), color="gray"),
            rx.text(activity.get("time", ""), color="gray"),
            align="start",
            spacing="2",
        ),
        style={
            "cursor": "pointer",
            "_hover": {
                "box_shadow": "lg",
                "transform": "translateY(-2px)",
            },
            "transition": "all 0.15s ease",
        },
    )


def my_activities() -> rx.Component:
    """Page that lists only the current user's activities."""
    return rx.box(
        rx.vstack(
            rx.heading("My Activities"),
            rx.text("Activities you have created."),
            rx.grid(
                rx.foreach(State.my_activities_list, my_activity_card),
                columns={"base": "1", "md": "2"},
                spacing="4",
                width="100%",
            ),
            padding="8",
            max_width="1000px",
            margin_x="auto",
        ),
    )
