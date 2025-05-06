import os
import sqlite3
from datetime import datetime

db_path = 'data/admin_users.db'
if not os.path.exists(db_path):
    print("❌ Datenbank nicht gefunden.")
    exit(1)

print("🏆 Champion-Test wird eingetragen...")

username = "TestChampion"
month = datetime.utcnow().strftime("%Y-%m")
poster_url = "/static/champions/test_champion.png"
honor_title = "🔥 Champion of Unity 🔥"

with sqlite3.connect(db_path) as conn:
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO hall_of_fame (username, honor_title, month, poster_url)
        VALUES (?, ?, ?, ?)
    """, (username, honor_title, month, poster_url))
    conn.commit()

print(f"✅ Champion '{username}' für {month} erfolgreich eingetragen.")
