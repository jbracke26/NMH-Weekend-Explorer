
import reflex as rx
from app.example_data import EXAMPLE_ACTIVITIES


def activity_card(activity: dict) -> rx.Component:
    return rx.link(
        rx.card(
            rx.vstack(
                rx.heading(activity["title"]),
                rx.badge(activity["category"], color_scheme="blue"),
                rx.text(activity["description"], color="gray", no_of_lines=2),
                rx.hstack(
                    rx.text(activity["location"]),
                    rx.text(activity["distance"]),
                ),
                align="start",
            ),
            style={"cursor": "pointer", "_hover": {"box_shadow": "lg"}},
        ),
        href=f"/activity/{activity['id']}",
        text_decoration="none",
    )


def explore() -> rx.Component:
    return rx.box(
        rx.vstack(
            rx.heading("Explore Activities"),
            rx.hstack(
                rx.input(placeholder="Search activities..."),
                rx.select(
                    ["All Categories", "Outdoor", "Food", "Arts", "Sports", "Other"],
                    placeholder="Category",
                ),
                rx.select(
                    ["Any Distance", "5 min", "15 min", "30 min"],
                    placeholder="Distance",
                ),
            ),
            rx.grid(
                rx.foreach(EXAMPLE_ACTIVITIES, activity_card),
                columns="3",
            ),
            padding="8",
        ),
    )
