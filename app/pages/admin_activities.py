import reflex as rx
from app.states.admin_state import AdminState
from app.layout import layout
from app.design import COLORS, card_style


def admin_activities():
    return layout(
        rx.cond(
            AdminState.is_admin,
            rx.vstack(
                rx.hstack(
                    rx.heading("Manage Activities", size="7"),
                    rx.spacer(),
                    rx.link(
                        rx.button("Back to Dashboard", variant="outline"),
                        href="/admin",
                    ),
                    width="100%",
                    align="center",
                ),
                rx.box(
                    rx.vstack(
                        rx.foreach(
                            AdminState.enhanced_activities,
                            lambda activity: rx.box(
                                rx.hstack(
                                    rx.vstack(
                                        rx.text(
                                            activity["title"], weight="bold", size="4"
                                        ),
                                        rx.text(
                                            f"{activity['category']} • {activity['location']} • {activity['time']}",
                                            size="2",
                                            color=COLORS["text_muted"],
                                        ),
                                        rx.text(
                                            f"Created by: {activity['creator_name']}",
                                            size="1",
                                            color=COLORS["text_muted"],
                                        ),
                                        align_items="start",
                                        spacing="1",
                                        flex="1",
                                    ),
                                    rx.hstack(
                                        rx.badge(
                                            f"{activity['participant_count']} participants",
                                            color_scheme="blue",
                                        ),
                                        rx.cond(
                                            activity["max_participants"],
                                            rx.badge(
                                                f"Max: {activity['max_participants']}",
                                                color_scheme="gray",
                                                variant="soft",
                                            ),
                                        ),
                                        rx.link(
                                            rx.button(
                                                "Edit",
                                                size="2",
                                                variant="soft",
                                                color_scheme="blue",
                                            ),
                                            href="/edit/" + activity["id"].to_string(),
                                        ),
                                        rx.button(
                                            rx.icon("trash-2", size=16),
                                            size="2",
                                            variant="soft",
                                            color_scheme="red",
                                            on_click=lambda: AdminState.delete_activity_admin(
                                                activity["id"]
                                            ),
                                        ),
                                        spacing="3",
                                    ),
                                    width="100%",
                                    align="center",
                                    padding="4",
                                ),
                                border_bottom=f"1px solid {COLORS['border']}",
                                _last={"border_bottom": "none"},
                            ),
                        ),
                        width="100%",
                        spacing="0",
                    ),
                    **card_style(padding="0"),
                    margin_top="5",
                ),
                width="100%",
                spacing="5",
            ),
            rx.vstack(
                rx.heading("Access Denied", size="7"),
                rx.text("You need admin privileges to access this page."),
                rx.link(rx.button("Back to Home"), href="/"),
                spacing="4",
            ),
        ),
        on_mount=AdminState.on_admin_page_load,
    )
