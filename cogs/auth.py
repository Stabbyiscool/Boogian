import aiohttp
from discord.ext import commands
import discord
import json
import functools

def load_config():
    with open('configs.json', 'r') as config_file:
        return json.load(config_file)

@functools.lru_cache
def get_config():
    return load_config()

def reload_config():
    get_config.cache_clear()

class Auth(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def is_su(ctx):
        config = get_config()
        return str(ctx.author.id) in config['SU']

    @commands.command(name='auth')
    @commands.check(is_su)
    @commands.cooldown(rate=1, per=get_config()['COOLDOWN_TIME'], type=commands.BucketType.user)
    async def handle_auth(self, ctx, user: discord.User):
        config = get_config()
        user_id = str(user.id)
        if user_id not in config['AUTHORIZED_USERS']:
            config['AUTHORIZED_USERS'].append(user_id)
            with open('/DATA/Discordbots/selfbot/Boogianv5/configs.json', 'w') as config_file:
                json.dump(config, config_file, indent=4)
            reload_config()
            await ctx.send(f"User {user.name} has been authorized. Action pending for next restart of bot", reference=ctx.message)
        else:
            await ctx.send(f"User {user.name} is already authorized.", reference=ctx.message)

    @commands.command(name='unauth')
    @commands.check(is_su)
    async def handle_unauth(self, ctx, user: discord.User):
        config = get_config()
        user_id = str(user.id)
        if user_id in config['AUTHORIZED_USERS']:
            config['AUTHORIZED_USERS'].remove(user_id)
            with open('/DATA/Discordbots/selfbot/Boogianv5/configs.json', 'w') as config_file:
                json.dump(config, config_file, indent=4)
            reload_config()
            await ctx.send(f"User {user.name} has been unauthorized. Action pending for next restart of bot", reference=ctx.message)
        else:
            await ctx.send(f"User {user.name} is not authorized.", reference=ctx.message)

    @commands.command(name='ban')
    @commands.check(is_su)
    async def handle_ban(self, ctx, user: discord.User):
        config = get_config()
        user_id = str(user.id)
        if user_id not in config['BANNED_USERS']:
            config['BANNED_USERS'].append(user_id)
            with open('/DATA/Discordbots/selfbot/Boogianv5/configs.json', 'w') as config_file:
                json.dump(config, config_file, indent=4)
            reload_config()
            await ctx.send(f"User {user.name} has been banned. Action pending for next restart of bot.", reference=ctx.message)
        else:
            await ctx.send(f"User {user.name} is already banned.", reference=ctx.message)

    @commands.command(name='unban')
    @commands.check(is_su)
    async def handle_unban(self, ctx, user: discord.User):
        config = get_config()
        user_id = str(user.id)
        if user_id in config['BANNED_USERS']:
            config['BANNED_USERS'].remove(user_id)
            with open('/DATA/Discordbots/selfbot/Boogianv5/configs.json', 'w') as config_file:
                json.dump(config, config_file, indent=4)
            reload_config()
            await ctx.send(f"User {user.name} has been unbanned. Action pending for next restart of bot.", reference=ctx.message)
        else:
            await ctx.send(f"User {user.name} is not banned.", reference=ctx.message)

    @commands.command(name='standing')
    async def handle_standing(self, ctx, user: discord.User = None):
        config = get_config()
        target_user = user or ctx.author
        user_id = str(target_user.id)
        is_authed = "Y" if user_id in config['AUTHORIZED_USERS'] else "N"
        is_banned = "Y" if user_id in config['BANNED_USERS'] else "N"
        is_su = "Y" if user_id in config['SU'] else "N"
        await ctx.send(f"Authed: {is_authed}\nBanned: {is_banned}\nSU: {is_su}", reference=ctx.message)

    @commands.command(name='authlist')
    @commands.check(is_su)
    async def handle_authlist(self, ctx):
        config = get_config()
        authorized_users = config['AUTHORIZED_USERS']
        authorized_names = []

        for user_id in authorized_users:
            user = await self.bot.fetch_user(user_id)
            if user:
                authorized_names.append(user.name)
        
        if authorized_names:
            await ctx.send(f"Authorized Users: {', '.join(authorized_names)}", reference=ctx.message)
        else:
            await ctx.send("There are no authorized users.", reference=ctx.message)

    @commands.command(name='banlist')
    @commands.check(is_su)
    async def handle_banlist(self, ctx):
        config = get_config()
        banned_users = config['BANNED_USERS']
        banned_names = []

        for user_id in banned_users:
            user = await self.bot.fetch_user(user_id)
            if user:
                banned_names.append(user.name)
        
        if banned_names:
            await ctx.send(f"Banned Users: {', '.join(banned_names)}", reference=ctx.message)
        else:
            await ctx.send("There are no banned users.", reference=ctx.message)

    @handle_auth.error
    @handle_unauth.error
    @handle_ban.error
    @handle_unban.error
    @handle_standing.error
    @handle_authlist.error
    @handle_banlist.error
    async def handle_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            return
        elif isinstance(error, commands.CheckFailure):
            await ctx.send("You are not SU")
        else:
            await ctx.send(f"An error occurred: {str(error)}")

async def setup(bot):
    await bot.add_cog(Auth(bot))