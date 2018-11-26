from discord.ext import commands
import discord
import re
import os

cwd = os.getcwd()

with open(cwd + '/token.txt', 'r') as f:
    token = f.read()

print(token)
print(token[:-1])

if not discord.opus.is_loaded():
    discord.opus.load_opus('/usr/lib/libopus.so')

description = """
    I am thom-bot! I'm here to make things more dumb!!!
    """

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


if __name__ == "__main__":
    for extension in startup_extensions:
        try:
            bot.load_extension(extension)
        except:
            pass


bot.run(token[:-1])
