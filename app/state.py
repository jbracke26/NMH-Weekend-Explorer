import reflex as rx
import json
from typing import List, Optional
from app.models import Activity, load_activities, save_activities
from app import example_data


class State(rx.State):
    current_user_id: Optional[int] = 1
    current_user_name: str = "Demo User"
    is_authenticated: bool = True

    activities: List[dict] = []
    redirect_path: str = ""

    search_query: str = ""
    filter_category: str = "All"
    filter_distance: str = "Any"

    activity_title: str = ""
    activity_description: str = ""
    activity_category: str = "Other"
    activity_location: str = ""
    activity_distance: str = ""
    activity_date: str = ""
    activity_time: str = "10:00"
    activity_max_participants: str = ""
    activity_admin: bool = False,
    log_location: bool = False,
    activity_latitude: str = ""
    activity_longitude: str = ""

    def set_activity_latitude(self, value: str):
    self.activity_latitude = value

    def set_activity_longitude(self, value: str):
    self.activity_longitude = value

    message: str = ""
    message_type: str = "info"

    current_activity: dict = {}

    def load_activity_details(self):
        """Load the specific activity details based on the route param."""
        activity_id = self.router.page.params.get("activity_id")
        if activity_id:
            if not self.activities:
                self.load_activities()

            try:
                aid = int(activity_id)
                for a in self.activities:
                    if a["id"] == aid:
                        self.current_activity = a
                        break
            except ValueError:
                pass

    def join_activity(self):
        """Join the current activity."""
        pass

    def load_activities(self):
        """Load activities from activities.json into state.activities."""
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
                "log_location": a.activity_log_location,
                "latitude": self.activity_latitude if self.activity_log_location else None,
                "longitude": self.activity_longitude if self.activity_log_location else None,
            }
            for a in acts
        ]

    def _next_id(self) -> int:
        acts = load_activities()
        return max([a.id for a in acts], default=0) + 1

    def create_activity(self):
        """Create a new activity and save it to activities.json."""
        try:
            acts = load_activities()

            if self.activity_max_participants.strip():
                try:
                    max_participants = int(self.activity_max_participants)
                except ValueError:
                    max_participants = None
            else:
                max_participants = None

            time_str = (
                f"{self.activity_date} {self.activity_time}".strip()
                if self.activity_date or self.activity_time
                else ""
            )

            new_activity = Activity(
                id=self._next_id(),
                title=self.activity_title,
                description=self.activity_description,
                category=self.activity_category,
                location=self.activity_location,
                distance=self.activity_distance,
                time=time_str,
                max_participants=max_participants,
                participants=[],
                creator_id=self.current_user_id or 1,
                activity_admin=self.activity_admin,
                log_location=self.activity_log_location,
            )

            acts.append(new_activity)
            save_activities(acts)

            self.load_activities()

            self.activity_title = ""
            self.activity_description = ""
            self.activity_location = ""
            self.activity_distance = ""
            self.activity_date = ""
            self.activity_time = "10:00"
            self.activity_max_participants = ""

            self.message = "Activity created successfully!"
            self.message_type = "success"

            return rx.redirect("/explore")
        except Exception as e:
            self.message = f"Error creating activity: {e}"
            self.message_type = "error"

    @rx.var
    def filtered_activities(self) -> List[dict]:
        """Activities after applying search, category, and distance filters."""
        acts = list(self.activities)

        q = self.search_query.lower().strip()
        if q:
            acts = [
                a
                for a in acts
                if q in a.get("title", "").lower()
                or q in a.get("description", "").lower()
                or q in a.get("location", "").lower()
            ]

        if self.filter_category != "All":
            acts = [
                a for a in acts if a.get("category", "Other") == self.filter_category
            ]

        if self.filter_distance != "Any":
            acts = [a for a in acts if a.get("distance", "Any") == self.filter_distance]

        return acts

    @rx.var
    def my_activities_list(self) -> List[dict]:
        """Activities created by the current user."""
        if not self.current_user_id:
            return []
        return [
            a for a in self.activities if a.get("creator_id") == self.current_user_id
        ]

    def filter_by_location(self, location: str):
        """Called when you click 'Home' etc on a card."""
        self.search_query = location

    def filter_by_distance_label(self, distance: str):
        """Called when you click 'Varies' or '5 minute walk'."""
        self.filter_distance = distance

    def clear_redirect(self):
        self.redirect_path = ""

    def toggle_chaperone(self):
        if self.current_activity["chaperone_id"] == self.current_user_id:
            self.current_activity["chaperone_id"] = None
            self.current_activity["admin_signed_up"] = False
        else:
            self.current_activity["chaperone_id"] = self.current_user_id
            self.current_activity["admin_signed_up"] = True
