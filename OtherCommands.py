import discord
from discord.ext import commands
from Utils import textadd, create_gift_embed
import os
import random

cwd = os.getcwd()

'''
Temporary list conatining all of the gifts as a dict
'''

gift_list = [
    {"title": '"pet" collar', "url": "https://amzn.to/2r4SvvR", "description": "Get a nice collar for your favorite \"pet\". You'll love to see them wear it around the house during the holidays!"},
    {"title": "Golden Garbage Bags", "url": "https://amzn.to/2RbONfd", "description": "These garbage bags are probably made of solid gold! Waste disposal fit for a king."},
    {"title": "Log Pillow", "url": "https://amzn.to/2RdlokR", "description": "Thought you would love this log pillow since you hate going outside but nature is still important."},
    {"title": "Lock Pick Kit", "url": "https://amzn.to/2FQcatk", "description": "Instead of putting thought into getting you a nice gift, I got you this lockpicking set! I figure you can jsut go steal whatever you want, I got you the gift of anything that's secured using a simple lock!"},
    {"title": "Corn that never goes bad!", "url": "https://amzn.to/2TJymZm", "description": "Corn that doesn't go bad. I knew you'd love it. Just don't eat it. Put it on the shelf! yeah! Great conversation piece."},
    {"title": "BEES??", "url": "https://mountainsweethoney.com/bees/", "description": "RUN."},
    {"title": "Gross Poop Car", "url": "https://amzn.to/2r0xdPU", "description": "I didn't want this either, you can have it."},
    {"title": "pez", "url": "https://amzn.to/2DZO7GE", "description": "You know I love collectables, so you can have this part."},
    {"title": "Neon Sign", "url": "https://amzn.to/2E0EYxI", "description": "For that garage bar you've been wanting to set up. You know, the hangout for all the lads."},
    {"title": "Honda parts", "url": "https://sfbay.craigslist.org/sby/mpo/d/honda-parts/6734958149.html", "description": "it's, uh, for you. You have a car, right?"},
    {"title": "Slap Bracelet", "url": "https://amzn.to/2SfpNnx", "description": "You had one of thses when you were a kid and well, I didn't get to see you while I was in jail, hope you still like these."},
    {"title": "Placenta Face Mask", "url": "https://amzn.to/2S7DWD8", "description": "It's gotta be good for you skin or they wouldn't make it, right? I ahven't tried it, but I thought you could really use it."},
    {"title": "Beans", "url": "http://bit.ly/2Bx93m1", "description": "Things aren't looking so good, save these for a rough time. Might need them sooner rather than later."},
    {"title": "Burlap Sacks", "url": "https://www.ebay.com/i/292095591352?chn=ps", "description": "Used to use these all the time when I was a kid. Hope you enjoy themm as much as I did."},
    {"title": "Tire Valve Caps", "url": "https://amzn.to/2RdC9wh", "description": "Have fun, kid."},
    {"title": "Smile Trainer", "url": "https://amzn.to/2BxhGNG", "escription": "Your mom told me you really needed one of these."},
    {"title": "Pig Ski Mask", "url": "https://amzn.to/2DGzbwa", "description": "It's got pigs on it."},
    {"title": "Cow Heart", "url": "https://amzn.to/2DGzxTw", "description": "At least it's warmer than my wifes heart, HAHAHAHAHAHA, GET IT? Please help me."},
    {"title": "Stylish Shirt", "url": "https://amzn.to/2Alduyx", "description": "Did a lot of research into waht kinds like these days, I tried really hard on this one."},
    {"title": "Bird Mask", "url": "https://amzn.to/2P3eKMb", "description": "Coo coo, motherfucker!"},
    {"title": "Microwave Cooking for One", "url": "https://amzn.to/2QhTpDd", "description": "Maybe you wont need this someday."},
    {"title": "Waist Pouch", "url": "https://amzn.to/2r6jaby", "description": "This is so you can store you vape."},
    {"title": "Fruit Cake", "url": "https://amzn.to/2PXQSPd", "description": "I got you your favorite food!"},
    {"title": "A new yard", "url": "https://amzn.to/2RdW6Dh", "description": "I know you were going for that nature theme in the bathroom, I figured you could use this as a rug."},
    {"title": "Stained Glass", "url": "https://amzn.to/2DUrtjf", "description": "Walk on this to show your friends you're a badass."},
    {"title": "Shift Knob", "url": "https://amzn.to/2DNxKwj", "description": "This was my first beer when I turned 21. You'll pass this on to your kids when they're old enough too."},
    {"title": "Celery Seed", "url": "https://amzn.to/2AoXvzk", "description": "Your dad said you cook, so here's something that says celery in it."},
    {"title": "Urn", "url": "http://bit.ly/2QmiEUW", "description": "Ashes not included."},
    {"title": "Roof Wash", "url": "https://amzn.to/2DJ74wp", "description": "I'd love it if you came over after Christmas."},
    {"title": "Branding Irons", "url": "http://bit.ly/2zpzjx4", "description": "For that long term relationship."},
    {"title": "Dancing Pole", "url": "https://amzn.to/2r29xdS", "description": "Uncle Thom-bot thinks you'd be REALLY good at this."},
    {"title": "Aluminum Wire", "url": "https://amzn.to/2RfQ44U", "description": "It's got lots of uses! hitting people, bondage, making daigrams in the dirt, and uh, making fursuits, probably."}
]

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
    
    @commands.command(pass_context=True)
    async def merrychristmas(self, ctx):
        '''
        wip christmas command
        will give a random persent to whoever invokes the command
        '''
        gift = random.random(gift_list)
        gift_embed = create_gift_embed(gift["title"], gift["url"],
                                       gift["description"])
        await self.bot.send_message(ctx.message.channel, embed=gift_embed)


def setup(bot):
    bot.add_cog(OtherCommands(bot))
