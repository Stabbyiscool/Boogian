import logging
import json
import concurrent.futures
from discord.ext import commands
from discord.ext.commands import MissingRequiredArgument
import ollama

with open('configs.json', 'r') as config_file:
    config = json.load(config_file)

AUTHORIZED_USERS = {int(user_id) for user_id in config['AUTHORIZED_USERS']}
BANNED_USERS = {int(user_id) for user_id in config['BANNED_USERS']}
CENSOR_WORDS = set(config['CENSOR_WORDS'])

logging.basicConfig(level=logging.INFO)

class Say(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.executor = concurrent.futures.ThreadPoolExecutor(max_workers=3)

    def contains_censored_words(self, text: str) -> bool:
        lower_text = text.lower()
        return any(word.lower() in lower_text for word in CENSOR_WORDS)

    def ai_censor(self, text: str) -> bool:
        prompt = (
            "You are a censor bot now. I'm going to give you a sentence to censor. "
            "It can't have any slurs, anything that says 'under tos' or any number under 13 so we don't get banned. "
            "Curse words are allowed. Only respond with a Y or an N. "
            "Now here is your prompt: " + text
        )
        try:
            response = ollama.generate(
                model="llama3",
                prompt=prompt
            )
            return response.strip().upper() == "Y"
        except Exception as e:
            logging.error(f"Error with AI censor: {e}")
            return False

    @commands.command(name='say')
    @commands.cooldown(rate=1, per=config['COOLDOWN_TIME'], type=commands.BucketType.user)
    async def handle_say(self, ctx: commands.Context, *, say_content: str):
        user_id = ctx.message.author.id

        if user_id in AUTHORIZED_USERS:
            if not self.contains_censored_words(say_content):
                loop = ctx.bot.loop
                result = await loop.run_in_executor(self.executor, self.ai_censor, say_content)
                if result:
                    await ctx.send(content=say_content, reference=ctx.message)
                else:
                    logging.info("AI censored the message")
                    await ctx.send(content='No bad words plz :D', reference=ctx.message)
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
            return
        else:
            await ctx.send("Command no workey ping stabby")

async def setup(bot: commands.Bot):
    await bot.add_cog(Say(bot))
