import atexit
import locale
import logging
import os
import signal
import sys
import threading
import os
from flask import Flask, request, jsonify
import web

import bot

import locale

try:
    locale.setlocale(locale.LC_ALL, "")
    locale.setlocale(locale.LC_ALL, "en_US.UTF-8")
except locale.Error:
    # Locale nicht verfügbar im Container – ignorieren oder auf fallback setzen
    pass

os.makedirs("data", exist_ok=True)

logging.basicConfig(
    filename="app.log", level=logging.ERROR, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)


def log_error(error_type, error):
    logging.error(f"{error_type}: {str(error)}", exc_info=True)


def start_bot():
    try:
        bot.run_bot()
    except Exception as e:
        log_error("Bot", e)


def start_web():
    try:
        if not all([os.getenv("DISCORD_CLIENT_ID"), os.getenv("DISCORD_CLIENT_SECRET")]):
            raise EnvironmentError("Missing required Discord configuration")
        port = int(os.getenv("PORT", 5000))
        web.app.run(host="0.0.0.0", port=port, debug=False)
    except OSError as e:
        if "Address already in use" in str(e):
            log_error("Web", "Port already in use. Try setting a different PORT in environment variables.")
        else:
            log_error("Web", e)
    except Exception as e:
        log_error("Web", e)
        raise


def cleanup():
    logging.info("Cleaning up resources...")
    if "bot" in globals() and bot.is_ready():
        bot.close()
    web.app.config["SHUTTING_DOWN"] = True


def signal_handler(sig, frame):
    print("Shutting down gracefully...")
    if bot.is_ready():
        bot.close()
    sys.exit(0)


if __name__ == "__main__":
    try:
        if os.getenv("ENABLE_DISCORD_BOT", "false").lower() == "true":
            if not all([os.getenv("DISCORD_TOKEN"), os.getenv("DISCORD_GUILD_ID")]):
                logging.warning("Discord bot features disabled - missing configuration")

        bot_thread = threading.Thread(target=start_bot)
        bot_thread.daemon = True
        bot_thread.start()

        atexit.register(cleanup)
        signal.signal(signal.SIGINT, signal_handler)

        start_web()
    except KeyboardInterrupt:
        print("Shutting down gracefully...")
    except Exception as e:
        log_error("Main", e)
