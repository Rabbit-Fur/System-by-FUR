import sqlite3
import asyncio
import discord
import os
from datetime import datetime, timedelta

DATABASE_PATH = os.getenv("DATABASE_PATH", "data/admin_users.db")
DISCORD_TOKEN = "MTM2Mjg4ODY4ODk5MTczMTk2Mw.GwCPnB.3zjO7l4fScMhl__F0OOgzqEfN22PHVC6LdaoxM"  # TESTTOKEN
GUILD_ID = 1344968805151019088
REMINDER_INTERVAL = 60  # Sekunden

EVENT_TIME = (datetime.utcnow() + timedelta(minutes=31)).isoformat()
EVENT_TITLE = "🔔 Reminder-Testevent"

TRANSLATION_PATH = "translations"
DEFAULT_LANG = "de"


def get_translation(lang, key):
    import json
    path = os.path.join(TRANSLATION_PATH, f"{lang}.json")
    try:
        with open(path, "r", encoding="utf-8") as f:
            translations = json.load(f)
        return translations.get(key, key)
    except Exception as e:
        print(f"⚠️ Übersetzung für {key} in {lang} fehlt: {e}")
        return key


def get_db_connection():
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    return conn


async def send_test_reminders(bot, event_id):
    conn = get_db_connection()
    rows = conn.execute("""
        SELECT e.title, p.user_id, p.username
        FROM events e
        JOIN participants p ON e.id = p.event_id
        WHERE e.id = ? AND e.reminded IS NULL
    """, (event_id,)).fetchall()

    for row in rows:
        try:
            user = await bot.fetch_user(int(row["user_id"]))
            lang = DEFAULT_LANG
            msg = f"⏰ {get_translation(lang, 'Reminder')}: **{row['title']}** startet in weniger als 30 Minuten!"
            await user.send(msg)
            print(
                f"📨 Reminder an {row['username']} ({row['user_id']}) gesendet.")
        except Exception as e:
            print(f"❌ Fehler bei {row['username']}: {e}")

    conn.execute("UPDATE events SET reminded = 1 WHERE id = ?", (event_id,))
    conn.commit()
    conn.close()


async def main():
    intents = discord.Intents.default()
    intents.members = True
    bot = discord.Client(intents=intents)

    @bot.event
    async def on_ready():
        print(f"✅ Bot eingeloggt als {bot.user}")
        guild = bot.get_guild(GUILD_ID) or await bot.fetch_guild(GUILD_ID)
        members = await guild.fetch_members(limit=None).flatten()

        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute("""
            INSERT INTO events (title, description, event_time, role, recurrence, reminded)
            VALUES (?, ?, ?, ?, ?, NULL)
        """, (EVENT_TITLE, "Reminder-Test durch alle Mitglieder", EVENT_TIME, "everyone", "once"))
        event_id = cur.lastrowid
        print(f"📆 Test-Event ID {event_id} für {EVENT_TIME} erstellt.")

        for m in members:
            if not m.bot:
                try:
                    cur.execute(
                        "INSERT INTO participants (event_id, user_id, username) VALUES (?, ?, ?)", (event_id, str(
                            m.id), m.name))
                except Exception as e:
                    print(
                        f"⚠️ Teilnehmer {m.name} konnte nicht hinzugefügt werden: {e}")

        conn.commit()
        conn.close()
        print("✅ Teilnehmer gespeichert.")
        await send_test_reminders(bot, event_id)
        await bot.close()

    await bot.start(DISCORD_TOKEN)

if __name__ == "__main__":
    asyncio.run(main())
