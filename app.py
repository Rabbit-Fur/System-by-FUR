import os
# --- START OF FILE app.py ---
import os
import sqlite3
import logging
from flask import Flask, g, request, session, render_template, redirect, url_for
from flask_wtf.csrf import CSRFProtect
from config import Config
from utils.i18n import get_translator  # Importiere unseren JSON Translator

from admin import admin_bp
from api import api_bp
from leaderboard import leaderboard_bp
from public import public_bp  # Importiere den Public Blueprint

# === Logging Setup ===
# (Wird in run.py detaillierter konfiguriert)
logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)

# === Database Helper ===


def get_db():
    """Stellt eine Datenbankverbindung für den aktuellen Request her."""
    if 'db' not in g:
        try:
            db_path = Config.DATABASE_PATH
            # Stelle sicher, dass das data Verzeichnis existiert
            os.makedirs(os.path.dirname(db_path), exist_ok=True)
            g.db = sqlite3.connect(db_path, timeout=10)
            g.db.row_factory = sqlite3.Row
            g.db.execute('PRAGMA foreign_keys = ON')  # Foreign Keys aktivieren
            g.db.execute('PRAGMA journal_mode=WAL')
            g.db.execute('PRAGMA busy_timeout = 5000')
            log.debug("Database connection established.")
        except sqlite3.Error as e:
            log.error(f"Database connection failed: {e}", exc_info=True)
            raise ConnectionError("Could not connect to the database.") from e
    return g.db


def close_db(e=None):
    """Schließt die Datenbankverbindung am Ende des Requests."""
    db = g.pop('db', None)
    if db is not None:
        db.close()
        log.debug("Database connection closed.")

# === App Factory ===


def create_app(config_class=Config):
    @app.route('/health')
    def healthcheck():
        return 'OK', 200
    """Erstellt und konfiguriert die Flask App."""
    app = Flask(__name__, static_folder='static', template_folder=os.path.join(os.path.dirname(__file__), 'templates'))
    app.config.from_object(config_class)

    # --- Initialize Extensions ---
    @app.route('/health')
    def healthcheck():
        return "OK", 200

    CSRFProtect(app)

    # --- Register Blueprints ---

    app.register_blueprint(admin_bp)  # Prefix ist im Blueprint definiert
    app.register_blueprint(api_bp)   # Prefix ist im Blueprint definiert
    app.register_blueprint(leaderboard_bp)  # Prefix ist im Blueprint definiert
    # Kein Prefix für öffentliche Hauptseiten
    app.register_blueprint(public_bp)

    # --- Database Teardown ---
    app.teardown_appcontext(close_db)

    # --- i18n / Translator Setup ---
    @app.context_processor
    def inject_translation_vars():
        """Stellt Übersetzungsfunktion und Sprache für Templates bereit."""
        selected_lang = request.args.get(
            'lang', session.get(
                'lang', Config.DEFAULT_LANGUAGE))
        if selected_lang not in Config.SUPPORTED_LANGUAGES:
            selected_lang = Config.DEFAULT_LANGUAGE
        # Speichere gewählte Sprache in Session
        if 'lang' not in session or session['lang'] != selected_lang:
            session['lang'] = selected_lang
            log.debug(f"Language set to: {selected_lang}")

            _ = g.get('_', lambda x: x)

        return dict(
            _=_,
            lang=selected_lang,
            supported_languages=Config.SUPPORTED_LANGUAGES)

    # --- Basic Root Route ---
    # (Wird jetzt vom public_bp übernommen)
    # @app.route('/')
    # def index():
    #     return redirect(url_for('public.landing'))

    # --- Error Handling ---
    @app.errorhandler(404)
    def not_found_error(error):
        log.warning(f"404 Not Found: {request.path}")
        return render_template(
            'error.html', error_code=404, error_message='Page Not Found'), 404

    @app.errorhandler(500)
    def internal_error(error):
        log.error(f"500 Internal Server Error: {error}", exc_info=True)
        close_db()  # Sicherheitshalber DB schließen
        return render_template(
            'error.html', error_code=500, error_message='An internal error occurred.'), 500

    @app.errorhandler(ConnectionError)
    def database_connection_error(error):
        log.critical(f"Database Connection Error: {error}", exc_info=True)
        return render_template(
            'error.html', error_code=503, error_message='Database connection error.'), 503

    log.info("Flask App created successfully.")
    return app

# --- END OF FILE app.py ---