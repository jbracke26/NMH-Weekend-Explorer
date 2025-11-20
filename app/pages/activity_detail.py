import reflex as rx
from app.example_data import EXAMPLE_ACTIVITIES


def activity_detail() -> rx.Component:
    activity = EXAMPLE_ACTIVITIES[0]
    
    return rx.box(
        rx.vstack(
            rx.link(
                rx.button("← Back to Explore", variant="soft"),
                href="/explore",
            ),
            rx.hstack(
                rx.heading(activity["title"]),
                rx.badge(activity["category"], color_scheme="blue"),
                align="center",
            ),
            rx.vstack(
                rx.text(activity["description"]),
                rx.divider(),
                rx.hstack(
                    rx.text(f"{activity['location']}", weight="medium"),
                    rx.text(f"{activity['distance']}", weight="medium"),
                ),
                rx.text(f"Time: {activity['time']}", weight="medium"),
                rx.text(f"Host: {activity['host']}", weight="medium"),
                align="start",
                width="100%",
            ),
            rx.divider(),
            rx.heading("Participants"),
            rx.cond(
                len(activity["participants"]) > 0,
                rx.vstack(
                    rx.foreach(
                        activity["participants"],
                        lambda p: rx.text(f"• {p}"),
                    ),
                    align="start",
                ),
                rx.text("No participants yet", color="gray"),
            ),
            rx.divider(),
            rx.hstack(
                rx.button("Join Activity", color_scheme="green", disabled=True),
                rx.button("Edit", color_scheme="blue", disabled=True),
                rx.button("Delete", color_scheme="red", disabled=True),
            ),
            padding="8",
            max_width="800px",
        ),
    )
