import discord
from discord.ext import commands


class Leaderboard(commands.Cog):
    """Zeigt Ingame-Statistiken / Rankings an (aus DB/API)"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="top")
    async def top_players(self, ctx, category: str = "raids"):
        # Platzhalter – soll später aus DB/API lesen
        fake_data = {
            "raids": ["Alice - 120", "Bob - 110", "Charlie - 100"],
            "donations": ["Dino - 500", "Eva - 450"]
        }
        if category not in fake_data:
            await ctx.send(f"❌ Kategorie '{category}' ist nicht verfügbar.")
            return

        entries = fake_data[category]
        msg = f"🏆 Top {category.capitalize()}:\n" + "\n".join(entries)
        await ctx.send(msg)


async def setup(bot):
    await bot.add_cog(Leaderboard(bot))
