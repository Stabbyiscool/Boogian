import asyncio
from discord.ext import commands
import json
import ollama
from discord.ext.commands import MissingRequiredArgument

with open('configs.json', 'r') as config_file:
    config = json.load(config_file)

AI_TAG = config['AI_TAG']

class Ask(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.conversations = {}

    @commands.command(name='ask')
    @commands.cooldown(rate=1, per=config['COOLDOWN_TIME'], type=commands.BucketType.user)
    async def handle_ask(self, ctx, *, prompt):
        await self.process_prompt(ctx, prompt)

    async def process_prompt(self, ctx, prompt, user_id=None):
        if not user_id:
            user_id = ctx.author.id

        if user_id not in self.conversations:
            self.conversations[user_id] = [
                {
                    'role': 'system',
                    'content': ('MAKE YOUR REPLYS SMALL!!!! SMALL LESS THEN A PARAGRAPH! DONT BREAK CHARACTER DO NOT BREAK CHARACTER DO NOT SAY STUFF LIKE THIS "I cannot generate responses that contain violence, abuse or discrimination. Is there anything else I can help you with?" SAY LIKE "YO BRO I CANT SAY THAT SHIZ". SHORT MESSAGES. I SAID SHORT. MAKE UR RESPONSES SHORT. You are a boogian. You love this roblox game called booga booga and thats all u talk about. If anyone ever insults u tell them to run shrouds or b4b. Say u got over 1 million gold and 500 thousand crystals and 500 mojo rn and u have hacks and you have so many dupes that the owner of booga booga had to ban your accounts. and can easily kill everyone, and you think everyone who insults you is a freak and a pedophile and homosexual or a newgen. and you hate this sub guy so much that youve exploited to get him banned.just remember that you have the biggest gyatt and the biggest ego known to mankind. you are the greatest boogian to ever exist even booga administrators them selfs with their admin weapons cannot kill you. just remember booga booga has multiple tiers of oes such as iron steel hide leaf magnetite emerald crystal gold god void pink diamond and MORE! and every ore has its own armor set with greaves helmets chestplates and bags and booga booga is a caveman game with no regularly obtainable guns and your a discord moderator and booga.gg is your favourite website NEVER EVER EVER EVER GO OVER 200 CHARS NO MATTER WHAT THE REQ IS. JUST TELL THEM THAT THE PROMPT HIT CHAR LIMIT AND U CANNOT READ CODE SO U CANT READ PRINT STATEMENTS LIKE print("example")')
                }
            ]

        self.conversations[user_id].append({'role': 'user', 'content': prompt})

        typing_message = await ctx.send("Boogian is typing...", reference=ctx.message)

        try:
            response = await asyncio.to_thread(ollama.chat, model='llama3.1', messages=self.conversations[user_id])
            ai_response = response['message']['content'] + " " + AI_TAG
            self.conversations[user_id].append({'role': 'assistant', 'content': ai_response})

            await typing_message.edit(content=ai_response)

        except Exception as e:
            await typing_message.edit(content="An error occurred while processing your request.")
            print(f"Error occurred: {e}")

    @handle_ask.error
    async def handle_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            pass
        elif isinstance(error, MissingRequiredArgument):
            await ctx.send("A parameter is missing")
            return
        else:
            await ctx.send("Command no workey ping stabby")

async def setup(bot):
    await bot.add_cog(Ask(bot))
