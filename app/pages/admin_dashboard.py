import reflex as rx
from app.states.admin_state import AdminState
from app.layout import layout
from app.design import COLORS, card_style


def admin_dashboard():
    return layout(
        rx.cond(
            AdminState.is_admin,
            rx.vstack(
                rx.heading("Admin Dashboard", size="7", margin_bottom="6"),
                rx.hstack(
                    rx.box(
                        rx.vstack(
                            rx.text(
                                "Total Activities", size="2", color=COLORS["text_muted"]
                            ),
                            rx.heading(
                                AdminState.admin_stats["total_activities"], size="8"
                            ),
                            spacing="2",
                        ),
                        **card_style(padding="6", flex="1"),
                    ),
                    rx.box(
                        rx.vstack(
                            rx.text(
                                "Total Users", size="2", color=COLORS["text_muted"]
                            ),
                            rx.heading(AdminState.admin_stats["total_users"], size="8"),
                            spacing="2",
                        ),
                        **card_style(padding="6", flex="1"),
                    ),
                    rx.box(
                        rx.vstack(
                            rx.text(
                                "Recent (7 days)", size="2", color=COLORS["text_muted"]
                            ),
                            rx.heading(
                                AdminState.admin_stats["recent_activities"], size="8"
                            ),
                            spacing="2",
                        ),
                        **card_style(padding="6", flex="1"),
                    ),
                    spacing="5",
                    width="100%",
                ),
                rx.box(
                    rx.heading("Quick Actions", size="5", margin_bottom="4"),
                    rx.hstack(
                        rx.link(
                            rx.button("Manage Activities", size="3"),
                            href="/admin/activities",
                        ),
                        rx.link(
                            rx.button("Manage Users", size="3", variant="soft"),
                            href="/admin/users",
                        ),
                        rx.link(
                            rx.button("Back to App", size="3", variant="outline"),
                            href="/",
                        ),
                        spacing="4",
                    ),
                    **card_style(padding="6"),
                    margin_top="8",
                ),
                width="100%",
                spacing="5",
            ),
            rx.vstack(
                rx.heading("Access Denied", size="7"),
                rx.text("You need admin privileges to access this page."),
                rx.link(
                    rx.button("Back to Home"),
                    href="/",
                ),
                spacing="4",
            ),
        ),
        on_mount=AdminState.on_admin_page_load,
    )
