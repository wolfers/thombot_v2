from discord.ext import commands
import discord
import asyncio
import re
import os
import sys, traceback

import logging
import logging.handlers

cwd = os.getcwd()

with open(cwd + '/token.txt', 'r') as f:
    token = f.read()

if not discord.opus.is_loaded():
    discord.opus.load_opus('/usr/lib/libopus.so')

description = """
    I am thom-bot. Created by protonheart for the thom stargazer memorial conglomerate.
    """

bot = commands.Bot(command_prefix=commands.when_mentioned_or('!'), description=description)

initial_extentions = ['cogs.otherCommands',
                      'cogs.imageCommands',
                      'cogs.Music',
                      'cogs.moderation']

for extention in initial_extentions:
    try:
        bot.load_extension(extention)
    except Exception as e:
        print(f'Failed to load extention {extention}.', file=sys.stderr)
        traceback.print_exc()


@bot.event
async def on_ready():
    print('logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('-----')
    await bot.change_presence(activity=discord.Game(name='fordnight'))

bot.run(token[:-1])
