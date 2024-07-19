import aiohttp
from discord.ext import commands
from io import BytesIO
import discord
import json

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
                            file_extension = image_url.split('.')[-1] 
                            image_file = discord.File(BytesIO(image_data), f'cat_picture.{file_extension}')
                            await ctx.send(file=image_file, reference=ctx.message)
                else:
                    await ctx.send("Failed to fetch cat picture from API.")

    @handle_cat_picture.error
    async def handle_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            return
        else:
            await ctx.send("An error occurred while processing the command.")

async def setup(bot):
    await bot.add_cog(Cat(bot))
