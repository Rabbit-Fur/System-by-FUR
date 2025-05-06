import os
import sqlite3
from datetime import datetime

# Konfiguration
db_path = "data/admin_users.db"
username = "TestChampion"
title = "🔥 Champion of Unity 🔥"
month = "Mai 2025"
poster_url = "/static/champions/champion_testchampion_mai2025.png"

# Prüfe ob DB existiert
if not os.path.exists(db_path):
    print("❌ Datenbank nicht gefunden:", db_path)
    exit(1)

# Eintrag durchführen
with sqlite3.connect(db_path) as conn:
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO hall_of_fame (username, honor_title, month, poster_url)
        VALUES (?, ?, ?, ?)
    """,
        (username, title, month, poster_url),
    )
    conn.commit()

print(f"✅ Champion '{username}' wurde für {month} erfolgreich eingetragen.")
