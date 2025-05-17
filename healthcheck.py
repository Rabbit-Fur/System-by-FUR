import os
import sqlite3
from pathlib import Path


def check_file(path, name):
    if Path(path).is_file():
        print(f"✅ {name}: OK")
    else:
        print(f"❌ {name}: FEHLT")


def check_table(conn, table):
    try:
        conn.execute(f"SELECT 1 FROM {table} LIMIT 1")
        print(f"✅ Tabelle '{table}': OK")
    except sqlite3.OperationalError:
        print(f"❌ Tabelle '{table}' fehlt!")


def run_healthcheck():
    print("🔍 Starte Healthcheck...\n")

    # === Dateien prüfen ===
    files = {
        "data/admin_users.db": "Datenbank",
        "static/img/background.jpg": "Hintergrundbild",
        "static/img/fur_logo.gif": "Logo",
        "static/css/style.css": "CSS"
    }

    for path, name in files.items():
        check_file(path, name)

    # === Tabellen prüfen ===
    db_path = "data/admin_users.db"
    if not os.path.exists(db_path):
        print("⛔ Datenbank fehlt – Tabellentests übersprungen.")
        return

    conn = sqlite3.connect(db_path)
    tables = [
        "admin_users",
        "events",
        "participants",
        "scores",
        "hall_of_fame",
        "settings"
    ]
    for table in tables:
        check_table(conn, table)

    conn.close()
    print("\n🏁 Healthcheck abgeschlossen.")


if __name__ == "__main__":
    run_healthcheck()
