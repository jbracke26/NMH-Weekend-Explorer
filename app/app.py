import reflex as rx
from app.pages.explore import explore
from app.pages.activity_detail import activity_detail



app = rx.App()


app.add_page(explore, route="/explore")
app.add_page(activity_detail, route="/activity/[id]")
