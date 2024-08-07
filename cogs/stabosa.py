import aiohttp
from discord.ext import commands
from io import BytesIO
import discord
import json
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
                            image_file = discord.File(BytesIO(image_data), 'catgirl_picture.jpg')
                            await ctx.send(file=image_file, reference=ctx.message)

    @handle_neko_picture.error
    async def handle_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            pass
        elif isinstance(error, MissingRequiredArgument):
            await ctx.send("A parameter is missing") 
            return
        else:
            await ctx.send("Command no workey ping stabby")


async def setup(bot):
    await bot.add_cog(Stabosa(bot))