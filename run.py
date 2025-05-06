import atexit
import logging
import os
import signal
import sys
import threading

from app import create_app
from bot.bot_main import main as start_discord_bot
from init_db_core import init_db  # ✅ Korrekt: aus init_db_core.py importieren

# === Datenbank Initialisieren ===
try:
    init_db()
    print("✅ Datenbank-Initialisierung erfolgreich.")
except Exception as e:
    print("❌ Fehler bei Datenbank-Initialisierung.")
    sys.exit(1)

# === Logging Setup ===
logging.basicConfig(filename="app.log", level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# === Flask App Setup ===
app = create_app()


def run_web():
    """Function run_web."""
    try:
        port = int(os.getenv("PORT", 5000))
        app.run(host="0.0.0.0", port=port, debug=False)
    except Exception as e:
        logging.error(f"❌ Webserver Error: {e}", exc_info=True)


def run_bot():
    """Function run_bot."""
    try:
        start_discord_bot()
    except Exception as e:
        logging.error(f"❌ Discord-Bot Error: {e}", exc_info=True)


def cleanup():
    """Function cleanup."""
    logging.info("🔻 Cleanup eingeleitet.")


def signal_handler(sig, frame):
    """Function signal_handler."""
    logging.info("🛑 SIGINT empfangen. Beende Anwendung...")
    sys.exit(0)


# === Startlogik ===
if __name__ == "__main__":
    atexit.register(cleanup)
    signal.signal(signal.SIGINT, signal_handler)

    # Starte Discord-Bot im Hintergrund
    threading.Thread(target=run_bot, daemon=True).start()

    # Starte Flask-Webserver
    run_web()

# trigger-ci
