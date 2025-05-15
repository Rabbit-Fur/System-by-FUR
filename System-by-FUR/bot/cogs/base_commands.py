import discord
from discord.ext import commands


class BaseCommands(commands.Cog):
    """Basisbefehle für alle User (z. B. Ping, Hilfe, Status)"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="ping")
    async def ping(self, ctx):
        await ctx.send("🏓 Pong! FUR is online.")

    @commands.command(name="fur")
    async def fur_info(self, ctx):
        await ctx.send("🔥 Welcome to the FUR Alliance – Strength, Unity, Respect.")


async def setup(bot):
    await bot.add_cog(BaseCommands(bot))
