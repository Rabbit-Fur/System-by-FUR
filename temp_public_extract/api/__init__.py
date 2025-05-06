from flask import Blueprint

from . import routes

api_bp = Blueprint("api", __name__, url_prefix="/api")  # Zentrales Prefix für alle API Routen

# Routen importieren NACH Blueprint Definition
