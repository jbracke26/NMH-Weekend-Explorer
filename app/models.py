
import json
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import List, Optional

DATA_FILE = Path(__file__).with_name("activities.json")


def _read_json() -> list[dict]:
    if not DATA_FILE.exists():
        return []
    try:
        with DATA_FILE.open("r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError:
        return []


def _write_json(data: list[dict]) -> None:
    with DATA_FILE.open("w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)


@dataclass
class Activity:
    id: int
    title: str
    description: str = ""
    category: str = "Other"
    location: str = ""
    distance: str = ""
    time: str = ""
    max_participants: Optional[str] = None
    participants: Optional[list[str]] = None
    creator_id: Optional[int] = None

    @staticmethod
    def load_all() -> List["Activity"]:
        raw_list = _read_json()
        activities: List[Activity] = []
        for raw in raw_list:
            activities.append(
                Activity(
                    id=raw.get("id", 0),
                    title=raw.get("title", ""),
                    description=raw.get("description", ""),
                    category=raw.get("category", "Other"),
                    location=raw.get("location", ""),
                    distance=raw.get("distance", ""),
                    time=raw.get("time", ""),
                    max_participants=raw.get("max_participants"),
                    participants=raw.get("participants") or [],
                    creator_id=raw.get("creator_id"),
                )
            )
        return activities

    @staticmethod
    def save_all(activities: List["Activity"]) -> None:
        _write_json([asdict(a) for a in activities])


def load_activities() -> List[Activity]:
    return Activity.load_all()


def save_activities(activities: List[Activity]) -> None:
    Activity.save_all(activities)

def join_activity(activity_id: int, user_id: int) -> None:
    activities = load_activities()
    for activity in activities:
        if activity.id == activity_id:
            if activity.participants is None:
                activity.participants = []
                activity.participants.append(user_id)
                save_activities(activities)
            if user_id not in activity.participants:
                activity.participants.append(user_id)
                save_activities(activities)
            break
