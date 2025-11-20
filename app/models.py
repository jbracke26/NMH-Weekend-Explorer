from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import date, time, datetime

from sqlmodel import SQLModel

Base = SQLModel
class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    email: str
    password_hash: str
    is_admin: bool = False

    def check_password(self, password: str) -> bool:
        return password == self.password_hash

class Activity(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    description: str | None = ""
    date: date
    time: time
    location_name: str
    latitude: float = 0.0
    longitude: float = 0.0
    max_participants: Optional[int] = None
    creator_id: int

    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class Participation(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int
    activity_id: int
