import discord
from discord.ext import commands


class Newsletter(commands.Cog):
    """Verwaltet Clan-Mitteilungen oder Infos"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="announce")
    @commands.has_permissions(administrator=True)
    async def announce(self, ctx, *, message: str):
        await ctx.send(f"📢 Clan-Ankündigung:\n{message}")


async def setup(bot):
    await bot.add_cog(Newsletter(bot))
