import reflex as rx
from app.states.state import State
from app.layout import layout


# style constants
accent_color = "teal"


def activity_card(activity: dict) -> rx.Component:
    return rx.link(
        rx.box(
            rx.vstack(
                rx.text(
                    activity["title"],
                    weight="bold",
                    size="3",
                ),
                rx.hstack(
                    rx.badge(
                        activity["category"],
                        size="1",
                        variant="soft",
                    ),
                    rx.text(
                        activity.get("time", ""),
                        size="2",
                        color="var(--gray-11)",
                    ),
                    rx.cond(
                        activity.get("admin_signed_up", False),
                        rx.badge(
                            "Chaperone assigned",
                            size="1",
                            color_scheme="green",
                        ),
                        rx.cond(
                            activity.get("needs_chaperone", False),
                            rx.badge(
                                "Needs chaperone",
                                size="1",
                                color_scheme="red",
                            ),
                            rx.fragment(),
                        ),
                    ),
                    spacing="2",
                ),
                rx.text(
                    f"Location: {activity['location']}",
                    size="1",
                    color="var(--gray-8)",
                ),
                align_items="start",
                spacing="2",
            ),
            padding="3",
            border_radius="8px",
            border="1px solid var(--gray-6)",
            background="var(--color-background)",
            _hover={
                "background": "var(--gray-3)",
                "border_color": "var(--gray-7)",
            },
            transition="all 0.2s ease",
            width="100%",
        ),
        href=f"/activity/{activity['id']}",
        text_decoration="none",
        color="inherit",
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
            on_mount=State.on_page_load,
            min_height="100vh",
        )
    )
