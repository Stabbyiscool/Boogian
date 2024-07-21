import discord
from discord.ext import commands
import json
import time
import os
from discord.ext.commands import MissingRequiredArgument

with open('configs.json', 'r') as config_file:
    config = json.load(config_file)

TOKEN = config['TOKEN']
AUTHORIZED_USERS = [int(user_id) for user_id in config['AUTHORIZED_USERS']]
BANNED_USERS = [int(user_id) for user_id in config['BANNED_USERS']]
COOLDOWN_TIME = config['COOLDOWN_TIME']

client = commands.Bot(command_prefix='b.')

client.remove_command('help')

@client.event
async def on_ready():
    print('Boogian has conquered the vessel called', client.user)
    print(f'Authorized Users: {AUTHORIZED_USERS}')
    print(f'Banned Users: {BANNED_USERS}')
    await load_cogs()

@client.event
async def on_message(message):
    if message.author == client.user or message.author.id in BANNED_USERS:
        return

    await client.process_commands(message)

async def load_cogs():
    cogs_dir = '/home/stabosa/Documents/GitHub/Boogian/cogs'
    for cogpath in os.listdir(cogs_dir):
        if cogpath.endswith(".py"):
            try:
                cog_name = cogpath[:-3]
                await client.load_extension(f'cogs.{cog_name}')
                print(f'Loaded cog: {cogpath}')
            except Exception as e:
                print(f'Failed to load cog {cogpath}: {e}')

@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        return  
    else:
        print(f'Error occurred: {error}') 

client.run(TOKEN)
