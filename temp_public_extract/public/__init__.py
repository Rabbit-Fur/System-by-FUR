from . import routes
from flask import Blueprint

public_bp = Blueprint(
    'public',
    __name__,
    template_folder='templates/public',
    # Nutzt globale static Files
    url_prefix='/'  # Kein Prefix für öffentliche Hauptseiten
)

# Routen importieren
