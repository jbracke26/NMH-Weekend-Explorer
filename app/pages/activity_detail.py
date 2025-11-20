import reflex as rx
from app.models import load_activities


def get_activity_by_id(activity_id: str):
    for a in load_activities():
        if str(a.id) == str(activity_id):
            return a
    return None


def activity_detail(id: str) -> rx.Component:
    """Detail page for a single activity."""
    activity = get_activity_by_id(id)

    if activity is None:
        return rx.box(
            rx.vstack(
                rx.link(
                    rx.button("← Back to Explore", variant="soft"),
                    href="/explore",
                ),
                rx.heading("Activity not found", color="red"),
                padding="8",
                max_width="800px",
                margin_x="auto",
            )
        )

    return rx.box(
        rx.vstack(
            rx.link(
                rx.button("← Back to Explore", variant="soft"),
                href="/explore",
            ),
            rx.hstack(
                rx.heading(activity.title),
                rx.badge(activity.category, color_scheme="blue"),
                align="center",
                spacing="4",
            ),
            rx.text(activity.description),
            rx.divider(),
            rx.vstack(
                rx.text(f"Location: {activity.location}", weight="medium"),
                rx.text(f"Distance: {activity.distance}", weight="medium"),
                rx.text(f"Time: {activity.time}", weight="medium"),
                rx.text(f"Max participants: {activity.max_participants}", weight="medium"),
                align="start",
            ),
            rx.divider(),
            rx.heading("Participants", size="md"),
            rx.cond(
                len(activity.participants) > 0,
                rx.vstack(
                    rx.foreach(
                        activity.participants,
                        lambda p: rx.text(f"• {p}"),
                    ),
                    align="start",
                ),
                rx.text("No participants yet", color="gray"),
            ),
            rx.divider(),
            rx.text(
                "Buttons are disabled in this prototype. "
                "The important part is that data flows correctly."
            ),
            rx.hstack(
                rx.button("Join Activity", color_scheme="green", disabled=True),
                rx.button("Edit", color_scheme="blue", disabled=True),
                rx.button("Delete", color_scheme="red", disabled=True),
            ),
            padding="8",
            max_width="800px",
            margin_x="auto",
        ),
    )
