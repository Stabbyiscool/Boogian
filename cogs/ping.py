import aiohttp
from discord.ext import commands
from io import BytesIO
import discord
import json
from discord.ext.commands import MissingRequiredArgument

with open('configs.json', 'r') as config_file:
    config = json.load(config_file)

class Ping(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='ping')
    @commands.cooldown(rate=1, per=config['COOLDOWN_TIME'], type=commands.BucketType.user)
    async def ping(self, ctx):
        await ctx.send("Pong!")

    @ping.error
    async def handle_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            pass

async def setup(bot):
    await bot.add_cog(Ping(bot))
