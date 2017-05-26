import discord
from discord.ext import commands

class image_commands():
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def cat(self):
        ran_cat_link = random.choice(['http://thecatapi.com/api/images/get','http://random.cat/meow'])
        if ran_cat_link == 'http://random.cat/meow':
            ran_cat = requests.get(ran_cat_link).json()["file"]
        else:
            ran_cat = requests.get(ran_cat_link).url
        await self.bot.say(ran_cat)

    @commands.command()
    async def nickelback(self):
        songs = ('https://www.youtube.com/watch?v=BB0DU4DoPP4','https://www.youtube.com/watch?v=4OjiOn5s8s8','https://www.youtube.com/watch?v=_1hgVcNzvzY','https://www.youtube.com/watch?v=PvxVNGdwVwk','https://www.youtube.com/watch?v=JtxpcQaSR0k','https://www.youtube.com/watch?v=76RbWuFll0Y','https://www.youtube.com/watch?v=1cQh1ccqu8M','https://www.youtube.com/watch?v=wQzn4a5qHT4','https://www.youtube.com/watch?v=-qcZ9M-QoOc','https://www.youtube.com/watch?v=5RtTFP2TNcM','https://www.youtube.com/watch?v=GP7zpdwo3Xo','https://www.youtube.com/watch?v=FIjRo-gMlKE','https://www.youtube.com/watch?v=vt-UtzP1u1g');
        rand_song = random.choice(songs)
        await self.bot.say(rand_song)

    @commands.command()
    async def harambe(self):
        harambe_pics = ('Harambe.jpg','Harambe2.jpg','Harambe3.jpg','Harambe4.jpg','Harambe5.jpg','Harambe6.jpg','Harambe7.jpg','Harambe8.jpg')
        await self.bot.say('/home/pi/thombot/pictures/harambe/' + random.choice(harambe_pics))

    @commands.command()
    async def aliens(self):
        await self.bot.say('/home/pi/thombot/pictures/aliens.png')

    @commands.command()
    async def slab(self):
        await self.bot.say('RETURN THE SLAAAAB')

    @commands.command()
    async def dva(self:
        await self.bot.say('/home/pi/thombot/pictures/dva.png')

    @commands.command()
    async def mission_statement(self):
        await self.bot.say('/home/pi/thombot/pictures/thom_stargazer.jpg')

    @commands.command()
    async def goo(self):
        await self.bot.say('/home/pi/thombot/pictures/goo.jpg')

def setup(bot):
    bot.add_cog(image_commands(bot))
