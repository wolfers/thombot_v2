import discord
from discord.ext import commands


class OtherCommands():
    def __init__(self, bot):
        self.bot = bot

    # sets the playing tag for the bot. only someone with the bot friend role can change this.
    @commands.command(pass_context=True)
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

    # sets the avatar picture for the bot. It wasn't working on the website so I made this command to update it manually
    # it takes whatever picture you give it in the images folder. Need bot friend role to use command
    @commands.command(pass_context=True)
    async def setavatar(self, ctx):
        role_test = 1
        for role in ctx.message.author.roles:
            if role.name == 'bot friend':
                avatar = open('/home/pi/thombot/pictures/avatar.jpg', 'rb')
                await self.bot.edit_profile(avatar=avatar.read())
                role_test = 0
                break
        if role_test == 1:
            await self.bot.say('You\'re not a bot friend!')

    # post in chat the text
    @commands.command()
    async def slab(self):
        await self.bot.say('RETURN THE SLAAAAB')

    # posts the filthy frank song
    @commands.command()
    async def stfu(self):
        await self.bot.say('https://youtu.be/OLpeX4RRo28')

    # "bans" someone (just says they're banned in chat"
    @commands.command(pass_context=True)
    async def ban(self, ctx):
        await self.bot.say('you\'ve been banned, {}!'.format(ctx.message.mentions[0].mention))

    # nick's cooking blog that he probably wont update after the first post
    @commands.command()
    async def cooking(self):
        await self.bot.say('https://itsyourlifeloafofbread.tumblr.com/')


def setup(bot):
    bot.add_cog(OtherCommands(bot))
