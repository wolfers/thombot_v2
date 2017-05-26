from discord.ext import commands
import discord
from discord_tokens import *

description = """
    I am thom bot! I'm here to make things more dumb!!!
    """

startup_extensions = ["cogs.image_commands"]

bot = commands.Bot(command_prefix='!', description=description)

@bot.event
async def on_ready():
    print('logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('-----')

@bot.event
async def on_member_join(member):
    bot.say('{} welcome {} to the server!'.format(member.roles[0].mention, member.mention))

if __name__ == "__main__":
    for extension in startup_extensions:
        try:
            bot.load_extension(extension)
        except Exception as e:
            exc = '{}: {}'.format(type(e).__name__, e)
            print('failed to load extention {}\n{}'.format(extention, exc))

bot.run(token)
