import os
from datetime import timedelta
from dotenv import load_dotenv
from env_helpers import get_env_str, get_env_int, get_env_bool

# 📍 .env Pfad dynamisch bestimmbar via ENV_FILE, sonst Fallback zu ./env
basedir = os.path.abspath(os.path.dirname(__file__))
env_path = os.environ.get("ENV_FILE", os.path.join(basedir, ".env"))
load_dotenv(env_path)


class Config:
    # --- Flask Core ---
    SECRET_KEY = get_env_str("SECRET_KEY", default="dev-secret-key-CHANGE-ME-IN-PROD")
    FLASK_ENV = get_env_str("FLASK_ENV", default="development")
    DEBUG = FLASK_ENV == "development"

    # --- Security ---
    SESSION_COOKIE_SECURE = FLASK_ENV == "production"
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = "Lax"
    PERMANENT_SESSION_LIFETIME = timedelta(
        minutes=get_env_int("SESSION_LIFETIME_MINUTES", default=60)
    )
    WTF_CSRF_ENABLED = True

    # --- Database ---
    DATABASE_PATH = os.path.join(basedir, "data", "admin_users.db")

    # --- Discord Integration ---
    DISCORD_WEBHOOK_URL = get_env_str("DISCORD_WEBHOOK_URL", required=False)
    DISCORD_TOKEN = get_env_str("DISCORD_TOKEN", required=True)
    DISCORD_GUILD_ID = get_env_int("DISCORD_GUILD_ID", required=True)
    DISCORD_CHANNEL_ID = get_env_int("DISCORD_CHANNEL_ID", required=True)
    DISCORD_CLIENT_ID = get_env_str("DISCORD_CLIENT_ID", required=False)
    DISCORD_CLIENT_SECRET = get_env_str("DISCORD_CLIENT_SECRET", required=False)
    DISCORD_REDIRECT_URI = get_env_str("DISCORD_REDIRECT_URI", required=False)

    # --- Internationalization ---
    SUPPORTED_LANGUAGES = ["en", "de", "vi", "tr", "it", "cs", "es", "fr", "pl", "ru"]
    DEFAULT_LANGUAGE = "en"

    # --- Poster & Medal Generation ---
    STATIC_FOLDER = os.path.join(basedir, "static")
    POSTER_OUTPUT_REL_PATH = "temp"
    MEDAL_OUTPUT_REL_PATH = "medals"
    CHAMPION_OUTPUT_REL_PATH = "champions"

    POSTER_FONT_TITLE_PATH = os.path.join(STATIC_FOLDER, "fonts/FUR-Bold.ttf")
    POSTER_FONT_TEXT_PATH = os.path.join(STATIC_FOLDER, "fonts/FUR-Regular.ttf")
    POSTER_BG_DEFAULT_PATH = os.path.join(STATIC_FOLDER, "img/fur_bg.jpg")
    POSTER_BG_TEMPLATES = {
        "meeting": "img/meeting_bg.jpg",
        "battle": "img/battle_bg.jpg",
        "training": "img/training_bg.jpg",
        "party": "img/party_bg.jpg",
    }
    MOTTOS = [
        "Forged in Unity",
        "Strength Through Honor",
        "We Never Give Up",
        "Rise Together",
        "Fire in Our Veins",
        "Glory Awaits",
        "Wolves Among Sheep",
    ]
    IMG_WIDTH, IMG_HEIGHT = 1280, 720
    TEXT_COLOR = (255, 215, 0)
    ROLE_COLOR = (255, 100, 100)
    CHAMPION_TEXT_COLOR = (255, 215, 0)
    CHAMPION_USERNAME_COLOR = (255, 255, 255)
    CHAMPION_SUBTEXT_COLOR = (200, 200, 200)
    CHAMPION_BG_COLOR = "#0a0a0a"
    MEDAL_SIZE = (150, 150)
    MEDAL_POSITION = (1000, 50)

    # --- Upload Settings ---
    UPLOAD_FOLDER = os.path.join(STATIC_FOLDER, "uploads")
    ALLOWED_EXTENSIONS = {"jpg", "png"}
    MAX_CONTENT_LENGTH = 2 * 1024 * 1024  # 2 MB

    # --- Bot Specific ---
    BOT_PREFIX = "!"
    EVENT_REMINDER_CHANNEL = "events"
    CHAMPION_ANNOUNCEMENT_CHANNEL = "announcements"

    # --- Base URL ---
    BASE_URL = get_env_str("BASE_URL", default="http://localhost:5000")
