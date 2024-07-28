import discord
import json
from discord.ext import commands
with open('configs.json', 'r') as config_file:
    config = json.load(config_file)

class Emojify(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.emoji_dict = {
            'a': '🇦', 'b': '🇧', 'c': '🇨', 'd': '🇩', 'e': '🇪', 'f': '🇫', 'g': '🇬',
            'h': '🇭', 'i': '🇮', 'j': '🇯', 'k': '🇰', 'l': '🇱', 'm': '🇲', 'n': '🇳',
            'o': '🇴', 'p': '🇵', 'q': '🇶', 'r': '🇷', 's': '🇸', 't': '🇹', 'u': '🇺',
            'v': '🇻', 'w': '🇼', 'x': '🇽', 'y': '🇾', 'z': '🇿',
            '0': '0️⃣', '1': '1️⃣', '2': '2️⃣', '3': '3️⃣', '4': '4️⃣', '5': '5️⃣',
            '6': '6️⃣', '7': '7️⃣', '8': '8️⃣', '9': '9️⃣'
        }

    @commands.command(name='emojify')
    @commands.cooldown(rate=1, per=config['COOLDOWN_TIME'], type=commands.BucketType.user)
    async def emojify(self, ctx, *, text: str):
        emojified_text = ''.join([self.emoji_dict.get(char.lower(), char) for char in text])
        await ctx.send(emojified_text)

    @emojify.error
    async def handle_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            return
        elif isinstance(error, MissingRequiredArgument):
            await ctx.send("A parameter is missing", reference=ctx.message) 
            return
        else:
            await ctx.send("Command no workey ping stabby", reference=ctx.message)

async def setup(bot):
    await bot.add_cog(Emojify(bot))
