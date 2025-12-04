import reflex as rx
from app.states.state import State
from app.layout import layout


def map_page():
    """Map page showing activities on a map and in a list."""
    return layout(
        rx.vstack(
            rx.heading("Activity Map", size="7", margin_bottom="5"),
            # Map and List Container
            rx.hstack(
                # Map placeholder (Left 2/3)
                rx.box(
                    rx.center(
                        rx.vstack(
                            rx.icon("map-pin", size=48, color="var(--gray-9)"),
                            rx.text(
                                "Interactive Map View", size="4", color="var(--gray-11)"
                            ),
                            rx.text("Coming soon", size="2", color="var(--gray-10)"),
                            spacing="3",
                        ),
                        height="500px",
                    ),
                    border_radius="12px",
                    border="1px solid var(--gray-6)",
                    background="var(--gray-2)",
                    flex="2",
                ),
                # Activities List (Right 1/3)
                rx.vstack(
                    rx.heading("All Activities", size="4", margin_bottom="3"),
                    rx.box(
                        rx.vstack(
                            rx.foreach(
                                State.filtered_activities,
                                lambda activity: rx.link(
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
                                                    activity["location"],
                                                    size="2",
                                                    color="var(--gray-11)",
                                                ),
                                                spacing="2",
                                            ),
                                            rx.text(
                                                activity["time"],
                                                size="2",
                                                color="var(--gray-10)",
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
                                ),
                            ),
                            spacing="2",
                            width="100%",
                        ),
                        height="500px",
                        overflow_y="auto",
                        width="100%",
                    ),
                    flex="1",
                ),
                spacing="4",
                width="100%",
                align_items="start",
            ),
            width="100%",
            spacing="5",
        ),
        on_mount=State.load_activities,
    )
