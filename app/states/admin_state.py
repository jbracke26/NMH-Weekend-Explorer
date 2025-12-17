import reflex as rx
from typing import List
from app.models import load_activities
from app.states.state import State
from datetime import datetime, timedelta
import json
from pathlib import Path


class AdminState(State):
    @rx.var
    def admin_stats(self) -> dict:
        if not self.is_admin:
            return {}

        activities = load_activities()

        now = datetime.utcnow()
        week_ago = now - timedelta(days=7)

        recent_count = 0
        for a in activities:
            if hasattr(a, "created_at") and a.created_at:
                try:
                    created = datetime.fromisoformat(str(a.created_at))
                    if created >= week_ago:
                        recent_count += 1
                except:
                    pass

        user_file = Path(__file__).parent.parent / "data" / "user.json"
        users = []
        if user_file.exists():
            try:
                with open(user_file, "r") as f:
                    users = json.load(f)
            except:
                users = []

        return {
            "total_activities": len(activities),
            "total_users": len(users) if isinstance(users, list) else 0,
            "recent_activities": recent_count,
        }

    @rx.var
    def all_users_list(self) -> List[dict]:
        if not self.is_admin:
            return []

        user_file = Path(__file__).parent.parent / "data" / "user.json"
        users = []
        if user_file.exists():
            try:
                with open(user_file, "r") as f:
                    data = json.load(f)
                    users = data if isinstance(data, list) else []
            except:
                users = []

        activities = load_activities()

        result = []
        for u in users:
            user_id = u.get("user_id")
            created = len([a for a in activities if a.creator_id == user_id])
            joined = len([a for a in activities if user_id in (a.participants or [])])

            result.append(
                {
                    "user_id": user_id,
                    "name": u.get("name", f"User {user_id}"),
                    "email": u.get("email", f"user{user_id}@nmh.edu"),
                    "is_admin": u.get("is_admin", False),
                    "created_activities": created,
                    "joined_activities": joined,
                }
            )

        return result

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
    def enhanced_activities(self) -> List[dict]:
        """Activities with additional information like creator names."""
        if not self.is_admin:
            return []

        result = []
        for activity in self.activities:
            enhanced = dict(activity)
            creator_id = activity.get("creator_id")
            if creator_id:
                enhanced["creator_name"] = self.get_user_name(creator_id)
            else:
                enhanced["creator_name"] = "Unknown"

            # Add participant count
            participants = activity.get("participants", [])
            enhanced["participant_count"] = (
                len(participants) if isinstance(participants, list) else 0
            )

            result.append(enhanced)
        return result

    def delete_activity_admin(self, activity_id: int):
        if not self.is_admin:
            self.message = "Unauthorized"
            self.message_type = "error"
            return

        activities = load_activities()
        activities = [a for a in activities if a.id != activity_id]

        from app.models import save_activities

        save_activities(activities)

        self.message = "Activity deleted"
        self.message_type = "success"
        self.load_activities()

    def on_admin_page_load(self):
        """Called when an admin page loads - clear messages and load activities"""
        self.clear_message()
        self.load_activities()
