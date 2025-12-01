import reflex as rx
from app.state import State


def my_activity_card(activity: dict) -> rx.Component:
    return rx.link(
        rx.card(
            rx.vstack(
                rx.heading(activity["title"]),
                rx.text(activity.get("time", "")),
                rx.text(activity.get("location", "")),
                align="start",
                spacing="2",
            ),
            style={"cursor": "pointer", "_hover": {"box_shadow": "lg"}},
        ),
        href=f"/activity/{activity['id']}",
        text_decoration="none",
    )


def my_activities() -> rx.Component:
    return rx.box(
        rx.vstack(
            rx.heading("My Activities"),
            rx.text("Activities you have created."),
            rx.grid(
                rx.foreach(State.my_activities_list, my_activity_card),
                columns="2",
                spacing="4",
            ),
            padding="8",
            max_width="1000px",
            margin_x="auto",
        )
    )
