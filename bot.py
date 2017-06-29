from discord.ext import commands

#contains token to log in the bot
from discord_tokens import *

description = """
    I am thom-bot! I'm here to make things more dumb!!!
    """

#the extentions that contain all the bot commands
startup_extensions = [  "image_commands",
                        "other_commands"]

bot = commands.Bot(command_prefix='!', description=description)

@bot.event
async def on_ready():
    print('logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('-----')

#Welcome new members that join the server
@bot.event
async def on_member_join(member):
    bot.say('{} welcome {} to the server!'.format(member.roles[0].mention, member.mention))

#load the extention files that contain the commands for the bot
if __name__ == "__main__":
    for extension in startup_extensions:
        try:
            bot.load_extension(extension)
        except Exception as e:
            exc = '{}: {}'.format(type(e).__name__, e)
            print('failed to load extension {}\n{}'.format(extension, exc))

#run the bot
bot.run(token)
