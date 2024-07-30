import discord
from discord.ext import commands
from discord.ext.commands import MissingRequiredArgument
import random
import json
with open('configs.json', 'r') as config_file:
    config = json.load(config_file)

class EightBall(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.responses = [
            "Yes.",
            "No.",
            "Maybe.",
            "I don't know.",
            "Definitely.",
            "Absolutely not.",
            "Ask again later.",
            "I'm not sure.",
            "Try again."
        ]

    @commands.command(name='8ball')
    @commands.cooldown(rate=1, per=config['COOLDOWN_TIME'], type=commands.BucketType.user)
    async def eight_ball(self, ctx, *, question: str):
        response = random.choice(self.responses)
        formatted_response = (
            f"**Your question:** {question}\n"
            f"**8ball says:** {response}"
        )
        await ctx.send(formatted_response)

    @eight_ball.error
    async def handle_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            pass
        elif isinstance(error, MissingRequiredArgument):
            await ctx.send("A parameter is missing.")
            return
        else:
            await ctx.send("Command no workey ping stabby")

async def setup(bot):
    await bot.add_cog(EightBall(bot))
