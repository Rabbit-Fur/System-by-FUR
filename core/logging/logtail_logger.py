# System-by-FUR: Logtail Integration (Better Stack)

import os
import logging
import requests
from datetime import datetime

# Setup Logger
logger = logging.getLogger("fur-system")
logger.setLevel(logging.INFO)

# Webhook Settings
LOGTAIL_ENDPOINT = "https://s1308699.eu-nbg-2.betterstackdata.com"
LOGTAIL_TOKEN = os.getenv("LOGTAIL_TOKEN")

def log_event(message: str, level="info"):
    log_entry = {
        "dt": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC"),
        "message": message
    }

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {LOGTAIL_TOKEN}"
    }

    try:
        response = requests.post(
            LOGTAIL_ENDPOINT,
            json=log_entry,
            headers=headers,
            verify=False  # Optional: wegen `-k` im curl, bei SSL-Problemen
        )
        logger.info(f"Logtail status: {response.status_code}")
    except Exception as e:
        logger.error(f"Logtail Error: {e}")
