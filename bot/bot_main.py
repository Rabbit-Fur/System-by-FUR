import logging

import discord
from discord.ext import commands

log = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)


@bot.event
async def on_ready():
    log.info(f"✅ Eingeloggt als {bot.user} (ID: {bot.user.id})")


def main():
    try:
        from config import Config

        log.info("🚀 Bot wird gestartet...")
        bot.run(Config.DISCORD_TOKEN)
    except Exception as e:
        log.critical(f"❌ Login fehlgeschlagen. Prüfe Token und Intents: {e}", exc_info=True)
