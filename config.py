from datetime import timedelta
from dotenv import load_dotenv
import os


# Lade Umgebungsvariablen aus .env Datei
basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))


class Config:
    # --- Flask Core ---
    SECRET_KEY = os.environ.get(
        'SECRET_KEY') or 'dev-secret-key-CHANGE-ME-IN-PROD'
    FLASK_ENV = os.environ.get('FLASK_ENV', 'development')
    DEBUG = FLASK_ENV == 'development'

    # --- Security ---
    SESSION_COOKIE_SECURE = FLASK_ENV == 'production'
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'  # 'Strict' ist sicherer, wenn möglich
    PERMANENT_SESSION_LIFETIME = timedelta(
        minutes=int(
            os.environ.get(
                'SESSION_LIFETIME_MINUTES',
                60)))  # Default 1h
    WTF_CSRF_ENABLED = True
    # Optional: Rate Limiting
    # RATELIMIT_STORAGE_URL = os.environ.get('REDIS_URL', 'memory://')

    # --- Database ---
    DATABASE_PATH = os.path.join(
        basedir, 'data', 'admin_users.db')  # Zentrale DB

    # --- Discord Integration ---
    DISCORD_WEBHOOK_URL = os.environ.get(
        'DISCORD_WEBHOOK_URL')  # Für Event Posts
    DISCORD_TOKEN = os.environ.get('DISCORD_TOKEN')             # Für Bot
    DISCORD_GUILD_ID = int(os.environ.get(
        'DISCORD_GUILD_ID') or 0)  # Bot Kontext
    # Default Channel für Reminders etc.
    DISCORD_CHANNEL_ID = int(os.environ.get('DISCORD_CHANNEL_ID') or 0)
    # Optional: Discord OAuth für login
    # DISCORD_CLIENT_ID = os.environ.get('DISCORD_CLIENT_ID')
    # DISCORD_CLIENT_SECRET = os.environ.get('DISCORD_CLIENT_SECRET')
    # DISCORD_REDIRECT_URI = os.environ.get('DISCORD_REDIRECT_URI')

    # --- Celery (Falls für Cron/Background Tasks genutzt) ---
    # CELERY_BROKER_URL = os.environ.get('CELERY_BROKER_URL', 'redis://localhost:6379/0')
    # CELERY_RESULT_BACKEND = os.environ.get('CELERY_RESULT_BACKEND', 'redis://localhost:6379/0')

    # --- Internationalization (i18n via JSON) ---
    SUPPORTED_LANGUAGES = [
        'en',
        'de',
        'vi',
        'tr',
        'it',
        'cs',
        'es',
        'fr',
        'pl',
        'ru']
    DEFAULT_LANGUAGE = 'en'

    # --- Poster & Medal Generation ---
    STATIC_FOLDER = os.path.join(basedir, 'static')
    POSTER_OUTPUT_REL_PATH = 'temp'  # Relativ zu static
    MEDAL_OUTPUT_REL_PATH = 'medals'  # Relativ zu static
    CHAMPION_OUTPUT_REL_PATH = 'champions'  # Relativ zu static

    POSTER_FONT_TITLE_PATH = os.path.join(STATIC_FOLDER, "fonts/FUR-Bold.ttf")
    POSTER_FONT_TEXT_PATH = os.path.join(
        STATIC_FOLDER, "fonts/FUR-Regular.ttf")
    POSTER_BG_DEFAULT_PATH = os.path.join(STATIC_FOLDER, "img/fur_bg.jpg")
    POSTER_BG_TEMPLATES = {  # Schlüssel: Event-Typ -> Wert: Pfad relativ zu static/
        'meeting':   'img/meeting_bg.jpg',
        'battle':    'img/battle_bg.jpg',
        'training':  'img/training_bg.jpg',
        'party':     'img/party_bg.jpg',
    }
    MOTTOS = [
        "Forged in Unity",
        "Strength Through Honor",
        "We Never Give Up",
        "Rise Together",
        "Fire in Our Veins",
        "Glory Awaits",
        "Wolves Among Sheep"]
    IMG_WIDTH, IMG_HEIGHT = 1280, 720
    TEXT_COLOR = (255, 215, 0)
    ROLE_COLOR = (255, 100, 100)
    CHAMPION_TEXT_COLOR = (255, 215, 0)
    CHAMPION_USERNAME_COLOR = (255, 255, 255)
    CHAMPION_SUBTEXT_COLOR = (200, 200, 200)
    CHAMPION_BG_COLOR = "  #0a0a0a"
    MEDAL_SIZE = (150, 150)
    MEDAL_POSITION = (1000, 50)  # Position für Medaillen-Overlay

    # --- Upload Settings ---
    UPLOAD_FOLDER = os.path.join(STATIC_FOLDER, 'uploads')
    ALLOWED_EXTENSIONS = {'jpg', 'png'}
    MAX_CONTENT_LENGTH = 2 * 1024 * 1024  # 2 MB Limit

    # --- Bot Specific ---
    BOT_PREFIX = '!'  # Oder anderes Prefix, falls benötigt
    EVENT_REMINDER_CHANNEL = 'events'  # Name des Channels für Reminder
    # Name des Channels für Champion-Posts
    CHAMPION_ANNOUNCEMENT_CHANNEL = 'announcements'

    # --- Base URL (Wichtig für externe Links in Discord Posts etc.) ---
    BASE_URL = os.environ.get(
        'BASE_URL',
        'http://localhost:5000')  # Anpassen für Produktion!
