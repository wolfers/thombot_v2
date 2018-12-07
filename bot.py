from discord.ext import commands
import discord
import asyncio
import re
import os

import logging

logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

from ImageCommands import ImageCommands
from OtherCommands import OtherCommands
#update Music file later and try to fix issues with it
#from Music import Music
from ValentinesDay2019 import ValentinesDay2019

cogs = [ImageCommands,
        OtherCommands,
        ValentinesDay2019
        ]

cwd = os.getcwd()

with open(cwd + '/token.txt', 'r') as f:
    token = f.read()

if not discord.opus.is_loaded():
    discord.opus.load_opus('/usr/lib/libopus.so')

description = """
    I am thom-bot. Created by protonheart for the thom stargazer memorial conglomerate.
    """

bot = commands.Bot(command_prefix=commands.when_mentioned_or('!'), description=description, pm_help=None)

for cog in cogs:
    bot.add_cog(cog)

async def on_ready():
    print('logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('-----')


@bot.event
async def on_member_join(member):
    '''
    Welcomes any new users to the server.
    '''
    bot.say('{} welcome {} to the server!'.format(member.roles[0].mention, member.mention))


@bot.event
async def on_message(message):
    '''
    checks if the member uses owo in their message and then responds
    in the correct manor.
    '''
    if re.search(r'( )owo( )', message.content) or message.content.startswith('owo'):
        await bot.send_message(message.channel, "*notices bulge* What's this?")
    await bot.process_commands(message)

bot.run(token[:-1])
