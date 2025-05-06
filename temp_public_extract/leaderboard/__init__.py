from . import routes
from flask import Blueprint

leaderboard_bp = Blueprint(
    'leaderboard',
    __name__,
    template_folder='templates/leaderboard',
    # Kein eigener static folder, nutzt globale oder admin static
    url_prefix='/leaderboard'  # Erreichbar unter /leaderboard/...
)

# Routen importieren
