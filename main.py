import threading
import bot
import web
import os
import sys
import signal
import logging
import atexit
from typing import Optional
from datetime import datetime

import locale

# Set the locale to the user's default setting (usually the system's locale)
locale.setlocale(locale.LC_ALL, '')

# If you need a specific locale, you can set it like this:
locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')
# Ensure data directory exists
os.makedirs('data', exist_ok=True)

logging.basicConfig(
    filename='app.log',
    level=logging.ERROR,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)


def log_error(error_type, error):
    """Function log_error."""
    logging.error(f"{error_type}: {str(error)}", exc_info=True)


def start_bot():
    """Function start_bot."""
    try:
        bot.run_bot()
    except Exception as e:
        log_error("Bot", e)


def start_web():
    """Function start_web."""
    try:
        if not all([os.getenv("DISCORD_CLIENT_ID"),
                   os.getenv("DISCORD_CLIENT_SECRET")]):
            raise EnvironmentError("Missing required Discord configuration")
        port = int(os.getenv("PORT", 5000))
        web.app.run(host="0.0.0.0", port=port, debug=False)
    except OSError as e:
        if "Address already in use" in str(e):
            log_error(
    "Web",
     "Port already in use. Try setting a different PORT in environment variables.")
        else:
            log_error("Web", e)
    except Exception as e:
        log_error("Web", e)
        raise


if __name__ == "__main__":
    try:
        # Only check Discord config if bot features are enabled
        if os.getenv("ENABLE_DISCORD_BOT", "false").lower() == "true":
            if not all([os.getenv("DISCORD_TOKEN"),
                       os.getenv("DISCORD_GUILD_ID")]):
                logging.warning(
                    "Discord bot features disabled - missing configuration")

        bot_thread = threading.Thread(target=start_bot)
        bot_thread.daemon = True
        bot_thread.start()

        def cleanup():
    """Function cleanup."""
            logging.info("Cleaning up resources...")
            if 'bot' in globals() and bot.is_ready():
                bot.close()
            web.app.config['SHUTTING_DOWN'] = True

        atexit.register(cleanup)

        def signal_handler(sig, frame):
    """Function signal_handler."""
            print("Shutting down gracefully...")
            if bot.is_ready():
                bot.close()
            sys.exit(0)

        signal.signal(signal.SIGINT, signal_handler)

        # Start web app in main thread
        start_web()
    except KeyboardInterrupt:
        print("Shutting down gracefully...")
    except Exception as e:
        log_error("Main", e)
    