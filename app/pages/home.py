import reflex as rx
from app.states.state import State
from app.layout import layout
from app.config import Config


_config = Config()
GOOGLE_CLIENT_ID = _config.GOOGLE_CLIENT_ID or ""


def index():
    """Home page with specific user-requested layout."""
    return layout(
        rx.vstack(
            # Row 1: My Activities (Horizontal)
            rx.box(
                rx.heading("My Activities", size="5", margin_bottom="3"),
                rx.cond(
                    State.is_authenticated,
                    rx.cond(
                        State.my_activities_list,
                        rx.hstack(
                            rx.foreach(
                                State.my_activities_list,
                                lambda activity: rx.card(
                                    rx.vstack(
                                        rx.text(
                                            activity["title"], weight="bold", size="2"
                                        ),
                                        rx.text(activity["time"], size="1"),
                                        rx.badge(
                                            rx.cond(
                                                activity["creator_id"]
                                                == State.current_user_id,
                                                "Created",
                                                "Joined",
                                            ),
                                            color_scheme=rx.cond(
                                                activity["creator_id"]
                                                == State.current_user_id,
                                                "green",
                                                "blue",
                                            ),
                                            size="1",
                                        ),
                                        align_items="start",
                                        spacing="1",
                                    ),
                                    min_width="200px",
                                    height="100px",
                                    cursor="pointer",
                                    _hover={"box_shadow": "md"},
                                ),
                            ),
                            overflow_x="auto",
                            padding_bottom="4",
                            spacing="4",
                            width="100%",
                        ),
                        rx.text(
                            "No activities yet. Create one or join an upcoming activity!",
                            size="2",
                            color="gray",
                        ),
                    ),
                    rx.text(
                        "Please log in to see your activities.",
                        size="2",
                        color="gray",
                    ),
                ),
                width="100%",
                margin_bottom="6",
            ),
            # Row 2: Map (Left 2/3) and Upcoming Activities (Right 1/3)
            rx.hstack(
                # Map (Left 2/3)
                rx.box(
                    rx.center(
                        rx.vstack(
                            rx.icon("map", size=48, color="var(--gray-9)"),
                            rx.text("Map View", size="4", color="var(--gray-11)"),
                            spacing="3",
                        ),
                        height="400px",
                    ),
                    border_radius="12px",
                    border="1px solid var(--gray-6)",
                    background="var(--gray-2)",
                    flex="2",
                ),
                # Upcoming Activities (Right 1/3)
                rx.vstack(
                    rx.heading("Upcoming Activities", size="4", margin_bottom="3"),
                    rx.vstack(
                        rx.foreach(
                            State.filtered_activities[:5],
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
                                                activity["time"],
                                                size="2",
                                                color="var(--gray-11)",
                                            ),
                                            spacing="2",
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
                    rx.link(
                        rx.button(
                            "Create Activity",
                            size="3",
                            width="100%",
                            margin_top="4",
                        ),
                        href="/create",
                        width="100%",
                    ),
                    flex="1",
                ),
                spacing="4",
                width="100%",
            ),
            width="100%",
            spacing="0",
        ),
        on_mount=State.load_activities,
    )
