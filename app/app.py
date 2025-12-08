import reflex as rx
from app.pages.home import index as login_page
from app.pages.explore import explore
from app.pages.activity_detail import activity_detail
from app.pages.create_activity import create_activity
from app.pages.my_activities import my_activities
from app.pages.map_page import map_page
from app.pages.admin_dashboard import admin_dashboard
from app.pages.admin_activities import admin_activities
from app.pages.admin_users import admin_users
from app.states.state import State


app = rx.App()

app.add_page(login_page, route="/", title="Login")

app.add_page(
    explore,
    route="/explore",
    title="Explore",
    on_load=State.load_activities,
)

app.add_page(
    activity_detail,
    route="/activity/[activity_id]",
    title="Activity",
)

app.add_page(
    create_activity,
    route="/create",
    title="Create Activity",
)

app.add_page(
    my_activities,
    route="/my-activities",
    title="My Activities",
)

app.add_page(
    map_page,
    route="/map",
    title="Map",
    on_load=State.load_activities,
)

app.add_page(
    admin_dashboard,
    route="/admin",
    title="Admin Dashboard",
)

app.add_page(
    admin_activities,
    route="/admin/activities",
    title="Manage Activities",
)

app.add_page(
    admin_users,
    route="/admin/users",
    title="Manage Users",
)
