import discord
from discord.ext import commands
from Utils import textadd
import os
import random

cwd = os.getcwd()

class OtherCommands:
    def __init__(self, bot):
        self.bot = bot

    @bot.command()
    async def slab(self, ctx):
        '''
        posts the text into chat.
        you're cursed until you return it.
        '''
        await self.ctx.send('RETURN THE SLAAAAB')


    @bot.command()
    async def stfu(self, ctx):
        '''
        posts the stfu filthy frank song
        might remove this in the future.
        '''
        await self.ctx.send('https://youtu.be/OLpeX4RRo28')


    @bot.command()
    async def ban(self, ctx):
        '''
        Actually for real "bans" someone from the server
        '''
        await self.ctx.send('you\'ve been banned, {}!'.format(ctx.message.mentions[0].mention))


    @bot.command()
    async def WehavenobeginningWehavenoendWeareinfiniteMillionsofyearsafteryourcivilizationhasbeeneradicatedandforgottenwewillendure(self, ctx):
        '''
        This will never be used.
        '''
        await self.ctx.send('We impose order on the chaos of organic evolution. You exist because we allow it, and you will end because we demand it. ')


    @bot.command()
    async def gooedit(self, ctx):
        '''
        This command runs the textadd to add text to a blank
        copy of the shoot your goo image then posts the iamge.
        '''
        textadd(ctx.message.content[9:])
        gooedit_file = discord.File(cwd + "/pictures/gootext.png", "goo")
        await self.ctx.send(file=gooedit_file)
