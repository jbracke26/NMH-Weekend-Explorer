import reflex as rx
from app.state import State


# style constants
bg_color = "gray.50"
card_bg = "white"
text_color = "gray.600"
heading_color = "gray.900"
accent_color = "teal"
border_color = "gray.200"


def activity_card(activity: dict) -> rx.Component:
    return rx.link(
        rx.box(
            rx.vstack(
                # category badge
                rx.box(
                    rx.badge(
                        activity["category"],
                        color_scheme=accent_color,
                        variant="solid",
                        padding="1",
                    ),
                    display="flex",
                    justify_content="flex-end",
                    width="100%",
                    mb=2,
                ),
                # title and description
                rx.heading(activity["title"], size="4", color=heading_color),
                rx.text(
                    activity["description"],
                    color=text_color,
                    size="2",
                    no_of_lines=3,
                ),
                rx.spacer(),
                rx.divider(border_color=border_color),
                # footer with location and date
                rx.hstack(
                    rx.hstack(
                        rx.icon("map-pin", size=14, color="gray.500"),
                        rx.text(
                            activity["location_name"], font_size="xs", color="gray.500"
                        ),
                        spacing="1",
                    ),
                    rx.spacer(),
                    rx.text(
                        activity["date"],
                        font_size="xs",
                        font_weight="bold",
                        color=f"{accent_color}.600",
                    ),
                    width="100%",
                    pt=2,
                ),
                align="start",
                height="100%",
                spacing="2",
            ),
            padding="5",
            bg=card_bg,
            border="1px solid",
            border_color=border_color,
            border_radius="xl",
            box_shadow="sm",
            transition="all 0.2s",
            _hover={
                "transform": "translateY(-2px)",
                "box_shadow": "md",
                "border_color": f"{accent_color}.300",
            },
            height="250px",
            width="100%",
        ),
        href=f"/activity/{activity['id']}",
        text_decoration="none",
        width="100%",
    )


def explore() -> rx.Component:
    return rx.box(
        rx.vstack(
            # hero section
            rx.box(
                rx.heading(
                    "Weekend Explorer", size="8", color=f"{accent_color}.800", mb=2
                ),
                rx.text(
                    "Find something to do this weekend.",
                    color=text_color,
                    font_size="lg",
                ),
                text_align="center",
                py=8,
                width="100%",
                bg=bg_color,
            ),
            # main content area
            rx.vstack(
                # filters and search
                rx.hstack(
                    rx.input(
                        placeholder="Search activities...",
                        value=State.search_query,
                        on_change=State.set_search_query,
                        bg=card_bg,
                        border_color="gray.300",
                        _focus={"border_color": f"{accent_color}.500"},
                        width=["100%", "300px"],
                    ),
                    rx.select(
                        [
                            "All Categories",
                            "Outdoor",
                            "Food",
                            "Shopping",
                            "Sports",
                            "Other",
                        ],
                        placeholder="Category",
                        value=State.filter_category,
                        on_change=State.set_filter_category,
                        bg=card_bg,
                        border_color="gray.300",
                    ),
                    rx.select(
                        ["Any Distance", "5 min", "15 min", "30 min"],
                        placeholder="Distance",
                        value=State.filter_distance,
                        on_change=State.set_filter_distance,
                        bg=card_bg,
                        border_color="gray.300",
                    ),
                    rx.button(
                        "Search",
                        on_click=State.load_activities,
                        color_scheme=accent_color,
                        variant="solid",
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
                    State.activities,
                    rx.grid(
                        rx.foreach(State.activities, activity_card),
                        columns=rx.breakpoints(initial="1", sm="2", md="3", lg="4"),
                        spacing="6",
                        width="100%",
                        padding_x="4",
                    ),
                    # empty state
                    rx.vstack(
                        rx.icon("search", size=48, color="gray.300"),
                        rx.text(
                            "No activities found matching your criteria.",
                            color="gray.500",
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
        bg=card_bg,
        min_height="100vh",
    )
