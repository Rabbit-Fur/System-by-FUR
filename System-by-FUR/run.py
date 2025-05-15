import atexit
import logging
import os
import signal
import sys
import threading

from bot.bot_main import main as start_discord_bot
from init_db_core import init_db
from main_app import create_app

# === Datenbank-Initialisierung ===
try:
    init_db()
    print("✅ Datenbank-Initialisierung erfolgreich.")
except Exception as e:
    print(f"❌ Fehler bei der Datenbank-Initialisierung: {e}")
    sys.exit(1)

# === Logging Setup ===
logging.basicConfig(
    filename="app.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# === Flask App Setup ===
app = create_app()


def run_web():
    """Startet den Webserver (Flask)."""
    try:
        port = int(os.getenv("PORT", 5000))
        logging.info(f"🌐 Webserver läuft auf http://localhost:{port}")
        app.run(host="0.0.0.0", port=port, debug=False)
    except Exception as e:
        logging.error(f"❌ Webserver-Fehler: {e}", exc_info=True)


def run_bot():
    """Startet den Discord-Bot."""
    try:
        logging.info("🤖 Discord-Bot wird gestartet...")
        start_discord_bot()
    except Exception as e:
        logging.error(f"❌ Discord-Bot-Fehler: {e}", exc_info=True)


def cleanup():
    """Aufräumen bei Beenden der App."""
    logging.info("🔻 Anwendung wird beendet...")


def signal_handler(sig, frame):
    logging.info("🛑 SIGINT empfangen. Beende Anwendung...")
    sys.exit(0)


# === Startpunkt der Anwendung ===
if __name__ == "__main__":
    atexit.register(cleanup)
    signal.signal(signal.SIGINT, signal_handler)

    # Starte Discord-Bot in eigenem Thread
    threading.Thread(target=run_bot, daemon=True).start()

    # Starte Webserver im Hauptthread
    run_web()
