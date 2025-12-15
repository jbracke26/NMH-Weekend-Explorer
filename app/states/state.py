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
    activity_log_location: bool = False
    activity_latitude: str = ""
    activity_longitude: str = ""
    use_map_for_location: bool = False
    activity_needs_chaperone: bool = False

    message: str = ""
    message_type: str = "info"
    
    intended_role: str = ""  # "student" or "teacher"

    current_activity: dict = {}
    editing_activity_id: Optional[int] = None

    def get_user_name(self, user_id: int) -> str:
        """Get user name from user_id for display purposes."""
        user_file = Path(__file__).parent.parent / "data" / "user.json"
        if user_file.exists():
            try:
                with open(user_file, "r") as f:
                    users = json.load(f)
                    for u in users:
                        if u.get("user_id") == user_id:
                            return u.get("name", f"User {user_id}")
            except:
                pass
        return f"User {user_id}"

    @rx.var
    def is_teacher(self) -> bool:
        """Check if current user is a teacher."""
        if not self.is_authenticated or not self.current_user_email:
            return False
        from app.config import Config

        config = Config()
        return self.current_user_email in config.TEACHER_EMAILS

    @rx.var
    def current_activity_creator_name(self) -> str:
        """Get the creator name for the current activity."""
        if not self.current_activity:
            return ""
        creator_id = self.current_activity.get("creator_id")
        if creator_id:
            return self.get_user_name(creator_id)
        return "Unknown"

    @rx.var
    def current_activity_participant_names(self) -> list[str]:
        """Get participant names for the current activity."""
        if not self.current_activity:
            return []
        participants = self.current_activity.get("participants", [])
        if not isinstance(participants, list):
            return []
        return [self.get_user_name(p) for p in participants]

    def set_activity_log_location(self, value: bool):
        self.activity_log_location = value

    def set_activity_latitude(self, value: str):
        self.activity_latitude = value

    def set_activity_longitude(self, value: str):
        self.activity_longitude = value

    def set_use_map_for_location(self, value: bool):
        self.use_map_for_location = value
        # Reset map coordinates when turning off map
        if not value:
            self.activity_latitude = ""
            self.activity_longitude = ""
            self.activity_log_location = False
    
    def toggle_use_map_for_location(self):
        """Toggle the use_map_for_location state."""
        self.use_map_for_location = not self.use_map_for_location
        # Reset map coordinates when turning off map
        if not self.use_map_for_location:
            self.activity_latitude = ""
            self.activity_longitude = ""
            self.activity_log_location = False

    def reset_create_activity_form(self):
        """Reset all create activity form fields to default values."""
        self.use_map_for_location = False
        self.activity_log_location = False
        self.activity_latitude = ""
        self.activity_longitude = ""

    def on_create_activity_page_load(self):
        """Called when create activity page loads - reset form fields."""
        self.hide_header_login = True
        self.use_map_for_location = False
        self.activity_log_location = False
        self.activity_latitude = ""
        self.activity_longitude = ""

    def set_location_from_map(self, lat: str, lng: str):
        """Set location coordinates from map click."""
        self.activity_latitude = lat
        self.activity_longitude = lng
        self.activity_log_location = True

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

    def toggle_chaperone(self):
        if not self.is_authenticated:
            self.message = "Please log in to manage chaperones."
            self.message_type = "error"
            return

        if not self.is_teacher:
            self.message = "Only teachers can sign up as chaperones."
            self.message_type = "error"
            return

        if not self.current_activity:
            return

        try:
            acts = load_activities()
            for a in acts:
                if a.id == self.current_activity["id"]:
                    current_chaperone = getattr(a, "chaperone_id", None)
                    if current_chaperone == self.current_user_id:
                        a.chaperone_id = None
                        a.admin_signed_up = False
                        a.chaperone_name = ""
                        self.current_activity["chaperone_id"] = None
                        self.current_activity["admin_signed_up"] = False
                        self.current_activity["chaperone_name"] = ""
                        self.message = "You are no longer chaperoning this activity."
                    else:
                        a.chaperone_id = self.current_user_id
                        a.admin_signed_up = True
                        a.chaperone_name = self.current_user_name
                        self.current_activity["chaperone_id"] = self.current_user_id
                        self.current_activity["admin_signed_up"] = True
                        self.current_activity["chaperone_name"] = self.current_user_name
                        self.message = "You are now chaperoning this activity."
                    self.message_type = "success"
                    save_activities(acts)
                    self.load_activities()
                    return
        except Exception as e:
            self.message = f"Error updating chaperone: {e}"
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
                "latitude": a.latitude,
                "longitude": a.longitude,
                "max_participants": a.max_participants,
                "participants": a.participants or [],
                "participants_count": len(a.participants) if a.participants else 0,
                "creator_id": a.creator_id,
                "admin_signed_up": getattr(a, "admin_signed_up", False),
                "chaperone_id": getattr(a, "chaperone_id", None),
                "needs_chaperone": getattr(a, "needs_chaperone", False),
                "chaperone_name": getattr(a, "chaperone_name", ""),
                "latitude": getattr(a, "latitude", None),
                "longitude": getattr(a, "longitude", None),
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

            if (
                self.activity_max_participants
                and self.activity_max_participants.strip()
            ):
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

            # parse coordinates if provided (only if map was used)
            latitude = None
            longitude = None
            if self.use_map_for_location:
                # Get coordinates from state first
                lat_str = str(self.activity_latitude).strip() if self.activity_latitude else ""
                lng_str = str(self.activity_longitude).strip() if self.activity_longitude else ""
                
                # Debug logging
                print(f"DEBUG create_activity - use_map_for_location: {self.use_map_for_location}")
                print(f"DEBUG create_activity - activity_latitude: '{self.activity_latitude}' (type: {type(self.activity_latitude)})")
                print(f"DEBUG create_activity - activity_longitude: '{self.activity_longitude}' (type: {type(self.activity_longitude)})")
                print(f"DEBUG create_activity - lat_str: '{lat_str}', lng_str: '{lng_str}'")
                
                # If state values are empty, coordinates might not have been synced yet
                # This is a fallback - in normal operation, state should have the values
                if not lat_str or not lng_str:
                    print(f"DEBUG: State values empty, coordinates may not have been synced")
                
                if lat_str and lng_str:
                    try:
                        # Validate that they are valid numbers and convert to float
                        latitude = float(lat_str)
                        longitude = float(lng_str)
                        print(f"DEBUG: Saving coordinates from state - lat: {latitude}, lng: {longitude}")
                    except ValueError:
                        print(f"DEBUG: Invalid coordinates - lat: {lat_str}, lng: {lng_str}")
                        latitude = None
                        longitude = None
                else:
                    print(f"DEBUG: Coordinates empty or invalid - lat: '{lat_str}', lng: '{lng_str}'")

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
                admin_signed_up=False,
                chaperone_id=None,
                needs_chaperone=self.activity_needs_chaperone,
                chaperone_name="",
                latitude=latitude,
                longitude=longitude,
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
            self.activity_log_location = False
            self.activity_latitude = ""
            self.activity_longitude = ""
            self.use_map_for_location = False

            self.message = "Activity created successfully!"
            self.message_type = "success"

            return rx.redirect("/explore")
        except Exception as e:
            self.message = f"Error creating activity: {str(e)}"
            self.message_type = "error"

    def clear_activity_form(self):
        """Clear all activity form fields."""
        self.editing_activity_id = None
        self.activity_title = ""
        self.activity_description = ""
        self.activity_category = "Other"
        self.activity_location = ""
        self.activity_distance = ""
        self.activity_date = ""
        self.activity_time = "10:00"
        self.activity_max_participants = ""
        self.activity_log_location = False
        self.activity_latitude = ""
        self.activity_longitude = ""
        self.activity_needs_chaperone = False

    def load_activity_for_edit(self):
        """Load activity data into form fields for editing."""
        # Check authentication first
        if not self.is_authenticated:
            return

        activity_id = self.router.page.params.get("activity_id")
        if not activity_id:
            self.message = "No activity ID provided"
            self.message_type = "error"
            return

        try:
            aid = int(activity_id)
            acts = load_activities()

            for a in acts:
                if a.id == aid:
                    # Check permissions - only creator or admin can edit
                    # Admins can edit any activity
                    if not self.is_admin and a.creator_id != self.current_user_id:
                        self.message = (
                            "You don't have permission to edit this activity."
                        )
                        self.message_type = "error"
                        return

                    # Load activity data into form fields
                    self.editing_activity_id = aid
                    self.activity_title = a.title
                    self.activity_description = a.description
                    self.activity_category = a.category
                    self.activity_location = a.location
                    self.activity_distance = a.distance

                    # Parse time string back into date and time components
                    if a.time:
                        time_parts = a.time.strip().split()
                        if len(time_parts) >= 2:
                            self.activity_date = time_parts[0]
                            self.activity_time = time_parts[1]
                        elif len(time_parts) == 1:
                            # Could be just date or just time
                            if ":" in time_parts[0]:
                                self.activity_time = time_parts[0]
                            else:
                                self.activity_date = time_parts[0]

                    self.activity_max_participants = (
                        str(a.max_participants) if a.max_participants else ""
                    )

                    # load map location if available
                    self.activity_needs_chaperone = getattr(a, "needs_chaperone", False)
                    latitude = getattr(a, "latitude", None)
                    longitude = getattr(a, "longitude", None)

                    if latitude and longitude:
                        self.activity_log_location = True
                        self.activity_latitude = str(latitude)
                        self.activity_longitude = str(longitude)
                    else:
                        self.activity_log_location = False
                        self.activity_latitude = ""
                        self.activity_longitude = ""

                    return

            self.message = "Activity not found."
            self.message_type = "error"
        except Exception as e:
            self.message = f"Error loading activity: {str(e)}"
            self.message_type = "error"

    def update_activity(self):
        """Update an existing activity with new data."""
        if not self.editing_activity_id:
            self.message = "No activity selected for editing."
            self.message_type = "error"
            return

        if not self.activity_title or not self.activity_title.strip():
            self.message = "Please provide a title for the activity."
            self.message_type = "error"
            return

        try:
            acts = load_activities()
            activity_found = False

            for a in acts:
                if a.id == self.editing_activity_id:
                    # Check permissions
                    if a.creator_id != self.current_user_id and not self.is_admin:
                        self.message = (
                            "You don't have permission to edit this activity."
                        )
                        self.message_type = "error"
                        return

                    # Update activity fields
                    a.title = self.activity_title
                    a.description = self.activity_description
                    a.category = self.activity_category
                    a.location = self.activity_location
                    a.distance = self.activity_distance

                    # Update max_participants
                    if (
                        self.activity_max_participants
                        and self.activity_max_participants.strip()
                    ):
                        try:
                            a.max_participants = int(self.activity_max_participants)
                        except ValueError:
                            a.max_participants = None
                    else:
                        a.max_participants = None

                    # Update time
                    time_str = (
                        f"{self.activity_date} {self.activity_time}".strip()
                        if self.activity_date or self.activity_time
                        else ""
                    )
                    a.time = time_str

                    # update map coordinates if enabled
                    if self.activity_log_location:
                        try:
                            a.latitude = (
                                float(self.activity_latitude)
                                if self.activity_latitude
                                else None
                            )
                            a.longitude = (
                                float(self.activity_longitude)
                                if self.activity_longitude
                                else None
                            )
                        except ValueError:
                            a.latitude = None
                            a.longitude = None
                    else:
                        a.latitude = None
                        a.longitude = None

                    a.needs_chaperone = self.activity_needs_chaperone

                    activity_found = True
                    break

            if not activity_found:
                self.message = "Activity not found."
                self.message_type = "error"
                return

            save_activities(acts)
            self.load_activities()

            # Clear form fields
            activity_id = self.editing_activity_id
            self.editing_activity_id = None
            self.activity_title = ""
            self.activity_description = ""
            self.activity_location = ""
            self.activity_distance = ""
            self.activity_date = ""
            self.activity_time = "10:00"
            self.activity_max_participants = ""

            self.message = "Activity updated successfully!"
            self.message_type = "success"

            return rx.redirect(f"/activity/{activity_id}")
        except Exception as e:
            self.message = f"Error updating activity: {str(e)}"
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
        activities = self.filtered_activities[:5]
        result = []
        for activity in activities:
            activity_copy = dict(activity)
            participants = activity_copy.get("participants", [])
            if isinstance(participants, list):
                activity_copy["participants_count"] = len(participants)
            else:
                activity_copy["participants_count"] = 0
            activity_copy["admin_signed_up"] = activity_copy.get(
                "admin_signed_up", False
            )
            result.append(activity_copy)
        return result

    @rx.var
    def filtered_activities_json(self) -> str:
        """Return filtered activities as JSON string for use in JavaScript."""
        import json

        return json.dumps(self.filtered_activities)

    @rx.var
    def my_activities_list(self) -> List[dict]:
        if not self.current_user_id:
            return []

        return [
            a
            for a in self.activities
            if a.get("creator_id") == self.current_user_id
            or (a.get("participants") and self.current_user_id in a.get("participants"))
            or a.get("chaperone_id") == self.current_user_id
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
        
        # Check if user logged in with the correct role button
        if self.intended_role:
            from app.config import Config
            config = Config()
            
            if self.intended_role == "teacher" and self.current_user_email not in config.TEACHER_EMAILS:
                self.message = "You logged in as a teacher but your email isn't in the teacher list. You're still logged in as a student."
                self.message_type = "error"
            elif self.intended_role == "student" and self.current_user_email in config.TEACHER_EMAILS:
                self.message = "You logged in as a student but you're actually a teacher. You're still logged in with teacher privileges."
                self.message_type = "error"
            else:
                self.message = "Logged in successfully!"
                self.message_type = "success"
        else:
            self.message = "Logged in successfully!"
            self.message_type = "success"

    def on_student_login_success(self, response: dict):
        """Handle student login button click"""
        self.intended_role = "student"
        self.on_google_login_success(response)
    
    def on_teacher_login_success(self, response: dict):
        """Handle teacher login button click"""
        self.intended_role = "teacher"
        self.on_google_login_success(response)
    
    def set_message(self, message: str):
        """Set or clear the message"""
        self.message = message
        if not message:
            self.message_type = "info"

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
