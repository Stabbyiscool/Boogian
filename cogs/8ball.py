import discord
from discord.ext import commands
import aiohttp
import json
import tempfile
import os
from discord.ext.commands import MissingRequiredArgument

with open('configs.json', 'r') as config_file:
    config = json.load(config_file)

class EightBall(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='8ball')
    @commands.cooldown(rate=1, per=config['COOLDOWN_TIME'], type=commands.BucketType.user)
    async def eight_ball(self, ctx, *, question: str):
        url = f'https://api.stabosa.fun/8ball/?question={question}'

        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    if response.content_type == 'application/json':
                        data = await response.json()
                        answer = data.get('answer', 'I am unable to provide an answer at this time noob.')
                        image_url = data.get('image', None)

                        if image_url:
                            await ctx.send(content=answer)
                            await ctx.send(image_url)
                        else:
                            await ctx.send(answer)
                    elif response.content_type == 'image/png':
                        image_bytes = await response.read()
                        with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as image_file:
                            image_file.write(image_bytes)
                            temp_filename = image_file.name
                        await ctx.send(file=discord.File(temp_filename, '8ball.png'))
                        os.remove(temp_filename)
                    else:
                        await ctx.send('Badfile')
                else:
                    await ctx.send('Failed to fetch the answer. Api down???')

    @eight_ball.error
    async def handle_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            return
        elif isinstance(error, MissingRequiredArgument):
            await ctx.send("A parameter is missing") 
            return
        else:
            await ctx.send("Command no workey ping stabby")
async def setup(bot):
    await bot.add_cog(EightBall(bot))