import discord
from discord.ext import commands
from Utils import textadd
import os
import random

cwd = os.getcwd()

class OtherCommands:
    def __init__(self, bot):
        self.bot = bot


    @commands.command(pass_context=True)
    async def gameset(self, ctx):
        '''
        Sets the playing tag for the bot. 
        Only someone with the bot friend role can use this command
        '''
        print(ctx.message.author.id)
        for role in ctx.message.author.roles:
            if role.name == 'bot friend' or ctx.message.author.id == '88838960175910912':
                game_name = ctx.message.content[9:]
                await self.bot.change_presence(game=discord.Game(name=game_name))
                break
        else:
            await self.bot.say('I\'m afraid I can\'t do that, {}.'.format(ctx.message.author.mention))


    @commands.command(pass_context=True)
    async def setavatar(self, ctx):
        '''
        Sets the avatar picture for the bot to the image named avatar.jpg
        in the images folder.
        '''
        for role in ctx.message.author.roles:
            if role.name == 'bot friend':
                avatar = open(cwd + '/pictures/avatar.jpg', 'rb')
                await self.bot.edit_profile(avatar=avatar.read())
                break
        else:
            await self.bot.say('I\'m afraid I can\'t do that, {}.'.format(ctx.message.author.mention))


    @commands.command(pass_context=True)
    async def slab(self, ctx):
        '''
        posts the text into chat.
        you're cursed until you return it.
        '''
        await self.bot.say('RETURN THE SLAAAAB')


    @commands.command(pass_context=True)
    async def stfu(self, ctx):
        '''
        posts the stfu filthy frank song
        might remove this in the future.
        '''
        await self.bot.say('https://youtu.be/OLpeX4RRo28')


    @commands.command(pass_context=True)
    async def ban(self, ctx):
        '''
        Actually for real "bans" someone from the server
        '''
        await self.bot.say('you\'ve been banned, {}!'.format(ctx.message.mentions[0].mention))


    @commands.command(pass_context=True)
    async def WehavenobeginningWehavenoendWeareinfiniteMillionsofyearsafteryourcivilizationhasbeeneradicatedandforgottenwewillendure(self, ctx):
        '''
        This will never be used.
        '''
        await self.bot.say('We impose order on the chaos of organic evolution. You exist because we allow it, and you will end because we demand it. ')


    @commands.command(pass_context=True)
    async def gooedit(self, ctx):
        '''
        This command runs the textadd to add text to a blank
        copy of the shoot your goo image then posts the iamge.
        '''
        textadd(ctx.message.content[9:])
        await self.bot.send_file(ctx.message.channel, cwd + "/pictures/gootext.png")

def setup(bot):
    bot.add_cog(OtherCommands(bot))
