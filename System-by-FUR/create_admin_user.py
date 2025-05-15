import os
import sqlite3

from werkzeug.security import generate_password_hash

from config import Config


def create_reminders_table():
    conn = sqlite3.connect(Config.DATABASE_PATH)
    c = conn.cursor()

    c.execute(
        """
        CREATE TABLE IF NOT EXISTS reminders_sent (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            event_id INTEGER NOT NULL,
            user_id TEXT NOT NULL,
            sent_at TEXT NOT NULL
        );
    """
    )

    conn.commit()
    conn.close()
    print("✅ Tabelle 'reminders_sent' wurde erstellt.")


if __name__ == "__main__":
    create_reminders_table()

db_path = "data/admin_users.db"
os.makedirs(os.path.dirname(db_path), exist_ok=True)

username = "Rabbit"
password = "Marcel"
hashed_password = generate_password_hash(password)

with sqlite3.connect(db_path) as conn:
    conn.execute(
        """
    CREATE TABLE IF NOT EXISTS admin_users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL
    );
    """
    )
    conn.execute("INSERT OR IGNORE INTO admin_users (username, password) VALUES (?, ?)", (username, hashed_password))
    conn.commit()

print(f"✅ Admin-User '{username}' wurde erstellt oder existiert bereits.")
