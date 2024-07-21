import discord
from discord.ext import commands
import aiohttp
import json
import tempfile
import os
with open('configs.json', 'r') as config_file:
    config = json.load(config_file)

class buildaboogian(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='buildaboogian')
    @commands.cooldown(rate=1, per=config['COOLDOWN_TIME'], type=commands.BucketType.user)
    async def eight_ball(self, ctx):
        await ctx.reply('[Boogian offical repo](https://github.com/Stabbyiscool/Boogian) give it a star and ill kiss u.')

    @eight_ball.error
    async def handle_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            return
        elif isinstance(error, MissingRequiredArgument):
            await ctx.send("A parameter is missing") 
        else:
            await ctx.send("Command no workey ping stabby")

async def setup(bot):
    await bot.add_cog(buildaboogian(bot))