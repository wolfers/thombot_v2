import discord
from dsicord.ext import commands

class other_commands():
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context = True)
    async def gameset(self, ctx):
        role_test = 1
        for role in ctx.message.author.roles:
            if role.name == 'bot friend':
                game_name = ctx.message.content[9:]
                await self.bot.change_presence(game=discord.Game(name=game_name))
                role_test = 0
                break
        if role_test == 1:
            await self.bot.say('you\'re not a bot friend!')

    @commands.command()
    async def setavatar(self):
        role_test = 1
        for role in message.author.roles:
            if role.name == 'bot friend':
                avatar = open('/home/pi/thombot/pictures/avatar.jpg', 'rb')
                await self.bot.edit_profile(avatar=avatar.read())
                role_test = 0
                break
        if role_test == 1:
            await self.bot.say('You\'re not a bot friend!')

    @commands.command()
    async def stfu(self):
        await self.bot.say('https://youtu.be/OLpeX4RRo28')

    @commands.command
    async def ban(self):
        await self.bot.say('you\'ve been banned, {}!'.format(message.mentions[0].mention))

    @commands.command()
    async def cooking(self):
        await self.bot.say('https://itsyourlifeloafofbread.tumblr.com/')
        
def setup(bot):
    bot.add_cog(other_commands(bot))
