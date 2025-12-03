import reflex as rx
from app.models import load_activities


def pick_activity(activity_id: str):
    """Try to find an activity by id; if that fails, fall back to the first one."""
    activities = load_activities()

    if not activities:
        return None

    for a in activities:
        try:
            stored_id = getattr(a, "id", None)
            if stored_id is None:
                continue

            if str(stored_id).strip() == str(activity_id).strip():
                return a
        except Exception:
            continue

    return activities[0]


def activity_detail(activity_id: str = "") -> rx.Component:
    """Detail page for a single activity."""
    activity = pick_activity(activity_id)

    if activity is None:
        return rx.box(
            rx.vstack(
                rx.link(
                    rx.button("← Back to Explore", variant="soft"),
                    href="/explore",
                ),
                rx.heading("No activities available", color="red"),
                padding="8",
                max_width="800px",
                margin_x="auto",
            )
        )

    # Defensive getters so we do not crash if a field is missing.
    title = getattr(activity, "title", "Untitled activity")
    category = getattr(activity, "category", "Other")
    description = getattr(activity, "description", "")
    location = getattr(activity, "location", "")
    distance = getattr(activity, "distance", "")
    time = getattr(activity, "time", "")
    max_participants = getattr(activity, "max_participants", "")
    participants = getattr(activity, "participants", []) or []

    return rx.box(
        rx.vstack(
            rx.link(
                rx.button("← Back to Explore", variant="soft"),
                href="/explore",
            ),
            rx.hstack(
                rx.heading(title, size="5"),
                rx.badge(category, color_scheme="blue"),
                align="center",
                spacing="4",
            ),
            rx.text(description),
            rx.divider(),
            rx.vstack(
                rx.text(f"Location: {location}"),
                rx.text(f"Distance: {distance}"),
                rx.text(f"Time: {time}"),
                rx.text(f"Max participants: {max_participants}"),
                align="start",
                spacing="1",
            ),
            rx.divider(),
            rx.heading("Participants", size="4"),
            rx.cond(
                len(participants) > 0,
                rx.vstack(
                    rx.foreach(participants, lambda p: rx.text(f"• {p}")),
                    align="start",
                ),
                rx.text("No participants yet", color="gray"),
            ),
            padding="8",
            max_width="800px",
            margin_x="auto",
        ),
    )
