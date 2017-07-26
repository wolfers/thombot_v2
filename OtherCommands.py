import discord
from discord.ext import commands
# import CommandTracker


class OtherCommands:
    def __init__(self, bot):
        self.bot = bot

    # sets the playing tag for the bot. only someone with the bot friend role can change this.
    @commands.command(pass_context=True)
    async def gameset(self, ctx):
        print(ctx.message.author.id)
        for role in ctx.message.author.roles:
            if role.name == 'bot friend' or ctx.message.author.id == '88838960175910912':
                game_name = ctx.message.content[9:]
                await self.bot.change_presence(game=discord.Game(name=game_name))
                break
        else:
            await self.bot.say('I\'m afraid I can\'t do that, {}.'.format(ctx.message.author.mention))

    # sets the avatar picture for the bot. It wasn't working on the website so I made this command to update it manually
    # it takes whatever picture you give it in the images folder. Need bot friend role to use command
    @commands.command(pass_context=True)
    async def setavatar(self, ctx):
        for role in ctx.message.author.roles:
            if role.name == 'bot friend':
                avatar = open('/home/pi/thombot_v2/pictures/avatar.jpg', 'rb')
                await self.bot.edit_profile(avatar=avatar.read())
                break
        else:
            await self.bot.say('I\'m afraid I can\'t do that, {}.'.format(ctx.message.author.mention))

    # retrieve the commands that a user has used
    # @commands.command(pass_context=True)
    # async def used_commands(self, ctx):
    #     command_dict = CommandTracker.used_commands(ctx.message.author.id)
    #     print_list = ''
    #     for command in command_dict:
    #         print_list += (command + ': ' + str(command_dict[command]) + ' ')
    #     await self.bot.say(print_list)

    # post in chat the text
    @commands.command(pass_context=True)
    async def slab(self, ctx):
        # CommandTracker.add_entry(ctx.message.author.id, 'slab')
        await self.bot.say('RETURN THE SLAAAAB')

    # posts the filthy frank song
    @commands.command(pass_context=True)
    async def stfu(self, ctx):
        # CommandTracker.add_entry(ctx.message.author.id, 'stfu')
        await self.bot.say('https://youtu.be/OLpeX4RRo28')

    # "bans" someone (just says they're banned in chat"
    @commands.command(pass_context=True)
    async def ban(self, ctx):
        # CommandTracker.add_entry(ctx.message.author.id, 'ban')
        await self.bot.say('you\'ve been banned, {}!'.format(ctx.message.mentions[0].mention))

    # nick's cooking blog that he probably wont update after the first post
    @commands.command(pass_context=True)
    async def cooking(self, ctx):
        # CommandTracker.add_entry(ctx.message.author.id, 'cooking')
        await self.bot.say('https://itsyourlifeloafofbread.tumblr.com/')

    @commands.command(pass_context=True)
    async def WehavenobeginningWehavenoendWeareinfiniteMillionsofyearsafteryourcivilizationhasbeeneradicatedandforgottenwewillendure(self, ctx):
        # CommandTracker.add_entry(ctx.message.author.id, 'mass effect')
        await self.bot.say('We impose order on the chaos of organic evolution. You exist because we allow it, and you will end because we demand it. ')

def setup(bot):
    bot.add_cog(OtherCommands(bot))
