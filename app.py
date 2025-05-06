import logging
import os
import sqlite3

from flask import Flask, g, redirect, render_template, request, session, url_for
from flask_wtf.csrf import CSRFProtect

from admin import admin_bp
from api import api_bp
from config import Config
from leaderboard import leaderboard_bp
from public import public_bp
from utils.i18n import get_translator

# === Logging Setup ===
logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)


# === Database Helper ===
def get_db():
    """Stellt eine Datenbankverbindung für den aktuellen Request her."""
    if "db" not in g:
        try:
            db_path = Config.DATABASE_PATH
            os.makedirs(os.path.dirname(db_path), exist_ok=True)
            g.db = sqlite3.connect(db_path, timeout=10)
            g.db.row_factory = sqlite3.Row
            g.db.execute("PRAGMA foreign_keys = ON")
            g.db.execute("PRAGMA journal_mode=WAL")
            g.db.execute("PRAGMA busy_timeout = 5000")
            log.debug("Database connection established.")
        except sqlite3.Error as e:
            log.error(f"Database connection failed: {e}", exc_info=True)
            raise ConnectionError("Could not connect to the database.") from e
    return g.db


def close_db(e=None):
    db = g.pop("db", None)
    if db is not None:
        db.close()
        log.debug("Database connection closed.")


# === App Factory ===
def create_app(config_class=Config):
    """Erstellt und konfiguriert die Flask App."""
    app = Flask(__name__, static_folder="static", template_folder=os.path.join(os.path.dirname(__file__), "templates"))
    app.config.from_object(config_class)

    CSRFProtect(app)

    # Register Blueprints
    app.register_blueprint(admin_bp)
    app.register_blueprint(api_bp)
    app.register_blueprint(leaderboard_bp)
    app.register_blueprint(public_bp)

    # Teardown
    app.teardown_appcontext(close_db)

    # Healthcheck Route
    @app.route("/health")
    def healthcheck():
        return "OK", 200

    # i18n / Translator
    @app.context_processor
    def inject_translation_vars():
        selected_lang = request.args.get("lang", session.get("lang", Config.DEFAULT_LANGUAGE))
        if selected_lang not in Config.SUPPORTED_LANGUAGES:
            selected_lang = Config.DEFAULT_LANGUAGE
        if "lang" not in session or session["lang"] != selected_lang:
            session["lang"] = selected_lang
            log.debug(f"Language set to: {selected_lang}")
        _ = g.get("_", lambda x: x)
        return dict(_=_, lang=selected_lang, supported_languages=Config.SUPPORTED_LANGUAGES)

    # Error Handling
    @app.errorhandler(404)
    def not_found_error(error):
        log.warning(f"404 Not Found: {request.path}")
        return render_template("error.html", error_code=404, error_message="Page Not Found"), 404

    @app.errorhandler(500)
    def internal_error(error):
        log.error(f"500 Internal Server Error: {error}", exc_info=True)
        close_db()
        return render_template("error.html", error_code=500, error_message="An internal error occurred."), 500

    @app.errorhandler(ConnectionError)
    def database_connection_error(error):
        log.critical(f"Database Connection Error: {error}", exc_info=True)
        return render_template("error.html", error_code=503, error_message="Database connection error."), 503

    log.info("Flask App created successfully.")
    return app
