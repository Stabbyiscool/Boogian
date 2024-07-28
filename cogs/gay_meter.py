import random
from discord.ext import commands
import json
from discord.ext.commands import MissingRequiredArgument

with open('configs.json', 'r') as config_file:
    config = json.load(config_file)

class GayMeter(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='gay')
    @commands.cooldown(rate=1, per=config['COOLDOWN_TIME'], type=commands.BucketType.user)
    async def gaymeter(self, ctx):
        if ctx.message.mentions:
            target_user = ctx.message.mentions[0]
            special_users = [627905328075505683, 1085537701035524187, 1028248062130409572]

            if target_user.id in special_users:
                gayness = random.randint(1, 10)
            elif target_user.id == 989303284072325121:
              	gayness = 10000000000000000
            else:
                gayness = random.randint(1, 100)

            response_message = f"{target_user.mention} is {gayness}% gay! 🌈"
            await ctx.send(content=response_message, reference=ctx.message)

    @gaymeter.error
    async def handle_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            return
        elif isinstance(error, MissingRequiredArgument):
            await ctx.send("A parameter is missing", reference=ctx.message) 
            return
        else:
            await ctx.send("Command no workey ping stabby", reference=ctx.message)

async def setup(bot):
    await bot.add_cog(GayMeter(bot))
