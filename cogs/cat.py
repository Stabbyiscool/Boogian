import aiohttp
from discord.ext import commands
from io import BytesIO
import discord
import json
from discord.ext.commands import MissingRequiredArgument
from PIL import Image

with open('configs.json', 'r') as config_file:
    config = json.load(config_file)

class Cat(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='cat')
    @commands.cooldown(rate=1, per=config['COOLDOWN_TIME'], type=commands.BucketType.user)
    async def handle_cat_picture(self, ctx):
        async with aiohttp.ClientSession() as session:
            async with session.get('https://api.stabosa.fun/maka') as resp:
                if resp.status == 200:
                    data = await resp.json()
                    image_url = data.get('url')
                    async with session.get(image_url) as image_resp:
                        if image_resp.status == 200:
                            image_data = await image_resp.read()
                            image = Image.open(BytesIO(image_data))

                            new_size = (int(image.width * 0.25), int(image.height * 0.25))
                            resized_image = image.resize(new_size, Image.LANCZOS)

                            image_buffer = BytesIO()
                            file_extension = image_url.split('.')[-1]
                            resized_image.save(image_buffer, format=image.format)
                            image_buffer.seek(0)

                            image_file = discord.File(image_buffer, f'cat_picture.{file_extension}')
                            await ctx.send(file=image_file, reference=ctx.message)
                else:
                    await ctx.send("Failed to fetch cat picture from API.")

    @handle_cat_picture.error
    async def handle_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            pass
        elif isinstance(error, MissingRequiredArgument):
            await ctx.send("A parameter is missing")
            return
        else:
            await ctx.send("Command no workey ping stabby")

async def setup(bot):
    await bot.add_cog(Cat(bot))
