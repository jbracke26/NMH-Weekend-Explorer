from app.models import Activity, load_activities, save_activities, DATA_FILE  # type: ignore


EXAMPLE_ACTIVITIES = [
    Activity(
        id=1,
        title="Thanksgiving Break",
        description=(
            "Everyone is going on Thanksgiving Break, make sure you have a bus "
            "linked in this activity!"
        ),
        category="Other",
        location="Home",
        distance="Varies",
        time="Saturday November 22nd",
        max_participants="2000",
        participants=["Henry", "Ethan", "Georgii", "Shun"],
        creator_id=1,
    )
]


def ensure_seed_data() -> None:
    """If activities.json is missing or empty, write EXAMPLE_ACTIVITIES into it."""
    if not DATA_FILE.exists():
        save_activities(EXAMPLE_ACTIVITIES)
        return

    if not load_activities():
        save_activities(EXAMPLE_ACTIVITIES)


ensure_seed_data()
