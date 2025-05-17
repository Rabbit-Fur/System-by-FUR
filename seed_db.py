import os
import sqlite3

DB_PATH = "data/admin_users.db"

if not os.path.exists(DB_PATH):
    print("❌ Datenbank nicht gefunden. Bitte zuerst init_db.py ausführen.")
    exit(1)

with sqlite3.connect(DB_PATH) as conn:
    conn.execute("PRAGMA foreign_keys = ON")
    cursor = conn.cursor()

    # === Events ===
    cursor.execute("""
        INSERT INTO events (title, description, event_time, role, recurrence)
        VALUES (?, ?, ?, ?, ?)
    """, ("🔥 Flame Raid", "Elite war against Clan Shadow", "2025-05-10 18:00", "@RaidTeam", "weekly"))

    cursor.execute("""
        INSERT INTO events (title, description, event_time, role, recurrence)
        VALUES (?, ?, ?, ?, ?)
    """, ("📜 Council Meeting", "Monthly planning & lore updates", "2025-05-12 20:30", "@Leaders", "monthly"))

    # === Teilnehmer ===
    cursor.execute("INSERT INTO participants (event_id, user_id, username, checked_in) VALUES (?, ?, ?, ?)",
                   (1, "user123", "Alice", 1))
    cursor.execute("INSERT INTO participants (event_id, user_id, username, checked_in) VALUES (?, ?, ?, ?)",
                   (1, "user456", "Bob", 0))
    cursor.execute("INSERT INTO participants (event_id, user_id, username, checked_in) VALUES (?, ?, ?, ?)",
                   (2, "user789", "Xevi", 1))

    # === Scores ===
    cursor.execute("INSERT INTO scores (user_id, username, category, period, score) VALUES (?, ?, ?, ?, ?)",
                   ("user123", "Alice", "raids", "alltime", 120))
    cursor.execute("INSERT INTO scores (user_id, username, category, period, score) VALUES (?, ?, ?, ?, ?)",
                   ("user456", "Bob", "donations", "alltime", 300))

    # === Hall of Fame ===
    cursor.execute("INSERT INTO hall_of_fame (username, honor_title, month, poster_url) VALUES (?, ?, ?, ?)",
                   ("Xevi", "🔥 Champion of the Month 🔥", "2025-04", "/static/champions/xevi_april.png"))

    # === Settings ===
    cursor.execute("INSERT INTO settings (user_id, allow_dm) VALUES (?, ?)", ("user123", 1))

    conn.commit()

print("✅ Seed-Daten erfolgreich eingefügt.")
