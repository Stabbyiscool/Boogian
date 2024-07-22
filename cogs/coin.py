import aiohttp
from discord.ext import commands
from io import BytesIO
import discord
import json
from discord.ext.commands import MissingRequiredArgument
import random

with open('configs.json', 'r') as config_file:
    config = json.load(config_file)

class coin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='coinflip', aliases=['coin'])
    @commands.cooldown(rate=1, per=config['COOLDOWN_TIME'], type=commands.BucketType.user)
    async def handle_coin(self, ctx):
        coinflip = random.randint(0,1)
        if coinflip == 1:
            await ctx.send("Heads")
        elif coinflip == 0:
            await ctx.send("tails!")


    @handle_coin.error
    async def handle_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            return
        elif isinstance(error, MissingRequiredArgument):
            await ctx.send("A parameter is missing") 
            return
        else:
            await ctx.send("Command no workey ping stabby")


async def setup(bot):
    await bot.add_cog(coin(bot))
