import discord
from discord.ext import commands
import os
import random
from PIL import ImageFont, Image, ImageDraw

font = ImageFont.truetype("comic-sans.ttf", 40)

cwd = os.getcwd()

def textadd(message):
    '''
    draws the text onto the goo image.
    '''
    with Image.open(cwd + "/pictures/blankgoo.png") as img:
        draw = ImageDraw.Draw(img)
        message = textprep(message)
        draw.text((420, 150), message, fill=(0,0,0,0), font=font)
        draw = ImageDraw.Draw(img)
        img.save(cwd + "/pictures/gootext.png")


def textprep(message):
    '''
    tries to fit the text onto the page.
    This function needs to be updated. It works but not well.
    '''
    letter_list = []
    line_list = []
    for letter in message:
        if len(letter_list) <= 2 or letter != " ":
            letter_list.append(letter)
        else:
            line = "".join(letter_list)
            line_list.append(line)
            letter_list = []
    line = "".join(letter_list)
    line_list.append(line)
    text = "\n".join(line_list)
    return text 


class otherCommands:
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def slab(self, ctx):
        '''
        you're cursed until you return it.
        '''
        await ctx.send('RETURN THE SLAAAAB')


    @commands.command()
    @commands.guild_only()
    async def ban(self, ctx):
        '''
        Actually for real "bans" someone from the server
        '''
        await ctx.send('you\'ve been banned, {}!'.format(ctx.message.mentions[0].mention))


    @commands.command()
    async def WehavenobeginningWehavenoendWeareinfiniteMillionsofyearsafteryourcivilizationhasbeeneradicatedandforgottenwewillendure(self, ctx):
        '''
        This will never be used.
        '''
        await ctx.send('We impose order on the chaos of organic evolution. You exist because we allow it, and you will end because we demand it. ')


    @commands.command()
    async def gooedit(self, ctx):
        '''
        Shoot your goo but the way you always wanted it, with your own, dumb words all over it.
        '''
        textadd(ctx.message.content[9:])
        gooedit_file = discord.File(cwd + "/pictures/gootext.png")
        await ctx.send(file=gooedit_file)

def setup(bot):
    bot.add_cog(otherCommands(bot))
