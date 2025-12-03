
import os
from pathlib import Path
from dotenv import load_dotenv

basedir = Path(__file__).parent.parent
load_dotenv(basedir / '.env')

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    DATABASE_URL = os.environ.get('DATABASE_URL') or f'sqlite:///{basedir}/instance/app.db'
    
    GOOGLE_CLIENT_ID = os.environ.get('GOOGLE_CLIENT_ID') or ''
    GOOGLE_CLIENT_SECRET = os.environ.get('GOOGLE_CLIENT_SECRET') or ''
    GOOGLE_REDIRECT_URI = os.environ.get('GOOGLE_REDIRECT_URI') or 'http://localhost:3000/auth/google/callback'
    
    # Okta OAuth settings
    OKTA_DOMAIN = os.environ.get('OKTA_DOMAIN') or ''
    OKTA_CLIENT_ID = os.environ.get('OKTA_CLIENT_ID') or ''
    OKTA_CLIENT_SECRET = os.environ.get('OKTA_CLIENT_SECRET') or ''
    OKTA_REDIRECT_URI = os.environ.get('OKTA_REDIRECT_URI') or 'http://localhost:3000/auth/okta/callback'

