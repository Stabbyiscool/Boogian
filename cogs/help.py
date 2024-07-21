from discord.ext import commands
import json
from discord.ext.commands import MissingRequiredArgument

with open('configs.json', 'r') as config_file:
    config = json.load(config_file)

command_descriptions = config['COMMAND_DESCRIPTIONS']

class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='help')
    @commands.cooldown(rate=1, per=config['COOLDOWN_TIME'], type=commands.BucketType.user)
    async def send_help_message(self, ctx):
        help_message = "Here are the available commands:\n ```markdown\n"
        for command, description in command_descriptions.items():
            help_message += f"{command}: {description}\n"
        await ctx.send(help_message + "```\n```markdown\nContributors : Stabosa <creator> Mrbanto <brain-creator>```", reference=ctx.message)

    @send_help_message.error
    async def handle_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            return
        elif isinstance(error, MissingRequiredArgument):
            await ctx.send("A parameter is missing") 
            return
        else:
            await ctx.send("Command no workey ping stabby")


async def setup(bot):
    await bot.add_cog(Help(bot))
