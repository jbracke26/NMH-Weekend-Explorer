import reflex as rx


from reflex_google_auth import GoogleAuthState

from typing import List, Optional

from app.models import Activity, load_activities, save_activities
from app import example_data  


class State(rx.State):
    current_user_id: Optional[int] = None
    current_user_name: str = ""
    is_authenticated: bool = False
    current_user_email: str = ""
    current_user_picture: str = ""

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

    message: str = ""
    message_type: str = "info"


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
                a
                for a in acts
                if a.get("category", "Other") == self.filter_category
            ]

        if self.filter_distance != "Any":
            acts = [
                a
                for a in acts
                if a.get("distance", "Any") == self.filter_distance
            ]

        return acts

    @rx.var
    def my_activities_list(self) -> List[dict]:
        """Activities created by the current user."""
        if not self.current_user_id:
            return []
        return [
            a
            for a in self.activities
            if a.get("creator_id") == self.current_user_id
        ]

    def filter_by_location(self, location: str):
        """Called when you click 'Home' etc on a card."""
        self.search_query = location

    def filter_by_distance_label(self, distance: str):
        """Called when you click 'Varies' or '5 minute walk'."""
        self.filter_distance = distance

    def clear_redirect(self):
        self.redirect_path = ""

    def on_google_login_success(self, response: dict):
        """Handler for successful Google login."""
        # TODO: Extract name / email from response if needed
        if not self.current_user_name:
            self.current_user_name = "Google User"

        self.is_authenticated = True
        self.redirect_path = "/explore"
        self.message = "Logged in successfully!"
        self.message_type = "success"
        return rx.redirect("/explore")

    def logout(self):
        """Logout: Clear authentication and redirect to login page."""
        self.current_user_id = None
        self.current_user_name = ""
        self.current_user_email = ""
        self.current_user_picture = ""
        self.is_authenticated = False
        self.redirect_path = "/"
        self.message = "Logged out."
        self.message_type = "info"
        return rx.redirect("/")