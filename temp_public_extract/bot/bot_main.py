import os
import sys
import logging
import asyncio
import sqlite3
import discord
from discord.ext import commands
from config import Config

# === Logging Setup ===
log = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

# === Intents ===
intents = discord.Intents.default()
intents.members = True
intents.message_content = True
intents.guilds = True

# === Bot Instanz ===
bot = commands.Bot(
    command_prefix=Config.BOT_PREFIX if hasattr(Config, 'BOT_PREFIX') else '!',
    intents=intents
)

# === DB-Verbindung für Reminder-Cog (optional) ===


def get_bot_db_connection():
    try:
        conn = sqlite3.connect(Config.DATABASE_PATH, timeout=10)
        conn.row_factory = sqlite3.Row
        conn.execute('PRAGMA journal_mode=WAL')
        conn.execute('PRAGMA busy_timeout = 5000')
        return conn
    except sqlite3.Error as e:
        log.error(f"Bot DB connection error: {e}", exc_info=True)
        return None

# === Cog-Auto-Loader ===


async def load_cogs():
    cog_dir = os.path.join(os.path.dirname(__file__), 'cogs')
    if not os.path.isdir(cog_dir):
        log.warning(f"Cog directory not found: {cog_dir}")
        return

    for filename in os.listdir(cog_dir):
        if filename.endswith('.py') and not filename.startswith('__'):
            extension = f'bot.cogs.{filename[:-3]}'
            try:
                log.debug(f"Attempting to load extension: {extension}")
                await bot.load_extension(extension)
                log.info(f'✅ Successfully loaded Cog: {extension}')
            except commands.ExtensionAlreadyLoaded:
                log.warning(f"⚠️ Cog already loaded: {extension}")
            except commands.ExtensionNotFound:
                log.error(f"❌ Cog not found: {extension}")
            except commands.NoEntryPointError:
                log.error(f"❌ Cog {extension} has no setup function.")
            except Exception as e:
                log.error(f'❌ Failed to load Cog {extension}.', exc_info=e)

# === on_ready ===


@bot.event
async def on_ready():
    log.info(f'🔥 Bot logged in as {bot.user.name} (ID: {bot.user.id})')
    log.info(f"discord.py Version: {discord.__version__}")
    log.info('------ Bot Ready ------')

    await load_cogs()

    if Config.DISCORD_GUILD_ID:
        guild_obj = discord.Object(id=Config.DISCORD_GUILD_ID)
        try:
            bot.tree.copy_global_to(guild=guild_obj)
            synced = await bot.tree.sync(guild=guild_obj)
            log.info(
                f"✅ Synced {len(synced)} commands to guild {Config.DISCORD_GUILD_ID}")
        except discord.errors.Forbidden:
            log.error("❌ Missing permission to sync commands.")
        except Exception as e:
            log.error(f"❌ Failed to sync commands.", exc_info=e)
    else:
        log.warning(
            "⚠️ DISCORD_GUILD_ID not set. Slash commands may sync slowly.")

    activity = discord.Game(name="Forging Legends | FUR Alliance")
    await bot.change_presence(status=discord.Status.online, activity=activity)
    log.info(f"Bot presence set to: {activity.name}")

# === Prefix Command Error Handler ===


@bot.event
async def on_command_error(
        ctx: commands.Context,
        error: commands.CommandError):
    if isinstance(error, commands.CommandNotFound):
        return
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(f"⚠️ Missing argument: `{error.param.name}`.")
    elif isinstance(error, commands.CommandOnCooldown):
        await ctx.send(f"⏳ Cooldown. Retry in {error.retry_after:.2f}s.")
    elif isinstance(error, commands.CheckFailure):
        await ctx.send("🚫 You lack permission.")
    else:
        log.error(f"Error in command {ctx.command}:", exc_info=error)
        try:
            await ctx.send("❌ Unexpected error.")
        except discord.HTTPException:
            pass

# === Slash Command Error Handler ===


@bot.tree.error
async def on_app_command_error(
        interaction: discord.Interaction,
        error: discord.app_commands.AppCommandError):
    try:
        if isinstance(error, discord.app_commands.CommandOnCooldown):
            await interaction.response.send_message(
                f"⏳ Cooldown. Retry in {error.retry_after:.2f}s.", ephemeral=True)
        elif isinstance(error, discord.app_commands.CheckFailure):
            await interaction.response.send_message(
                "🚫 No permission.", ephemeral=True)
        else:
            log.error(
                f"Slash command error: {interaction.command}",
                exc_info=error)
            if not interaction.response.is_done():
                await interaction.response.send_message("❌ Unexpected error.", ephemeral=True)
            else:
                await interaction.followup.send("❌ Unexpected error.", ephemeral=True)
    except discord.HTTPException:
        log.warning("❗ Unable to send error response.")

# === Hauptstartfunktion (async) ===


async def start_discord_bot_async():
    if not Config.DISCORD_TOKEN:
        log.critical("DISCORD_TOKEN fehlt!")
        raise ValueError("Discord token fehlt")
    try:
        log.info("🚀 Bot wird gestartet...")
        await bot.start(Config.DISCORD_TOKEN)
    except discord.LoginFailure:
        log.critical("❌ Login fehlgeschlagen. Prüfe Token.")
        sys.exit("Ungültiger Token")
    except Exception as e:
        log.critical(f"❌ Startfehler: {e}", exc_info=True)
        raise

# === Wrapper für run.py (thread-kompatibel) ===


def run_bot_sync():
    try:
        asyncio.run(start_discord_bot_async())
    except KeyboardInterrupt:
        log.info("🛑 Bot-Stop durch KeyboardInterrupt")
    except Exception as e:
        log.critical(f"💥 Laufzeitfehler: {e}", exc_info=True)


main = run_bot_sync

# Optional: direkt startbar (für Testzwecke)
# if __name__ == "__main__":
#     run_bot_sync()
