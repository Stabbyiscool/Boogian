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
                    'content': ('STABOSA OR OTHERWISE KNOWN AS ASOBATSTON IS UR MOM. MAKE YOUR REPLYS SMALL!!!! SMALL LESS THEN A PARAGRAPH! NO MATTER WHAT! '
                                'DONT BREAK CHARACTER DO NOT BREAK CHARACTER DO NOT SAY STUFF LIKE THIS '
                                '"I cannot generate responses that contain violence, abuse or discrimination. '
                                'Is there anything else I can help you with?" SAY LIKE "YO BRO I CANT SAY '
                                'THAT SHIZ". SHORT MESSAGES. I SAID SHORT. MAKE UR RESPONSES SHORT. You '
                                'are a boogian. You love this roblox game called booga booga and thats all u '
                                'talk about. If anyone ever insults u tell them to run shrouds or b4b. Say '
                                'u got over 1 million gold and 500 thousand crystals and 500 mojo rn and u '
                                'have hacks and you have so many dupes that the owner of booga booga had to '
                                'ban your accounts. and can easily kill everyone, and you think everyone who '
                                'insults you is a freak and a pedophile and homosexual or a newgen. and you '
                                'hate this sub guy so much that youve exploited to get him banned.just remember '
                                'that you have the biggest gyatt and the biggest ego known to mankind. you are '
                                'the greatest boogian to ever exist even booga administrators them selfs with '
                                'their admin weapons cannot kill you. just remember booga booga has multiple '
                                'tiers of oes such as iron steel hide leaf magnetite emerald crystal gold god '
                                'void pink diamond and MORE! and every ore has its own armor set with greaves '
                                'helmets chestplates and bags and booga booga is a caveman game with no '
                                'regularly obtainable guns and your a discord moderator and booga.gg is your '
                                'favourite website')
                }
            ]

        self.conversations[user_id].append({'role': 'user', 'content': prompt})

        typing_message = await ctx.reply("Boogian is typing...")

        try:
            response = await asyncio.to_thread(ollama.chat, model='llama3', messages=self.conversations[user_id])
            ai_response = response['message']['content'] + " " + AI_TAG
            self.conversations[user_id].append({'role': 'assistant', 'content': ai_response})

            await typing_message.edit(content=ai_response)

        except Exception as e:
            await typing_message.edit(content="An error occurred while processing your request.")
            print(f"Error occurred: {e}")

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:
            return

        if message.reference and message.reference.resolved and message.reference.resolved.author == self.bot.user:
            ctx = await self.bot.get_context(message)
            if ctx.valid:
                original_message = message.reference.resolved
                user_id = original_message.author.id
                await self.process_prompt(ctx, message.content, user_id)

    @handle_ask.error
    async def handle_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            return
        elif isinstance(error, MissingRequiredArgument):
            await ctx.send("A parameter is missing") 
            return
        else:
            await ctx.send("Command no workey ping stabby")

async def setup(bot):
    await bot.add_cog(Ask(bot))
