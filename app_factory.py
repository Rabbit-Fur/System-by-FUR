# app_factory.py
from flask import Flask, send_from_directory

def create_app():
    app = Flask(__name__)

    @app.route("/health")
    def health():
        return "ok", 200

    @app.route("/.well-known/<path:filename>")
    def well_known(filename):
        return send_from_directory(".well-known", filename)

    # ➕ NEU: Root-Route für /
    @app.route("/")
    def index():
        return "<h1>🐇 FUR SYSTEM ONLINE</h1><p>Webserver aktiv – System bereit.</p>"

    return app
