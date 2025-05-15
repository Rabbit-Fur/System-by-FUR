import os
import sqlite3
from datetime import datetime, timedelta

# === Konfiguration ===
DB_PATH = "data/admin_users.db"
REMINDER_WINDOW_MINUTES = 5
DATETIME_FORMAT = "%Y-%m-%d %H:%M"

# === DB vorhanden?
if not os.path.exists(DB_PATH):
    print("❌ Datenbank nicht gefunden:", DB_PATH)
    exit(1)

print("🔔 Reminder-Prüfung gestartet...")

with sqlite3.connect(DB_PATH) as conn:
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    now = datetime.utcnow()
    window = now + timedelta(minutes=REMINDER_WINDOW_MINUTES)

    events = cursor.execute(
        "SELECT id, title, event_time FROM events"
    ).fetchall()

    if not events:
        print("ℹ️ Keine Events vorhanden.")
    else:
        for event in events:
            try:
                event_time = datetime.strptime(event["event_time"], DATETIME_FORMAT)
                if now <= event_time <= window:
                    print(f"⏰ [BALD] {event['title']} – {event['event_time']} UTC")
                else:
                    print(f"🕒 [Später] {event['title']} – {event['event_time']}")
            except ValueError:
                print(f"⚠️ Ungültiges Datum in Event ID {event['id']}: {event['event_time']}")

print("✅ Reminder-Prüfung abgeschlossen.")
