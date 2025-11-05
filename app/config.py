import os
from pathlib import Path

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "super-secret-key")
    WTF_CSRF_ENABLED = True
    SESSION_COOKIE_NAME = os.getenv("SESSION_COOKIE_NAME", "routemaster_session")
    API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000")
    APP_NAME = os.getenv("APP_NAME", "RouteMaster Frontend")
    PERMANENT_SESSION_LIFETIME = int(os.getenv("SESSION_LIFETIME", 60 * 60 * 4))
