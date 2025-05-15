import os
import sqlite3
from datetime import datetime, timedelta

db_path = "data/admin_users.db"
if not os.path.exists(db_path):
    print("❌ Datenbank fehlt. Bitte erst init_db.py ausführen.")
    exit(1)

with sqlite3.connect(db_path) as conn:
    cursor = conn.cursor()

    # 1. Event erstellen
    event_time = (datetime.utcnow() + timedelta(minutes=10)).strftime("%Y-%m-%d %H:%M")
    cursor.execute(
        """
        INSERT INTO events (title, description, event_time, role, recurrence)
        VALUES (?, ?, ?, ?, ?)
    """,
        ("🔥 Test Raid", "UQM Testlauf gegen Testgegner", event_time, "@Tester", "none"),
    )
    event_id = cursor.lastrowid

    # 2. Teilnehmer eintragen
    cursor.execute(
        """
        INSERT INTO participants (event_id, user_id, username, checked_in)
        VALUES (?, ?, ?, ?)
    """,
        (event_id, "testuser1", "AlphaWolf", 1),
    )
    cursor.execute(
        """
        INSERT INTO participants (event_id, user_id, username, checked_in)
        VALUES (?, ?, ?, ?)
    """,
        (event_id, "testuser2", "BetaWolf", 0),
    )

    # 3. Score für Leaderboard
    cursor.execute(
        """
        INSERT INTO scores (user_id, username, category, period, score)
        VALUES (?, ?, ?, ?, ?)
    """,
        ("testuser1", "AlphaWolf", "raids", "alltime", 99),
    )

    conn.commit()

print("✅ Testevent + Teilnehmer + Score erfolgreich eingetragen.")
