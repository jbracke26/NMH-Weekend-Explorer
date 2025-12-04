import reflex as rx
from app.states.state import State
from app.layout import layout


# style constants
accent_color = "teal"


def activity_card(activity: dict) -> rx.Component:
    return rx.link(
        rx.card(
            rx.vstack(
                rx.hstack(
                    rx.heading(activity["title"], size="4"),
                    rx.spacer(),
                    rx.badge(
                        activity["category"],
                        color_scheme=accent_color,
                        variant="solid",
                    ),
                    width="100%",
                    align="center",
                ),
                rx.text(
                    activity["description"],
                    size="2",
                    no_of_lines=2,
                ),
                rx.hstack(
                    rx.icon("map-pin", size=16),
                    rx.text(activity["location"], size="2"),
                    rx.spacer(),
                    rx.icon("clock", size=16),
                    rx.text(activity.get("time", ""), size="2"),
                    width="100%",
                    align="center",
                    padding_top="2",
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
        ),
        href=f"/activity/{activity['id']}",
        text_decoration="none",
        width="100%",
    )


def explore() -> rx.Component:
    return layout(
        rx.box(
            rx.vstack(
                # hero section
                rx.box(
                    rx.heading("Weekend Explorer", size="8", mb=2),
                    rx.text(
                        "Find something to do this weekend.",
                        font_size="lg",
                    ),
                    text_align="center",
                    py=8,
                    width="100%",
                ),
                # main content area
                rx.vstack(
                    # filters and search
                    rx.hstack(
                        rx.input(
                            placeholder="Search activities...",
                            value=State.search_query,
                            on_change=State.set_search_query,
                            width=["100%", "300px"],
                        ),
                        rx.select(
                            [
                                "All",
                                "Outdoor",
                                "Food",
                                "Shopping",
                                "Sports",
                                "Other",
                            ],
                            placeholder="Category",
                            value=State.filter_category,
                            on_change=State.set_filter_category,
                        ),
                        rx.select(
                            ["Any", "5 min", "15 min", "30 min"],
                            placeholder="Distance",
                            value=State.filter_distance,
                            on_change=State.set_filter_distance,
                        ),
                        width="100%",
                        justify="center",
                        wrap="wrap",
                        spacing="4",
                        padding_x="4",
                    ),
                    rx.divider(my=6),
                    # results grid
                    rx.cond(
                        State.filtered_activities,
                        rx.grid(
                            rx.foreach(State.filtered_activities, activity_card),
                            columns=rx.breakpoints(initial="1", sm="2", md="3", lg="4"),
                            spacing="6",
                            width="100%",
                            padding_x="4",
                        ),
                        # empty state
                        rx.vstack(
                            rx.icon("search", size=48),
                            rx.text(
                                "No activities found matching your criteria.",
                            ),
                            py=12,
                        ),
                    ),
                    max_width="1200px",
                    margin="0 auto",
                    width="100%",
                    padding_bottom="12",
                ),
                width="100%",
                spacing="0",
            ),
            on_mount=State.load_activities,
            min_height="100vh",
        )
    )
