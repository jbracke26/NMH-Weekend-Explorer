import reflex as rx
from app.models import load_activities


def _get_activity_by_id(activity_id: str):
    for a in load_activities():
        if str(a.id) == str(activity_id):
            return a
    return None


def activity_detail(id: str = "") -> rx.Component:
    activity = _get_activity_by_id(id) if id else None

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
            rx.text(activity.description or ""),
            rx.divider(),
            rx.vstack(
                rx.text(f"Location: {activity.location}", weight="medium"),
                rx.text(f"Distance: {activity.distance}", weight="medium"),
                rx.text(f"When: {activity.time}", weight="medium"),
                rx.text(
                    f"Max participants: {activity.max_participants or 'No limit'}",
                    weight="medium",
                ),
                align="start",
            ),
            rx.divider(),
            rx.heading("Participants", size="md"),
            rx.cond(
                len(activity.participants or []) > 0,
                rx.vstack(
                    rx.foreach(
                        activity.participants or [],
                        lambda p: rx.text(f"• {p}"),
                    ),
                    align="start",
                ),
                rx.text("No participants yet", color="gray"),
            ),
            padding="8",
            max_width="800px",
            margin_x="auto",
        ),
    )

