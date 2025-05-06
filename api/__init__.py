from flask import Blueprint

api_bp = Blueprint(
    'api',
    __name__,
    url_prefix='/api'  # Zentrales Prefix für alle API Routen
)

from . import routes
