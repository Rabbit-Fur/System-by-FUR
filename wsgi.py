"""WSGI entrypoint for Flask app (used by Gunicorn, uWSGI etc.)."""

import os
from app import create_app
from config import Config

# Setze FLASK_ENV nur, wenn nicht bereits gesetzt (z. B. durch Systemd, Docker, CI)
os.environ["FLASK_ENV"] = os.environ.get("FLASK_ENV", "production")

# Erstelle die Flask-App mit Produktionskonfiguration
app = create_app(Config)

# 👉 Wichtig:
# Kein app.run() hier – Gunicorn/Uwsgi übernimmt das.
