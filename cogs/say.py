import logging
import json
from discord.ext import commands

with open('configs.json', 'r') as config_file:
    config = json.load(config_file)

AUTHORIZED_USERS = {int(user_id) for user_id in config['AUTHORIZED_USERS']}
BANNED_USERS = {int(user_id) for user_id in config['BANNED_USERS']}
CENSOR_WORDS = set(config['CENSOR_WORDS'])

logging.basicConfig(level=logging.INFO)

class Say(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    def contains_censored_words(self, text: str) -> bool:
        lower_text = text.lower()
        return any(word.lower() in lower_text for word in CENSOR_WORDS)

    @commands.command(name='say')
    @commands.cooldown(rate=1, per=config['COOLDOWN_TIME'], type=commands.BucketType.user)
    async def handle_say(self, ctx: commands.Context, *, say_content: str):
        user_id = ctx.message.author.id

        if user_id in AUTHORIZED_USERS:
            if not self.contains_censored_words(say_content):
                await ctx.send(content=say_content, reference=ctx.message)
            else:
                logging.info("Censored words detected")
                await ctx.send(content='No bad words plz :D', reference=ctx.message)
        else:
            logging.info("User is not authorized")
            await ctx.send(content='Go away noob D8<', reference=ctx.message)

    @handle_say.error
    async def handle_error(self, ctx: commands.Context, error: commands.CommandError):
        if isinstance(error, commands.CommandOnCooldown):
            return
        elif isinstance(error, MissingRequiredArgument):
            await ctx.send("A parameter is missing") 
        else:
            await ctx.send("Command no workey ping stabby")


async def setup(bot: commands.Bot):
    await bot.add_cog(Say(bot))
