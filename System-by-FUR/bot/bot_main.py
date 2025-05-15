import logging

try:
    import discord
    from discord.ext import commands
    IS_STUB = False
except ImportError:
    import discord_util as discord
    IS_STUB = True

    class commands:
        class Bot(discord.Client):
            def command(self, *args, **kwargs):
                def wrapper(func): return func
                return wrapper


log = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

# Intents konfigurieren
intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.members = True

# Bot-Instanz erstellen
bot = commands.Bot(command_prefix="!", intents=intents)


@bot.event
async def on_ready():
    log.info(f"✅ Eingeloggt als {bot.user} (ID: {getattr(bot.user, 'id', 'n/a')})")


def is_ready():
    return hasattr(bot, "is_ready") and bot.is_ready()


def main():
    try:
        from config import Config
        log.info("🚀 Discord-Bot wird gestartet...")
        bot.run(Config.DISCORD_TOKEN)
    except Exception as e:
        log.critical(f"❌ Login fehlgeschlagen. Prüfe Token und Intents: {e}", exc_info=True)
