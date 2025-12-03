import reflex as rx

from app.pages.explore import explore
from app.pages.activity_detail import activity_detail
from app.pages.create_activity import create_activity
from app.pages.my_activities import my_activities
from app.state import State


app = rx.App()

app.add_page(
    explore,
    route="/",
    title="Explore",
    on_load=State.load_activities,
)

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

