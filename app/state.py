import reflex as rx
from typing import List, Optional

from app.models import Activity, load_activities, save_activities
from app import example_data  # noqa: F401  - make sure seed runs


class State(rx.State):
    current_user_id: Optional[int] = 1
    current_user_name: str = "Demo User"

    activities: List[dict] = []
    my_activities_list: List[dict] = []
    redirect_path: str = ""

    activity_title: str = ""
    activity_description: str = ""
    activity_category: str = "Other"
    activity_location: str = ""
    activity_distance: str = ""
    activity_date: str = ""         # "YYYY-MM-DD"
    activity_time: str = "10:00"
    activity_max_participants: str = ""

    message: str = ""
    message_type: str = "info"

    def load_activities(self):
        """Load activities from activities.json into state."""
        acts = load_activities()
        self.activities = [
            {
                "id": a.id,
                "title": a.title,
                "description": a.description,
                "category": a.category,
                "location": a.location,
                "distance": a.distance,
                "time": a.time,
                "max_participants": a.max_participants,
                "participants": a.participants or [],
                "creator_id": a.creator_id,
            }
            for a in acts
        ]
        self.my_activities_list = [
            a for a in self.activities if a.get("creator_id") == self.current_user_id
        ]

    def _next_id(self) -> int:
        acts = load_activities()
        return max([a.id for a in acts], default=0) + 1

    def create_activity(self):
        """Create a new activity and save it to activities.json."""
        acts = load_activities()
        new_id = self._next_id()
        when_str = f"{self.activity_date} {self.activity_time}".strip()

        new_activity = Activity(
            id=new_id,
            title=self.activity_title,
            description=self.activity_description,
            category=self.activity_category or "Other",
            location=self.activity_location,
            distance=self.activity_distance,
            time=when_str,
            max_participants=self.activity_max_participants or None,
            participants=[],
            creator_id=self.current_user_id,
        )
        acts.append(new_activity)
        save_activities(acts)

        self.message = "Activity created successfully."
        self.message_type = "success"
        self.redirect_path = f"/activity/{new_id}"

        # refresh lists so the new one appears
        self.load_activities()

    def clear_redirect(self):
        self.redirect_path = ""
