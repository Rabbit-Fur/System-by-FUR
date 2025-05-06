import os
import sqlite3
from datetime import datetime, timedelta

db_path = "data/admin_users.db"
if not os.path.exists(db_path):
    print("❌ Datenbank nicht gefunden.")
    exit(1)

print("🔔 Reminder-Prüfung gestartet...")

with sqlite3.connect(db_path) as conn:
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    now = datetime.utcnow()
    window = now + timedelta(minutes=5)

    upcoming = cursor.execute(
        """
        SELECT id, title, event_time FROM events
    """
    ).fetchall()

    for event in upcoming:
        event_time = datetime.strptime(event["event_time"], "%Y-%m-%d %H:%M")
        if now <= event_time <= window:
            print(f"⏰ EVENT BALD: {event['title']} um {event['event_time']} UTC")
        else:
            print(f"🕒 {event['title']} liegt außerhalb des Reminder-Zeitfensters.")

print("✅ Reminder-Prüfung abgeschlossen.")
