import discord
from discord.ext import commands
import pyfiglet

class Textart(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(description="Get a text art representation of your input")
    @commands.cooldown(1, 1.5, commands.BucketType.user)
    async def textart(self, ctx, *, request: str):
        result = pyfiglet.figlet_format(request)
        await ctx.reply(f"```\n{result}\n```")

async def setup(bot):
    await bot.add_cog(Textart(bot))
