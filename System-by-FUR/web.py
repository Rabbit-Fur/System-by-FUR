# web.py
from app_factory import create_app

app = create_app()

if __name__ == "__main__":
    import os
    from env_helpers import get_env_str

    port = int(get_env_str("PORT", default="5000"))
    debug = get_env_str("FLASK_ENV", default="development") == "development"

    print(f"🌐 Starte Flask-App auf http://localhost:{port} (Debug={debug})")
    app.run(host="0.0.0.0", port=port, debug=debug)
