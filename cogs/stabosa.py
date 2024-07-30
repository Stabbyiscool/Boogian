import aiohttp
from discord.ext import commands
from io import BytesIO
import discord
import json
from PIL import Image
from discord.ext.commands import MissingRequiredArgument

with open('configs.json', 'r') as config_file:
    config = json.load(config_file)

class Stabosa(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='stabosa', aliases=['cascade'])
    @commands.cooldown(rate=1, per=config['COOLDOWN_TIME'], type=commands.BucketType.user)
    async def handle_neko_picture(self, ctx):
        async with aiohttp.ClientSession() as session:
            async with session.get('https://api.stabosa.fun/catgirl') as resp:
                if resp.status == 200:
                    data = await resp.json()
                    image_url = data.get('url')
                    async with session.get(image_url) as image_resp:
                        if image_resp.status == 200:
                            image_data = await image_resp.read()

                            image = Image.open(BytesIO(image_data))

                            if image.mode in ('RGBA', 'P'):
                                image = image.convert('RGB')
                            new_size = (int(image.width * 0.25), int(image.height * 0.25))
                            resized_image = image.resize(new_size, Image.LANCZOS)

                            image_buffer = BytesIO()
                            resized_image.save(image_buffer, format='JPEG')
                            image_buffer.seek(0)

                            image_file = discord.File(image_buffer, 'catgirl_picture.jpg')
                            await ctx.send(file=image_file, reference=ctx.message)
                else:
                    await ctx.send("Failed to fetch catgirl picture from API.")

    @handle_neko_picture.error
    async def handle_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            return
        elif isinstance(error, MissingRequiredArgument):
            await ctx.send("A parameter is missing")
            return
        else:
            await ctx.send("Command no workey ping stabby")

async def setup(bot):
    await bot.add_cog(Stabosa(bot))
