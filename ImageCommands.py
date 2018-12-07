from discord.ext import commands
import random
import requests
import os

cwd = os.getcwd()

class ImageCommands:
    def __init__(self, bot):
        self.bot = bot


    @bot.command()
    async def cat(self):
        '''
        Grabs a random cat iamge from one of the two apis and
        sends it to the chat
        '''
        ran_cat_link = random.choice(['http://thecatapi.com/api/images/get',
                                      'http://random.cat/meow'])
        if ran_cat_link == 'http://random.cat/meow':
            ran_cat = requests.get(ran_cat_link).json()["file"]
        else:
            ran_cat = requests.get(ran_cat_link).url
        await self.ctx.send(ran_cat)


    @bot.command()
    async def nickelback(self):
        '''
        posts a random nickleback song from the list
        list is expandable if needed
        '''
        songs = ('https://www.youtube.com/watch?v=BB0DU4DoPP4',
                 'https://www.youtube.com/watch?v=4OjiOn5s8s8',
                 'https://www.youtube.com/watch?v=_1hgVcNzvzY',
                 'https://www.youtube.com/watch?v=PvxVNGdwVwk',
                 'https://www.youtube.com/watch?v=JtxpcQaSR0k',
                 'https://www.youtube.com/watch?v=76RbWuFll0Y',
                 'https://www.youtube.com/watch?v=1cQh1ccqu8M',
                 'https://www.youtube.com/watch?v=wQzn4a5qHT4',
                 'https://www.youtube.com/watch?v=-qcZ9M-QoOc',
                 'https://www.youtube.com/watch?v=5RtTFP2TNcM',
                 'https://www.youtube.com/watch?v=GP7zpdwo3Xo',
                 'https://www.youtube.com/watch?v=FIjRo-gMlKE',
                 'https://www.youtube.com/watch?v=vt-UtzP1u1g')
        rand_song = random.choice(songs)
        await self.bot.say(rand_song)


    @bot.command()
    async def harambe(self, ctx):
        '''
        posts a random image of harambe from the images folder
        '''
        harambe = 'Harambe' + str(random.randint(1,8)) + '.jpg'
        await self.bot.send_file(ctx.message.channel,
                                 cwd + '/pictures/harambe/' +
                                 harambe)


    @bot.command()
    async def aliens(self, ctx):
        '''
        aliens are real and they did everything cool in history
        '''
        await self.bot.send_file(ctx.message.channel,
                                 cwd + '/pictures/aliens.png')


    @bot.command()
    async def dva(self, ctx):
        '''
        gremlin dva image
        '''
        await self.bot.send_file(ctx.message.channel,
                                 cwd + '/pictures/dva.png')


    @bot.command()
    async def mission(self, ctx):
        '''
        mission statement of thom stargazer
        '''
        await self.bot.send_file(ctx.message.channel,
                                 cwd + '/pictures/thom_stargazer.jpg')


    @bot.command()
    async def goo(self, ctx):
        '''
        shoot your goo my dude
        '''
        await self.bot.send_file(ctx.message.channel,
                                 cwd + '/pictures/goo.jpg')


    @bot.command()
    async def goo2(self, ctx):
        '''
        shoot goo dude???
        distorted shoot your goo image
        '''
        await self.bot.send_file(ctx.message.channel,
                                 cwd + '/pictures/goo2.png')


    @bot.command()
    async def dog(self, _):
        '''
        random dog in chat! sometiems posts videos
        '''
        await self.bot.say(requests.get('https://random.dog/woof.json').json()['url'])


    @bot.command()
    async def skeleton(self, ctx):
        '''
        picks a random skeleton. very spooky
        happy halloween (or any day where you want a spoopy boi)
        '''
        skeleton = 'skeleton' + str(random.randint(1,19)) + '.jpg'
        await self.bot.send_file(ctx.message.channel,
                                 cwd + '/pictures/skeletons/' +
                                  skeleton)
