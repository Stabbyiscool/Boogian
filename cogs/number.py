import discord
from discord.ext import commands

class Counter(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:
            return

        if message.channel.id == 1142556779373396089:  # Channel id (this is for servers with the counter bot)
            if message.content.isdigit():
                number = int(message.content)
                incremented_number = number + 1

                await message.channel.send(str(incremented_number))

async def setup(bot):
    await bot.add_cog(Counter(bot))
