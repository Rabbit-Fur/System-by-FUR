import os
import sqlite3


def check_file(path, name):
    if os.path.exists(path):
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

    # === Check Dateien ===
    check_file("data/admin_users.db", "Datenbank")
    check_file("static/img/background.jpg", "Hintergrundbild")
    check_file("static/img/fur_logo.gif", "Logo")
    check_file("static/css/style.css", "CSS")

    # === Check Tabellen ===
    if not os.path.exists("data/admin_users.db"):
        print("⛔ DB fehlt – Tabellentest übersprungen.")
        return

    conn = sqlite3.connect("data/admin_users.db")
    for table in [
        "admin_users",
        "events",
        "participants",
        "scores",
        "hall_of_fame",
            "settings"]:
        check_table(conn, table)

    print("\n🏁 Healthcheck abgeschlossen.")


if __name__ == "__main__":
    run_healthcheck()
