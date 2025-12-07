import reflex as rx

from typing import List, Optional
import json
import hashlib
from pathlib import Path
from app.models import Activity, load_activities, save_activities


class State(rx.State):
    current_user_id: Optional[int] = None
    current_user_name: str = ""
    is_authenticated: bool = False
    current_user_email: str = ""
    current_user_picture: str = ""
    is_admin: bool = False

    activities: List[dict] = []
    redirect_path: str = ""
    hide_header_login: bool = False

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

    current_activity: dict = {}

    def load_activity_details(self):
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
        if not self.is_authenticated:
            self.message = "Please log in to join activities."
            self.message_type = "error"
            return rx.redirect("/")

        if not self.current_activity:
            return

        from app.models import join_activity as model_join_activity

        try:
            model_join_activity(self.current_activity["id"], self.current_user_id)

            if "participants" not in self.current_activity:
                self.current_activity["participants"] = []

            if self.current_user_id not in self.current_activity["participants"]:
                self.current_activity["participants"].append(self.current_user_id)

            self.message = "Joined activity successfully!"
            self.message_type = "success"

            self.load_activities()
        except Exception as e:
            self.message = f"Error joining activity: {e}"
            self.message_type = "error"

    def delete_activity(self):
        if not self.is_authenticated:
            self.message = "Please log in to delete activities."
            self.message_type = "error"
            return

        if not self.current_activity:
            return

        if self.current_user_id != self.current_activity.get("creator_id"):
            self.message = "You can only delete activities you created."
            self.message_type = "error"
            return

        try:
            acts = load_activities()
            acts = [a for a in acts if a.id != self.current_activity["id"]]
            save_activities(acts)

            self.message = "Activity deleted successfully!"
            self.message_type = "success"
            self.load_activities()

            return rx.redirect("/explore")
        except Exception as e:
            self.message = f"Error deleting activity: {e}"
            self.message_type = "error"

    def leave_activity(self):
        if not self.is_authenticated:
            self.message = "Please log in to leave activities."
            self.message_type = "error"
            return

        if not self.current_activity:
            return

        try:
            acts = load_activities()
            for a in acts:
                if a.id == self.current_activity["id"]:
                    if a.participants and self.current_user_id in a.participants:
                        a.participants.remove(self.current_user_id)
                        save_activities(acts)

                        self.current_activity["participants"] = a.participants

                        self.message = "Left activity successfully!"
                        self.message_type = "success"
                        self.load_activities()
                        return

            self.message = "You are not a participant of this activity."
            self.message_type = "error"
        except Exception as e:
            self.message = f"Error leaving activity: {e}"
            self.message_type = "error"

    def load_activities(self):
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
        if not self.activity_title or not self.activity_title.strip():
            self.message = "Please provide a title for the activity."
            self.message_type = "error"
            return

        try:
            acts = load_activities()

            if not isinstance(acts, list):
                acts = []

            if self.activity_max_participants and self.activity_max_participants.strip():
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
                creator_id=self.current_user_id,
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
            self.message = f"Error creating activity: {str(e)}"
            self.message_type = "error"

    @rx.var
    def filtered_activities(self) -> List[dict]:
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

        from datetime import datetime

        def parse_time(t_str):
            if not t_str:
                return datetime.max

            formats = [
                "%Y-%m-%d %H:%M",
                "%Y-%m-%d",
                "%H:%M",
            ]

            for fmt in formats:
                try:
                    return datetime.strptime(t_str, fmt)
                except ValueError:
                    continue

            return datetime.max

        acts.sort(key=lambda x: parse_time(x.get("time", "")))

        return acts

    @rx.var
    def upcoming_activities(self) -> List[dict]:
        return self.filtered_activities[:5]

    @rx.var
    def my_activities_list(self) -> List[dict]:
        if not self.current_user_id:
            return []

        return [
            a
            for a in self.activities
            if a.get("creator_id") == self.current_user_id
            or (a.get("participants") and self.current_user_id in a.get("participants"))
        ]

    def filter_by_location(self, location: str):
        self.search_query = location

    def filter_by_distance_label(self, distance: str):
        self.filter_distance = distance

    def clear_redirect(self):
        self.redirect_path = ""

    def on_google_login_success(self, response: dict):
        import base64

        credential = response.get("credential", "")
        if credential:
            try:
                payload = credential.split(".")[1]
                payload += "=" * (4 - len(payload) % 4)
                decoded = base64.urlsafe_b64decode(payload)
                user_info = json.loads(decoded)

                self.current_user_name = user_info.get(
                    "name", user_info.get("given_name", "NMH Student")
                )
                self.current_user_email = user_info.get("email", "student@nmh.edu")
                self.current_user_picture = user_info.get("picture", "")

                user_sub = user_info.get("sub", "")
                if user_sub:
                    self.current_user_id = (
                        int(hashlib.sha256(user_sub.encode()).hexdigest(), 16) % 10**8
                    )
                else:
                    self.current_user_id = 1

                from app.config import Config

                config = Config()
                self.is_admin = self.current_user_email in config.ADMIN_EMAILS

                user_file = Path(__file__).parent.parent / "data" / "user.json"
                users = []
                if user_file.exists():
                    try:
                        with open(user_file, "r") as f:
                            data = json.load(f)
                            users = data if isinstance(data, list) else []
                    except:
                        users = []

                user_exists = False
                for u in users:
                    if u.get("user_id") == self.current_user_id:
                        u["email"] = self.current_user_email
                        u["name"] = self.current_user_name
                        u["picture"] = self.current_user_picture
                        u["is_admin"] = self.is_admin
                        user_exists = True
                        break

                if not user_exists:
                    users.append(
                        {
                            "user_id": self.current_user_id,
                            "email": self.current_user_email,
                            "name": self.current_user_name,
                            "picture": self.current_user_picture,
                            "is_admin": self.is_admin,
                        }
                    )

                with open(user_file, "w") as f:
                    json.dump(users, f, indent=2)

            except Exception:
                self.current_user_name = "NMH Student"
                self.current_user_email = "student@nmh.edu"
                self.current_user_id = 1
                self.is_admin = False
        else:
            self.current_user_name = "NMH Student"
            self.current_user_email = "student@nmh.edu"
            self.current_user_id = 1
            self.is_admin = False

        self.is_authenticated = True
        self.message = "Logged in successfully!"
        self.message_type = "success"

    def check_login(self):
        if not self.is_authenticated:
            return rx.redirect("/")

    def logout(self):
        self.current_user_id = None
        self.current_user_name = ""
        self.current_user_email = ""
        self.current_user_picture = ""
        self.is_authenticated = False
        self.is_admin = False
        self.redirect_path = "/"
        self.message = "Logged out."
        self.message_type = "info"
        return rx.redirect("/")
