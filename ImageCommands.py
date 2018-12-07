from discord.ext import commands
import discord
import random
import requests
import os

cwd = os.getcwd()

class ImageCommands:
    def __init__(self, bot):
        self.bot = bot


    @bot.command()
    async def cat(self, ctx):
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
    async def nickelback(self, ctx):
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
        await self.ctx.send(rand_song)


    @bot.command()
    async def harambe(self, ctx):
        '''
        posts a random image of harambe from the images folder
        '''
        harambe = 'Harambe' + str(random.randint(1,8)) + '.jpg'
        harambe_file = discord.File(cwd + '/pictures/harambe/' + harambe, "harambe")
        await self.ctx.send(file=harambe_file)


    @bot.command()
    async def aliens(self, ctx):
        '''
        aliens are real and they did everything cool in history
        '''
        alien_file = discord.File(cwd + '/pictures/aliens.png', "aliens")
        await self.ctx.send(file=alien_file)


    @bot.command()
    async def dva(self, ctx):
        '''
        gremlin dva image
        '''
        dva_file = discord.File(cwd + '/pictures/dva.png', "dva")
        await self.ctx.send(file=dva_file)


    @bot.command()
    async def mission(self, ctx):
        '''
        mission statement of thom stargazer
        '''
        mission_file= discord.File(cwd + '/pictures/thom_stargazer.jpg', "mission statement")
        await self.ctx.send(file=mission_file)


    @bot.command()
    async def goo(self, ctx):
        '''
        shoot your goo my dude
        '''
        goo_file = discord.File(cwd + '/pictures/goo.jpg', "goo")
        await self.ctx.send(file=goo_file)


    @bot.command()
    async def goo2(self, ctx):
        '''
        shoot goo dude???
        distorted shoot your goo image
        '''
        goo2_file = discord.File(cwd + '/pictures/goo2.png', "goo2")
        await self.ctx.send(file=goo2_file)


    @bot.command()
    async def dog(self, ctx):
        '''
        random dog in chat! sometiems posts videos
        '''
        await self.ctx.send(requests.get('https://random.dog/woof.json').json()['url'])


    @bot.command()
    async def skeleton(self, ctx):
        '''
        picks a random skeleton. very spooky
        happy halloween (or any day where you want a spoopy boi)
        '''
        skeleton = 'skeleton' + str(random.randint(1,19)) + '.jpg'
        skeleton_file = discord.File(cwd + '/pictures/skeletons/' + skeleton, "skeleton")
        await self.bot.send_file(file=skeleton_file)
