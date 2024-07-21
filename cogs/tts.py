import aiohttp
from discord.ext import commands
from io import BytesIO
import discord
import json
from gtts import gTTS

with open('configs.json', 'r') as config_file:
    config = json.load(config_file)

class TTS(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='tts')
    @commands.cooldown(rate=1, per=config['COOLDOWN_TIME'], type=commands.BucketType.user)
    async def handle_tts(self, ctx, *, text: str):
        if len(text) > 250:
            await ctx.send("Too long noob. Make it shorter", reference=ctx.message)
            return

        try:
            tts = gTTS(text)
            audio_file = BytesIO()
            tts.write_to_fp(audio_file)
            audio_file.seek(0)
            await ctx.send(file=discord.File(audio_file, 'tts.mp3'))
        except Exception as e:
            await ctx.send(f"An error occurred while processing the command: {e}", reference=ctx.message)

    @handle_tts.error
    async def handle_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            return
        elif isinstance(error, MissingRequiredArgument):
            await ctx.send("A parameter is missing") 
            return
        else:
            await ctx.send("Command no workey ping stabby")


async def setup(bot):
    await bot.add_cog(TTS(bot))
