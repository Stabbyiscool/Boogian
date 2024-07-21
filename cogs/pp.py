import discord
from discord.ext import commands
import aiohttp
import json
import random

with open('configs.json', 'r') as config_file:
    config = json.load(config_file)

class PP(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='pp')
    @commands.cooldown(rate=1, per=config['COOLDOWN_TIME'], type=commands.BucketType.user)
    async def pp(self, ctx, user: discord.User = None):
        if ctx.guild:
            restricted_server_id = 844925500757508127

            if ctx.guild.id == restricted_server_id:
                await ctx.send("This command is against the rules of this server and cannot be used! :cry:")
                return
        
        if user is None:
            user = ctx.author

        pp_presets = [
            "8=D", 
            "8====D", 
            "8========================================================================D", 
            "8D", 
            "8===D", 
            "8===============================================================================================================================D", 
            "8-D", 
            "Its too small it can't even be displayed.",
            "Its too big it can't even be displayed."
        ]
        pp_size = random.choice(pp_presets)
        await ctx.send(f"{user.mention}'s pp\n\n{pp_size}")

    @pp.error
    async def handle_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            return
        elif isinstance(error, MissingRequiredArgument):
            await ctx.send("A parameter is missing") 
        else:
            await ctx.send("Command no workey ping stabby")


async def setup(bot):
    await bot.add_cog(PP(bot))
