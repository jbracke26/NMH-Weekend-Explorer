import reflex as rx
from app.state import State


# style constants
bg_color = "gray.50"
card_bg = "white"
text_color = "gray.600"
heading_color = "gray.900"
accent_color = "teal"


def activity_detail() -> rx.Component:
    return rx.box(
        rx.cond(
            State.current_activity,
            rx.vstack(
                # back button area
                rx.box(
                    rx.link(
                        rx.hstack(
                            rx.icon("arrow-left", size=20),
                            rx.text("Back to Explore"),
                            color=text_color,
                            _hover={"color": f"{accent_color}.600"},
                        ),
                        href="/explore",
                        text_decoration="none",
                    ),
                    mb=6,
                    width="100%",
                    max_width="800px",
                    margin="0 auto",
                    padding_top="8",
                    padding_x="4",
                ),
                # main content card
                rx.box(
                    rx.vstack(
                        # header with title and category
                        rx.hstack(
                            rx.heading(
                                State.current_activity["title"],
                                size="8",
                                color=heading_color,
                            ),
                            rx.spacer(),
                            rx.badge(
                                State.current_activity["category"],
                                color_scheme=accent_color,
                                size="3",
                            ),
                            width="100%",
                            align="start",
                            mb=4,
                        ),
                        # location and time info
                        rx.hstack(
                            rx.icon("map-pin", color="gray.500"),
                            rx.text(
                                State.current_activity["location_name"],
                                color=text_color,
                                font_weight="medium",
                            ),
                            rx.spacer(),
                            rx.icon("calendar", color="gray.500"),
                            rx.text(
                                f"{State.current_activity['date']} @ {State.current_activity['time']}",
                                color=text_color,
                                font_weight="medium",
                            ),
                            width="100%",
                            mb=6,
                            padding_bottom="6",
                            border_bottom="1px solid",
                            border_color="gray.100",
                        ),
                        # description
                        rx.text(
                            State.current_activity["description"],
                            font_size="lg",
                            color="gray.700",
                            line_height="1.6",
                            mb=8,
                        ),
                        # details grid (host, capacity)
                        rx.box(
                            rx.heading("Details", size="5", mb=4, color="gray.800"),
                            rx.grid(
                                rx.vstack(
                                    rx.text(
                                        "Host",
                                        font_size="sm",
                                        color="gray.500",
                                        text_transform="uppercase",
                                        letter_spacing="wide",
                                    ),
                                    rx.text(
                                        State.current_activity["creator_name"],
                                        font_weight="bold",
                                    ),
                                    align="start",
                                ),
                                rx.vstack(
                                    rx.text(
                                        "Capacity",
                                        font_size="sm",
                                        color="gray.500",
                                        text_transform="uppercase",
                                        letter_spacing="wide",
                                    ),
                                    rx.hstack(
                                        rx.text(
                                            State.current_activity["participant_count"]
                                        ),
                                        rx.text("/"),
                                        rx.cond(
                                            State.current_activity["max_participants"],
                                            rx.text(
                                                State.current_activity[
                                                    "max_participants"
                                                ]
                                            ),
                                            rx.text("Unlimited"),
                                        ),
                                        font_weight="bold",
                                    ),
                                    align="start",
                                ),
                                columns="2",
                                spacing="6",
                                width="100%",
                            ),
                            bg=bg_color,
                            padding="6",
                            border_radius="lg",
                            width="100%",
                            mb=8,
                        ),
                        # participants section
                        rx.heading("Participants", size="5", mb=4, color="gray.800"),
                        rx.box(
                            rx.cond(
                                State.current_activity_participants,
                                rx.flex(
                                    rx.foreach(
                                        State.current_activity_participants,
                                        lambda p: rx.badge(
                                            p,
                                            variant="soft",
                                            color_scheme="gray",
                                            padding="2",
                                            border_radius="full",
                                        ),
                                    ),
                                    spacing="2",
                                    wrap="wrap",
                                ),
                                rx.text(
                                    "No participants yet. Be the first!",
                                    color="gray.500",
                                    font_style="italic",
                                ),
                            ),
                            mb=8,
                        ),
                        rx.divider(mb=8),
                        # action buttons
                        rx.hstack(
                            rx.cond(
                                State.is_authenticated,
                                rx.button(
                                    "Join Activity",
                                    color_scheme=accent_color,
                                    size="3",
                                    width="full",
                                    on_click=lambda: State.join_activity(
                                        State.current_activity["id"]
                                    ),
                                ),
                                rx.tooltip(
                                    rx.button(
                                        "Join Activity",
                                        color_scheme="gray",
                                        size="3",
                                        width="full",
                                        disabled=True,
                                    ),
                                    label="Log in to join",
                                ),
                            ),
                            rx.cond(
                                State.current_user_id
                                == State.current_activity["creator_id"],
                                rx.hstack(
                                    rx.button(
                                        "Edit",
                                        variant="outline",
                                        color_scheme="blue",
                                        size="3",
                                    ),
                                    rx.button(
                                        "Delete",
                                        variant="outline",
                                        color_scheme="red",
                                        size="3",
                                    ),
                                ),
                            ),
                            width="100%",
                            spacing="4",
                        ),
                        align="start",
                        width="100%",
                    ),
                    bg=card_bg,
                    padding="8",
                    border_radius="xl",
                    box_shadow="lg",
                    max_width="800px",
                    margin="0 auto",
                    width="100%",
                ),
                width="100%",
                padding_bottom="12",
            ),
            # loading state
            rx.center(
                rx.spinner(color=f"{accent_color}.500", size="3"), height="100vh"
            ),
        ),
        on_mount=lambda: State.get_activity_detail(
            State.router.page.params["activity_id"]
        ),
        bg=bg_color,
        min_height="100vh",
    )
