from discord.ext import commands
import discord
import re

# contains token to log in the bot
from discord_tokens import *

if not discord.opus.is_loaded():
    discord.opus.load_opus('/usr/lib/libopus.so')

description = """
    I am thom-bot! I'm here to make things more dumb!!!
    """

# the extentions that contain all the bot commands
startup_extensions = ["ImageCommands",
                      "OtherCommands",
                      "Music"]

bot = commands.Bot(command_prefix='!', description=description)


@bot.event
async def on_ready():
    print('logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('-----')


# Welcome new members that join the server
@bot.event
async def on_member_join(member):
    bot.say('{} welcome {} to the server!'.format(member.roles[0].mention, member.mention))


@bot.event
async def on_message(message):
    if re.search(r'( )owo( )', message.content) or message.content.startswith('owo'):
        await bot.send_message(message.channel, '*notices bulge* What\'s this?')
    await bot.process_commands(message)

# load the extention files that contain the commands for the bot
if __name__ == "__main__":
    for extension in startup_extensions:
        try:
            bot.load_extension(extension)
        except Exception as e:
            exc = '{}: {}'.format(type(e).__name__, e)
            print('failed to load extension {}\n{}'.format(extension, exc))

# run the bot
bot.run(token)
