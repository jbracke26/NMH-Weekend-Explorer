import reflex as rx
from app.pages.explore import explore
from app.pages.activity_detail import activity_detail
from app.pages.create_activity import create_activity
from app.state import ActivityState

app = rx.App(state=ActivityState)

app.add_page(
    explore,
    route="/",
    title="Explore",
    on_load=ActivityState.load,
)

app.add_page(
    explore,
    route="/explore",
    title="Explore",
    on_load=ActivityState.load,
)

app.add_page(
    activity_detail,
    route="/activity/[id]",
    title="Activity",
)

app.add_page(
    create_activity,
    route="/create",
    title="Create Activity",
)
