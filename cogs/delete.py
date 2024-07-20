import aiohttp
from discord.ext import commands
from io import BytesIO
import discord
import json

with open('configs.json', 'r') as config_file:
    config = json.load(config_file)

class Delete(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='delete')
    @commands.cooldown(rate=1, per=config['COOLDOWN_TIME'], type=commands.BucketType.user)
    async def delete(self, ctx, message_id: int):
        su_role = discord.utils.get(ctx.guild.roles, name='SU')
        if su_role not in ctx.author.roles:
            await ctx.send("Ur not su")
            return

        try:
            message = await ctx.fetch_message(message_id)
            
            if message.author == self.bot.user:
                await message.delete()
                await ctx.send("Message deleted bruh")
            else:
                await ctx.send("The message was not sent by this bot ya big dummy")
        except discord.NotFound:
            await ctx.send("Message not found lil bro")
        except discord.Forbidden:
            await ctx.send("I do not have permission to delete this message bruh")
        except discord.HTTPException as e:
            await ctx.send(f"An error occurred: {e}")

    @delete.error
    async def handle_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            return
        else:
            await ctx.send(f"An error occurred: {error}")

async def setup(bot):
    await bot.add_cog(Delete(bot))
