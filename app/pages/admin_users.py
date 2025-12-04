import reflex as rx
from app.states.admin_state import AdminState
from app.layout import layout
from app.design import COLORS, card_style


def admin_users():
    return layout(
        rx.cond(
            AdminState.is_admin,
            rx.vstack(
                rx.hstack(
                    rx.heading("Manage Users", size="7"),
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
                            AdminState.all_users_list,
                            lambda user: rx.box(
                                rx.hstack(
                                    rx.vstack(
                                        rx.hstack(
                                            rx.text(
                                                user["name"], weight="bold", size="3"
                                            ),
                                            rx.cond(
                                                user["is_admin"],
                                                rx.badge(
                                                    "Admin",
                                                    color_scheme="purple",
                                                    size="1",
                                                ),
                                                rx.fragment(),
                                            ),
                                            spacing="3",
                                            align="center",
                                        ),
                                        rx.text(
                                            user["email"],
                                            size="2",
                                            color=COLORS["text_muted"],
                                        ),
                                        align_items="start",
                                        spacing="1",
                                        flex="1",
                                    ),
                                    rx.hstack(
                                        rx.badge(
                                            f"{user['created_activities']} created",
                                            color_scheme="green",
                                            size="1",
                                        ),
                                        rx.badge(
                                            f"{user['joined_activities']} joined",
                                            color_scheme="blue",
                                            size="1",
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
        on_mount=AdminState.load_activities,
    )
