📌 Wichtig: In deiner main_app.py darfst du KEINE doppelte Blueprint-Registrierung durchführen.

➡️ Entferne folgende Zeile, falls vorhanden:
    app.register_blueprint(landing_bp)

✅ Beide Blueprints werden jetzt ausschließlich in app_factory.py registriert.
