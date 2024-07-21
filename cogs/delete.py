import discord
from discord.ext import commands
import json

with open('configs.json', 'r') as config_file:
    config = json.load(config_file)

class Delete(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='delete')
    @commands.cooldown(rate=1, per=config['COOLDOWN_TIME'], type=commands.BucketType.user)
    async def delete(self, ctx, message_id: int):
        if str(ctx.author.id) not in config['SU']:
            await ctx.send("Ur not su bro")
            return

        try:
            message = await ctx.channel.fetch_message(message_id)
            
            if message.author == self.bot.user:
                await message.delete()
            else:
                await ctx.send("I didnt send that :cry:")
        
        except discord.NotFound:
            await ctx.send("cant find the message")
        except discord.Forbidden:
            await ctx.send("cant")
        except discord.HTTPException as e:
            await ctx.send(f"An error occurred: {e}")

    @delete.error
    async def handle_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            return
        elif isinstance(error, MissingRequiredArgument):
            await ctx.send("A parameter is missing") 
        else:
            await ctx.send("Command no workey ping stabby")


async def setup(bot):
    await bot.add_cog(Delete(bot))
