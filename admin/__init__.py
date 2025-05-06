from flask import Blueprint

admin_bp = Blueprint(
    'admin',
    __name__,
    template_folder='templates/admin',
    # FIXED: # FIXED:     static_folder='static/admin',
    url_prefix='/admin'  # Prefix hier zentral definieren
)

from . import routes
