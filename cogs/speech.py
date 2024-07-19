import discord
from discord.ext import commands
import requests
import json
from io import BytesIO

with open('configs.json', 'r') as config_file:
    config = json.load(config_file)

class Speech(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='speech')
    @commands.cooldown(rate=1, per=config['COOLDOWN_TIME'], type=commands.BucketType.user)
    async def speech(self, ctx, image_url: str = None, type: str = "full"):
        if type not in ["full", "cutout"]:
            await ctx.send("Invalid type specified. Please choose 'full' or 'cutout'.")
            return

        if not image_url and not ctx.message.attachments:
            await ctx.send("Please provide an image URL or attach an image.")
            return

        try:
            if image_url:
                encoded_url = requests.utils.quote(image_url, safe='')
                api_url = f"https://api.stabosa.fun/speech/?image_url={encoded_url}&type={type}"
                response = requests.get(api_url)
            else:
                attachment = ctx.message.attachments[0]
                image_data = await attachment.read()
                api_url = f"https://api.stabosa.fun/speech/?type={type}"
                response = requests.post(api_url, files={"file": ('image.png', image_data, 'image/png')})

            response.raise_for_status()

            if response.headers.get('Content-Type') == 'image/png':
                image_data = BytesIO(response.content)
                file = discord.File(fp=image_data, filename="speech_image.png")
                await ctx.send(file=file)
            else:
                await ctx.send("The API did not return an image.")

        except requests.RequestException as e:
            await ctx.send(f"File cannot be above 5MB")

async def setup(bot):
    await bot.add_cog(Speech(bot))
