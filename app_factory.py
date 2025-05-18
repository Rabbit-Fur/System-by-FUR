# app_factory.py
from flask import Flask, render_template, send_from_directory
from web.routes.main_routes import main_bp
from web.routes.admin_routes import admin_bp
from web.routes.public_routes import public_bp
from web.routes.member_routes import member_bp

def create_app():
    app = Flask(__name__)
    app.config.from_pyfile("config.py")

    # Register Blueprints
    app.register_blueprint(main_bp)
    app.register_blueprint(admin_bp, url_prefix="/admin")
    app.register_blueprint(public_bp, url_prefix="/public")
    app.register_blueprint(member_bp, url_prefix="/members")

    # Healthcheck
    @app.route("/health")
    def health():
        return "ok", 200

    # ACME-Challenge & Zertifikate
    @app.route("/.well-known/<path:filename>")
    def well_known(filename):
        return send_from_directory(".well-known", filename)

    # Root-Route für /
    @app.route("/")
    def index():
        return render_template("public/landing.html")

    return app
