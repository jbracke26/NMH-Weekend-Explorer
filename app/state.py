import reflex as rx
from datetime import date, datetime
from typing import List, Optional
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models import Base, User, Activity, Participation
from app.config import Config

config = Config()
engine = create_engine(config.DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
Base.metadata.create_all(bind=engine)

class State(rx.State):
    current_user_id: Optional[int] = None
    current_user_name: str = ""
    current_user_email: str = ""
    is_admin: bool = False
    is_authenticated: bool = False
    
    activities: List[dict] = []
    redirect_path: str = ""
    
    email: str = ""
    password: str = ""
    name: str = ""
    
    filter_date_from: Optional[date] = None
    filter_date_to: Optional[date] = None
    sort_by: str = "date"
    
    activity_title: str = ""
    activity_description: str = ""
    activity_date: date = date.today()
    activity_time: str = "10:00"
    activity_location_name: str = ""
    activity_latitude: float = 0.0
    activity_longitude: float = 0.0
    activity_max_participants: Optional[int] = None
    
    message: str = ""
    message_type: str = "info"
    
    def get_db(self):
        return SessionLocal()
    
    def login(self):
        db = self.get_db()
        try:
            user = db.query(User).filter(User.email == self.email).first()
            if user and user.check_password(self.password):
                self.current_user_id = user.id
                self.current_user_name = user.name
                self.current_user_email = user.email
                self.is_admin = user.is_admin
                self.is_authenticated = True
                self.message = "Logged in successfully!"
                self.message_type = "success"
                self.redirect_path = "/"
            else:
                self.message = "Invalid email or password."
                self.message_type = "error"
        except Exception as e:
            self.message = f"Error: {str(e)}"
            self.message_type = "error"
        finally:
            db.close()
    
    def logout(self):
        self.current_user_id = None
        self.current_user_name = ""
        self.current_user_email = ""
        self.is_admin = False
        self.is_authenticated = False
        self.message = "Logged out successfully!"
        self.message_type = "info"
        self.redirect_path = "/"
    
    def load_activities(self):
        db = self.get_db()
        try:
            query = db.query(Activity)
            if self.filter_date_from:
                query = query.filter(Activity.date >= self.filter_date_from)
            if self.filter_date_to:
                query = query.filter(Activity.date <= self.filter_date_to)
            
            if self.sort_by == "date":
                query = query.order_by(Activity.date, Activity.time)
            elif self.sort_by == "created_at":
                query = query.order_by(Activity.created_at.desc())
            
            activities_list = query.all()
            self.activities = [{
                'id': a.id,
                'title': a.title,
                'description': a.description or '',
                'date': str(a.date),
                'time': str(a.time),
                'location_name': a.location_name,
                'latitude': a.latitude,
                'longitude': a.longitude,
                'max_participants': a.max_participants,
                'creator_id': a.creator_id
            } for a in activities_list]
        except Exception as e:
            self.message = f"Error loading activities: {str(e)}"
            self.message_type = "error"
        finally:
            db.close()
    
    def create_activity(self):
        if not self.is_authenticated:
            self.message = "You must be logged in to create an activity."
            self.message_type = "error"
            return
        
        db = self.get_db()
        try:
            from datetime import time as dt_time
            time_parts = self.activity_time.split(":")
            activity_time = dt_time(int(time_parts[0]), int(time_parts[1]))
            
            activity = Activity(
                title=self.activity_title,
                description=self.activity_description,
                date=self.activity_date,
                time=activity_time,
                location_name=self.activity_location_name,
                latitude=self.activity_latitude,
                longitude=self.activity_longitude,
                max_participants=self.activity_max_participants,
                creator_id=self.current_user_id
            )
            db.add(activity)
            db.commit()
            activity_id = activity.id
            self.message = "Activity created successfully!"
            self.message_type = "success"
            self.redirect_path = f"/activity/{activity_id}"
        except Exception as e:
            db.rollback()
            self.message = f"Error creating activity: {str(e)}"
            self.message_type = "error"
        finally:
            db.close()
    
    def join_activity(self, activity_id: int):
        if not self.is_authenticated:
            self.message = "You must be logged in to join an activity."
            self.message_type = "error"
            return
        
        db = self.get_db()
        try:
            existing = db.query(Participation).filter_by(user_id=self.current_user_id, activity_id=activity_id).first()
            if existing:
                self.message = "You are already participating in this activity."
                self.message_type = "info"
                return
            
            activity = db.query(Activity).get(activity_id)
            if activity and activity.max_participants:
                current_count = db.query(Participation).filter_by(activity_id=activity_id).count()
                if current_count >= activity.max_participants:
                    self.message = "Activity is full."
                    self.message_type = "warning"
                    return
            
            participation = Participation(user_id=self.current_user_id, activity_id=activity_id)
            db.add(participation)
            db.commit()
            self.message = "You joined the activity!"
            self.message_type = "success"
        except Exception as e:
            db.rollback()
            self.message = f"Error joining activity: {str(e)}"
            self.message_type = "error"
        finally:
            db.close()
    
    def leave_activity(self, activity_id: int):
        if not self.is_authenticated:
            return
        
        db = self.get_db()
        try:
            participation = db.query(Participation).filter_by(user_id=self.current_user_id, activity_id=activity_id).first()
            if participation:
                db.delete(participation)
                db.commit()
                self.message = "You left the activity."
                self.message_type = "info"
        except Exception as e:
            db.rollback()
            self.message = f"Error leaving activity: {str(e)}"
            self.message_type = "error"
        finally:
            db.close()
    
    def update_activity(self, activity_id: int):
        if not self.is_authenticated:
            self.message = "You must be logged in to update an activity."
            self.message_type = "error"
            return
        
        db = self.get_db()
        try:
            activity = db.query(Activity).get(activity_id)
            if not activity:
                self.message = "Activity not found."
                self.message_type = "error"
                return
            
            if activity.creator_id != self.current_user_id and not self.is_admin:
                self.message = "You do not have permission to edit this activity."
                self.message_type = "warning"
                return
            
            from datetime import time as dt_time
            time_parts = self.activity_time.split(":")
            activity_time = dt_time(int(time_parts[0]), int(time_parts[1]))
            
            activity.title = self.activity_title
            activity.description = self.activity_description
            activity.date = self.activity_date
            activity.time = activity_time
            activity.location_name = self.activity_location_name
            activity.latitude = self.activity_latitude
            activity.longitude = self.activity_longitude
            activity.max_participants = self.activity_max_participants
            activity.updated_at = datetime.utcnow()
            
            db.commit()
            self.message = "Activity updated successfully!"
            self.message_type = "success"
            self.redirect_path = f"/activity/{activity_id}"
        except Exception as e:
            db.rollback()
            self.message = f"Error updating activity: {str(e)}"
            self.message_type = "error"
        finally:
            db.close()

