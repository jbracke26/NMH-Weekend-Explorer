import reflex as rx
from app.state import State


def activity_card(activity: dict) -> rx.Component:
    """Single activity card on the Explore page."""
    return rx.card(
        rx.vstack(
            rx.link(
                rx.heading(activity.get("title", ""), size="4"),
                href=f"/activity/{activity['id']}",
                text_decoration="none",
            ),
            rx.badge(activity.get("category", "Other"), color_scheme="blue"),
            rx.text(
                activity.get("description", ""),
                color="gray",
                no_of_lines=3,
            ),
            # Location and distance act as filter buttons
            rx.hstack(
                rx.button(
                    activity.get("location", ""),
                    variant="ghost",
                    size="2",
                    padding_x="2",
                    on_click=lambda: State.filter_by_location(
                        activity.get("location", "")
                    ),
                ),
                rx.button(
                    activity.get("distance", ""),
                    variant="ghost",
                    size="2",
                    padding_x="2",
                    on_click=lambda: State.filter_by_distance_label(
                        activity.get("distance", "")
                    ),
                ),
                spacing="4",
                margin_top="1",
            ),
            rx.text(
                activity.get("time", ""),
                color="gray",
                margin_top="1",
            ),
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


def explore() -> rx.Component:
    return rx.box(
        rx.vstack(
            rx.heading("Explore Activities"),
            rx.text(
                "Browse activities created by the NMH community.",
                color="gray",
            ),
            rx.hstack(
                rx.input(
                    placeholder="Search activities...",
                    width="40%",
                    value=State.search_query,
                    on_change=State.set_search_query,
                ),
                rx.select(
                    ["All", "Outdoor", "Food", "Shopping", "Sports", "Other"],
                    placeholder="Category",
                    width="20%",
                    value=State.filter_category,
                    on_change=State.set_filter_category,
                ),
                rx.select(
                    ["Any", "5 min", "15 min", "30 min"],
                    placeholder="Distance",
                    width="20%",
                    value=State.filter_distance,
                    on_change=State.set_filter_distance,
                ),
                justify="between",
                width="100%",
            ),
            rx.grid(
                rx.foreach(State.filtered_activities, activity_card),
                columns={"base": "1", "md": "2", "lg": "3"},
                spacing="4",
                width="100%",
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
