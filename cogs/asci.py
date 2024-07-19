import discord
from discord.ext import commands
import pyfiglet
import json

with open('configs.json', 'r') as config_file:
    config = json.load(config_file)

class ascii(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='ascii')
    @commands.cooldown(rate=1, per=config['COOLDOWN_TIME'], type=commands.BucketType.user)
    async def textart(self, ctx, *, request: str):
        result = pyfiglet.figlet_format(request)
        await ctx.reply(f"```\n{result}\n```")

async def setup(bot):
    await bot.add_cog(ascii(bot))
