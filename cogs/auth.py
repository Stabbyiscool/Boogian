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
            with open('configs.json', 'w') as config_file:
                json.dump(config, config_file, indent=4)
            reload_config()
            await ctx.send(f"User {user.name} ({user_id}) has been authorized. Action pending for next restart of bot.", reference=ctx.message)
        else:
            await ctx.send(f"User {user.name} ({user_id}) is already authorized.", reference=ctx.message)

    @commands.command(name='unauth')
    @commands.check(is_su)
    async def handle_unauth(self, ctx, user: discord.User):
        config = get_config()
        user_id = str(user.id)
        if user_id in config['AUTHORIZED_USERS']:
            config['AUTHORIZED_USERS'].remove(user_id)
            with open('configs.json', 'w') as config_file:
                json.dump(config, config_file, indent=4)
            reload_config()
            await ctx.send(f"User {user.name} ({user_id}) has been unauthorized. Action pending for next restart of bot.", reference=ctx.message)
        else:
            await ctx.send(f"User {user.name} ({user_id}) is not authorized.", reference=ctx.message)

    @commands.command(name='ban')
    @commands.check(is_su)
    async def handle_ban(self, ctx, user: discord.User, *, reason: str):
        config = get_config()
        user_id = str(user.id)
        if user_id not in config['BANNED_USERS']:
            config['BANNED_USERS'][user_id] = reason
            with open('configs.json', 'w') as config_file:
                json.dump(config, config_file, indent=4)
            reload_config()
            await ctx.send(f"User {user.name} ({user_id}) has been banned for: {reason}. Action pending for next restart of bot.", reference=ctx.message)
        else:
            await ctx.send(f"User {user.name} ({user_id}) is already banned.", reference=ctx.message)

    @commands.command(name='unban')
    @commands.check(is_su)
    async def handle_unban(self, ctx, user: discord.User):
        config = get_config()
        user_id = str(user.id)
        if user_id in config['BANNED_USERS']:
            del config['BANNED_USERS'][user_id]
            with open('configs.json', 'w') as config_file:
                json.dump(config, config_file, indent=4)
            reload_config()
            await ctx.send(f"User {user.name} ({user_id}) has been unbanned. Action pending for next restart of bot.", reference=ctx.message)
        else:
            await ctx.send(f"User {user.name} ({user_id}) is not banned.", reference=ctx.message)

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
                authorized_names.append(f"{user.name} ({user_id})")
        
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

        for user_id, reason in banned_users.items():
            user = await self.bot.fetch_user(user_id)
            if user:
                banned_names.append(f"{user.name} ({user_id})")
        
        if banned_names:
            await ctx.send(f"Banned Users: {', '.join(banned_names)}", reference=ctx.message)
        else:
            await ctx.send("There are no banned users.", reference=ctx.message)

    @commands.command(name='sulist')
    @commands.check(is_su)
    async def handle_sulist(self, ctx):
        config = get_config()
        SU_users = config['SU']
        SU_names = []

        for user_id in SU_users:
            user = await self.bot.fetch_user(user_id)
            if user:
                SU_names.append(f"{user.name} ({user_id})")
        
        if SU_names:
            await ctx.send(f"SU Users: {', '.join(SU_names)}", reference=ctx.message)
        else:
            await ctx.send("There are no SU users.", reference=ctx.message)

    @commands.command(name='baninfo')
    @commands.check(is_su)
    async def handle_baninfo(self, ctx, user_id: str):
        config = get_config()
        if user_id in config['BANNED_USERS']:
            reason = config['BANNED_USERS'][user_id]
            user = await self.bot.fetch_user(user_id)
            if user:
                await ctx.send(f"User {user.name} ({user_id}) was banned for: {reason}", reference=ctx.message)
            else:
                await ctx.send(f"User ID {user_id} was banned for: {reason}", reference=ctx.message)
        else:
            await ctx.send(f"User ID {user_id} is not banned.", reference=ctx.message)

    @handle_auth.error
    @handle_unauth.error
    @handle_ban.error
    @handle_unban.error
    @handle_standing.error
    @handle_authlist.error
    @handle_banlist.error
    @handle_sulist.error
    @handle_baninfo.error
    async def handle_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            return
        elif isinstance(error, commands.CheckFailure):
            await ctx.send("You are noot SU.")
        else:
            await ctx.send(f"An error occurred: {str(error)}")

async def setup(bot):
    await bot.add_cog(Auth(bot))
