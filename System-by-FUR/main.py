import atexit
import locale
import logging
import signal
import sys
import threading

from dotenv import load_dotenv
from bot.bot_main import main as start_discord_bot, is_ready

from env_helpers import get_env_str, get_env_bool
import bot
import web

# ➕ NEU: GitHub-Modul importieren
from github_api import fetch_repo_info

# 🌍 Lokalisierung setzen
try:
    locale.setlocale(locale.LC_ALL, "")
    locale.setlocale(locale.LC_ALL, "en_US.UTF-8")
except locale.Error:
    pass

# 📄 .env laden
load_dotenv()

# 📋 Logging konfigurieren
logging.basicConfig(
    filename="app.log",
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)


def log_error(error_type, error):
    logging.error(f"{error_type}: {str(error)}", exc_info=True)


def start_bot():
    try:
        logging.info("🤖 Starte Discord-Bot...")
        bot.run_bot()
    except Exception as e:
        log_error("Bot", e)


def start_web():
    try:
        discord_client_id = get_env_str("DISCORD_CLIENT_ID")
        discord_client_secret = get_env_str("DISCORD_CLIENT_SECRET")
        port = int(get_env_str("PORT", default="5000"))
        logging.info(f"🌐 Starte Webserver auf Port {port}")
        web.app.run(host="0.0.0.0", port=port, debug=False)
    except Exception as e:
        log_error("Web", e)
        raise


def cleanup():
    logging.info("🔻 Anwendung wird beendet.")
    if "bot" in globals() and bot.is_ready():
        bot.close()
    web.app.config["SHUTTING_DOWN"] = True


def signal_handler(sig, frame):
    logging.info("🛑 SIGINT empfangen. Beende Anwendung...")
    if bot.is_ready():
        bot.close()
    sys.exit(0)


def check_github_repo():  # ➕ NEU: GitHub-Check beim Start
    try:
        repo_data = fetch_repo_info("Rabbit-Fur", "GGW-FUR-SYSTEM")
        logging.info(f"✅ GitHub Repo geladen: {repo_data['full_name']}")
        logging.info(f"🔗 {repo_data['html_url']}")
    except Exception as e:
        log_error("GitHub", e)


if __name__ == "__main__":
    try:
        atexit.register(cleanup)
        signal.signal(signal.SIGINT, signal_handler)

        # ➕ NEU: GitHub Repo prüfen
        check_github_repo()

        if get_env_bool("ENABLE_DISCORD_BOT", default=True):
            try:
                get_env_str("DISCORD_TOKEN")
                get_env_str("DISCORD_GUILD_ID")
                threading.Thread(target=start_bot, daemon=True).start()
            except RuntimeError as e:
                logging.warning(f"⚠️ Discord-Bot deaktiviert – {e}")

        start_web()

    except KeyboardInterrupt:
        print("🛑 Manuell unterbrochen.")
    except Exception as e:
        log_error("Main", e)
