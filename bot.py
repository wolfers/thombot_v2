from discord.ext import commands
import discord
import asyncio
import re
import os
import sys, traceback

import logging

logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

cwd = os.getcwd()

with open(cwd + '/token.txt', 'r') as f:
    token = f.read()

if not discord.opus.is_loaded():
    discord.opus.load_opus('/usr/lib/libopus.so')

description = """
    I am thom-bot. Created by protonheart for the thom stargazer memorial conglomerate.
    """

bot = commands.Bot(command_prefix=commands.when_mentioned_or('!'), description=description)

initial_extentions = [#'holidaycogs.etc',
                      'cogs.otherCommands',
                      'cogs.imageCommands',
                      'cogs.Music',]

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
    await bot.change_presence(activity=discord.Game(name='christmas music'))

bot.run(token[:-1])
