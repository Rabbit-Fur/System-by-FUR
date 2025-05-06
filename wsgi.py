"""WSGI entrypoint for Flask app."""

import os

from app import create_app
from config import Config

# Setze FLASK_ENV auf production, falls nicht schon extern gesetzt
os.environ["FLASK_ENV"] = os.environ.get("FLASK_ENV", "production")

# Erstelle die App Instanz mit der Produktionskonfiguration
app = create_app(Config)

# Gunicorn wird diese 'app' Variable nutzen
# Kein app.run() hier!
