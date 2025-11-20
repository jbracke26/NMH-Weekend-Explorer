import reflex as rx
from app.state import State


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
            rx.text(
                "This list is coming from activities.json. "
                "For the demo the filter controls are static."
            ),
            rx.hstack(
                rx.input(placeholder="Search activities...", width="40%"),
                rx.select(
                    ["All", "Outdoor", "Food", "Shopping", "Sports", "Other"],
                    placeholder="Category",
                    width="20%",
                ),
                rx.select(
                    ["Any", "5 min", "15 min", "30 min"],
                    placeholder="Distance",
                    width="20%",
                ),
            ),
            rx.grid(
                rx.foreach(ActivityState.activities, activity_card),
                columns=[1, 2, 3],
                spacing="4",
            ),
            rx.link(
                rx.button("Create Activity"),
                href="/create",
                align_self="flex-start",
                margin_top="4",
            ),
            padding="8",
            max_width="1000px",
            margin_x="auto",
        ),
    )
