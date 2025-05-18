from flask import Flask
from flask_babel import Babel

def create_app():
    app = Flask(__name__)
    app.config.from_pyfile("config.py")

    # Lokalisierung aktivieren
    babel = Babel(app)

    # Blueprints laden
    try:
        from landing_route import landing_bp
        from static_routes import static_bp

        app.register_blueprint(landing_bp)
        app.register_blueprint(static_bp)
    except Exception as e:
        app.logger.warning(f"Blueprint registration failed: {e}")

    return app
