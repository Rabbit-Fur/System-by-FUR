import os
import sqlite3
from datetime import datetime

# === Konfiguration ===
DB_PATH = "data/admin_users.db"

# Eingabedaten (statisch oder aus argparse)
username = "TestChampion"
title = "🔥 Champion of Unity 🔥"
month = "Mai 2025"  # Oder dynamisch: datetime.now().strftime("%B %Y")
poster_url = "/static/champions/champion_testchampion_mai2025.png"


def insert_champion(db_path, username, title, month, poster_url):
    if not os.path.exists(db_path):
        print(f"❌ Datenbank nicht gefunden: {db_path}")
        return

    try:
        with sqlite3.connect(db_path) as conn:
            conn.execute("PRAGMA foreign_keys = ON")
            cursor = conn.cursor()

            # Optional: Doppelte Champions für den Monat verhindern
            cursor.execute("""
                SELECT 1 FROM hall_of_fame
                WHERE username = ? AND month = ?
            """, (username, month))
            if cursor.fetchone():
                print(f"⚠️ Champion '{username}' für {month} existiert bereits.")
                return

            cursor.execute(
                """
                INSERT INTO hall_of_fame (username, honor_title, month, poster_url)
                VALUES (?, ?, ?, ?)
                """,
                (username, title, month, poster_url),
            )
            conn.commit()
            print(f"✅ Champion '{username}' wurde für {month} erfolgreich eingetragen.")

    except sqlite3.Error as e:
        print(f"❌ Fehler beim Eintrag in die Datenbank: {e}")


if __name__ == "__main__":
    insert_champion(DB_PATH, username, title, month, poster_url)
