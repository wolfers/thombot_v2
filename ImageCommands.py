from discord.ext import commands
import random
import requests
# import CommandTracker


class ImageCommands:
    def __init__(self, bot):
        self.bot = bot

    # posts a random cat picture from either thecatapi or random.cat/meow
    @commands.command(pass_context=True)
    async def cat(self):
        ran_cat_link = random.choice(['http://thecatapi.com/api/images/get', 'http://random.cat/meow'])
        if ran_cat_link == 'http://random.cat/meow':
            ran_cat = requests.get(ran_cat_link).json()["file"]
        else:
            ran_cat = requests.get(ran_cat_link).url
        await self.bot.say(ran_cat)

    # posts a random nickelback song
    @commands.command(pass_context=True)
    async def nickelback(self):
        songs = ('https://www.youtube.com/watch?v=BB0DU4DoPP4', 'https://www.youtube.com/watch?v=4OjiOn5s8s8',
                 'https://www.youtube.com/watch?v=_1hgVcNzvzY', 'https://www.youtube.com/watch?v=PvxVNGdwVwk',
                 'https://www.youtube.com/watch?v=JtxpcQaSR0k',  'https://www.youtube.com/watch?v=76RbWuFll0Y',
                 'https://www.youtube.com/watch?v=1cQh1ccqu8M', 'https://www.youtube.com/watch?v=wQzn4a5qHT4',
                 'https://www.youtube.com/watch?v=-qcZ9M-QoOc', 'https://www.youtube.com/watch?v=5RtTFP2TNcM',
                 'https://www.youtube.com/watch?v=GP7zpdwo3Xo', 'https://www.youtube.com/watch?v=FIjRo-gMlKE',
                 'https://www.youtube.com/watch?v=vt-UtzP1u1g')
        rand_song = random.choice(songs)
        await self.bot.say(rand_song)

    # posts a random picture of harambe
    @commands.command(pass_context=True)
    async def harambe(self, ctx):
        harambe_pics = ('Harambe.jpg', 'Harambe2.jpg', 'Harambe3.jpg', 'Harambe4.jpg', 'Harambe5.jpg', 'Harambe6.jpg',
                        'Harambe7.jpg', 'Harambe8.jpg')
        await self.bot.send_file(ctx.message.channel, '/home/pi/thombot_v2/pictures/harambe/' +
                                 random.choice(harambe_pics))

    # posts a picture of the aliens guy
    @commands.command(pass_context=True)
    async def aliens(self, ctx):
        await self.bot.send_file(ctx.message.channel, '/home/pi/thombot_v2/pictures/aliens.png')

    # posts a picture of gremlin dva
    @commands.command(pass_context=True)
    async def dva(self, ctx):
        await self.bot.send_file(ctx.message.channel, '/home/pi/thombot_v2/pictures/dva.png')

    # posts the mission statement
    @commands.command(pass_context=True)
    async def mission(self, ctx):
        await self.bot.send_file(ctx.message.channel, '/home/pi/thombot_v2/pictures/thom_stargazer.jpg')

    # posts the shoot your goo picture
    @commands.command(pass_context=True)
    async def goo(self, ctx):
        await self.bot.send_file(ctx.message.channel, '/home/pi/thombot_v2/pictures/goo.jpg')

    # second goo picture
    @commands.command(pass_context=True)
    async def goo2(self, ctx):
        await self.bot.send_file(ctx.message.channel, '/home/pi/thombot_v2/pictures/goo2.png')

    # random dog picture
    @commands.command()
    async def dog(self):
        await self.bot.say(requests.get('https://random.dog/woof.json').json()['url'])

    # random skeleton picture
    @commands.command(pass_context=True)
    async def skeleton(self, ctx):
        skeleton = 'skeleton' + str(random.randint(1,19)) + '.jpg'
        await self.bot.send_file(ctx.message.channel, '/home/pi/thombot_v2/pictures/skeletons/' + skeleton)


def setup(bot):
    bot.add_cog(ImageCommands(bot))
