from datetime import datetime

import discord
from discord.ext import commands, tasks


class Reminders(commands.Cog):
    """Regelmäßige Erinnerungen, z. B. Events, Quests"""

    def __init__(self, bot):
        self.bot = bot
        self.reminder_loop.start()

    def cog_unload(self):
        self.reminder_loop.cancel()

    @tasks.loop(minutes=60)
    async def reminder_loop(self):
        now = datetime.utcnow().strftime("%H:%M")
        channel = self.bot.get_channel(1365580225945014385)  # aus .env / config laden!
        if channel:
            await channel.send(f"⏰ Reminder Loop: UTC {now} – check your quests!")


async def setup(bot):
    await bot.add_cog(Reminders(bot))
