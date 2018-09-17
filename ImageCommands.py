from discord.ext import commands
import random
import requests


class ImageCommands:
    def __init__(self, bot):
        self.bot = bot


    @commands.command(pass_context=True)
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
        await self.bot.say(ran_cat)


    @commands.command(pass_context=True)
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


    @commands.command(pass_context=True)
    async def harambe(self, ctx):
        '''
        posts a random image of harambe from the images folder
        '''
        harambe_pics = ('Harambe.jpg', 'Harambe2.jpg', 'Harambe3.jpg',
                        'Harambe4.jpg', 'Harambe5.jpg', 'Harambe6.jpg',
                        'Harambe7.jpg', 'Harambe8.jpg')
        harambe = 'Harambe' + str(random.randint(1,8)) + '.jpg'
        await self.bot.send_file(ctx.message.channel,
                                 '/home/ubuntu/thombot_v2/pictures/harambe/' +
                                 harambe)


    @commands.command(pass_context=True)
    async def aliens(self, ctx):
        '''
        aliens are real and they did everything cool in history
        '''
        await self.bot.send_file(ctx.message.channel,
                                 '/home/ubuntu/thombot_v2/pictures/aliens.png')


    @commands.command(pass_context=True)
    async def dva(self, ctx):
        '''
        gremlin dva image
        '''
        await self.bot.send_file(ctx.message.channel,
                                 '/home/ubuntu/thombot_v2/pictures/dva.png')


    @commands.command(pass_context=True)
    async def mission(self, ctx):
        '''
        mission statement of thom stargazer
        '''
        await self.bot.send_file(ctx.message.channel,
                                 '/home/ubuntu/thombot_v2/pictures/thom_stargazer.jpg')


    @commands.command(pass_context=True)
    async def goo(self, ctx):
        '''
        shoot your goo my dude
        '''
        await self.bot.send_file(ctx.message.channel,
                                 '/home/ubuntu/thombot_v2/pictures/goo.jpg')


    @commands.command(pass_context=True)
    async def goo2(self, ctx):
        '''
        shoot goo dude???
        distorted shoot your goo image
        '''
        await self.bot.send_file(ctx.message.channel,
                                 '/home/ubuntu/thombot_v2/pictures/goo2.png')


    @commands.command()
    async def dog(self):
        '''
        random dog in chat! sometiems posts videos
        '''
        await self.bot.say(requests.get('https://random.dog/woof.json').json()['url'])


    @commands.command(pass_context=True)
    async def skeleton(self, ctx):
        '''
        picks a random skeleton. very spooky
        happy halloween (or any day where you want a spoopy boi)
        '''
        skeleton = 'skeleton' + str(random.randint(1,19)) + '.jpg'
        await self.bot.send_file(ctx.message.channel,
                                 './pictures/skeletons/' +
                                  skeleton)


def setup(bot):
    bot.add_cog(ImageCommands(bot))
