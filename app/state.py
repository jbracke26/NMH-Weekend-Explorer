import reflex as rx
from typing import Optional
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models import Base, User
from app.config import Config
import httpx

config = Config()
engine = create_engine(config.DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
Base.metadata.create_all(bind=engine)

class State(rx.State):
    current_user_id: Optional[int] = None
    current_user_name: str = ""
    current_user_email: str = ""
    current_user_picture: str = ""
    is_admin: bool = False
    is_authenticated: bool = False
    
    message: str = ""
    message_type: str = "info"
    
    def get_db(self):
        return SessionLocal()
    
    def handle_google_callback(self, code: str):
        if not code:
            self.message = "Authorization failed. No code received."
            self.message_type = "error"
            return
        
        try:
            token_url = "https://oauth2.googleapis.com/token"
            token_data = {
                "code": code,
                "client_id": config.GOOGLE_CLIENT_ID,
                "client_secret": config.GOOGLE_CLIENT_SECRET,
                "redirect_uri": config.GOOGLE_REDIRECT_URI,
                "grant_type": "authorization_code",
            }
            
            with httpx.Client() as http_client:
                token_response = http_client.post(token_url, data=token_data, timeout=30.0)
                token_response.raise_for_status()
                tokens = token_response.json()
                access_token = tokens.get("access_token")
                
                if not access_token:
                    self.message = "Failed to get access token."
                    self.message_type = "error"
                    return
                
                user_info_url = "https://www.googleapis.com/oauth2/v2/userinfo"
                headers = {"Authorization": f"Bearer {access_token}"}
                user_response = http_client.get(user_info_url, headers=headers, timeout=30.0)
                user_response.raise_for_status()
                user_info = user_response.json()
                
                google_id = user_info.get("id")
                email = user_info.get("email")
                name = user_info.get("name", "")
                picture = user_info.get("picture", "")
                
                if not email:
                    self.message = "Failed to get email from Google."
                    self.message_type = "error"
                    return
                
                db = self.get_db()
                try:
                    user = db.query(User).filter(User.google_id == google_id).first()
                    
                    if not user:
                        user = db.query(User).filter(User.email == email).first()
                        if user:
                            user.google_id = google_id
                            user.picture = picture
                            if not user.name:
                                user.name = name
                        else:
                            user = User(
                                email=email,
                                name=name,
                                google_id=google_id,
                                picture=picture,
                            )
                            db.add(user)
                    else:
                        user.email = email
                        user.name = name
                        user.picture = picture
                    
                    db.commit()
                    db.refresh(user)
                    
                    self.current_user_id = user.id
                    self.current_user_name = user.name
                    self.current_user_email = user.email
                    self.current_user_picture = user.picture or ""
                    self.is_admin = user.is_admin
                    self.is_authenticated = True
                    self.message = "Logged in successfully!"
                    self.message_type = "success"
                finally:
                    db.close()
                    
        except httpx.HTTPStatusError as e:
            self.message = f"HTTP error: {e.response.status_code}"
            self.message_type = "error"
        except Exception as e:
            self.message = f"Login error: {str(e)}"
            self.message_type = "error"
    
    def logout(self):
        self.current_user_id = None
        self.current_user_name = ""
        self.current_user_email = ""
        self.current_user_picture = ""
        self.is_admin = False
        self.is_authenticated = False
        self.message = "Logged out successfully!"
        self.message_type = "info"
    
    def clear_message(self):
        self.message = ""
        self.message_type = "info"
