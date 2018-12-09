'''
The Thom Stargazer 2019 Christmas event!

update this later

secret santa.
goals are to have people join via commands.
have them enter in some things they like.
at a certain date, give people their giftee. Store the list
send the santa their giftee
have the santa create something digital for thier giftee.
can be art, memes, soemthing silly, a video, a quick song, whatever they want.
They can submit it via the bot, they only get one submission
maybe have it so they can submit multiple things.
on a certain date, send the gifts to the giftee
mission complete
'''

import discord
from discord.ext import commands
from random import shuffle
from pony import orm
from pony.orm import db_session

santa_start = '''

'''
santa_info = '''

'''

with open("./db_info.txt", "r")as f:
    db_user = f.readline()[:-1]
    db_password = f.readline()[:-1]
    db_port = f.readline()[:-1]
    db_database = f.readline()[:-1]

db = orm.Database()
db.bind(provider='postgres', user=db_user, password=db_password, host="postgres", database=db_database, port=db_port)

class UserSanta2019(db.Entity):
    user_id = orm.Required(int, size=64)
    guild_id = orm.Required(int, size=64)
    guild_name = orm.Required(str)
    wishes = orm.Optional(str)

class GuildSanta2019(db.Entity):
    guild_id = orm.Required(int, size=64)
    status = orm.Required(str)

db.generate_mapping(create_tables=True)

def check_guild(guild):
    pass


def update_guild(guild):
    pass


def get_user(user):
    pass


def add_user(user):
    pass


def update_user(user):
    pass


class secretSanta2019:
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(hidden=True)
    @commands.guild_only()
    @commands.is_owner()
    async def santa_start(self, ctx):
        guild = ctx.guild.id
        status = check_guild(guild)
        if status == "active":
            await ctx.send("This guild is already a part of the event! No need to start it again!")
        else:
            update_guild(guild)
            await ctx.send(santa_start)
    
    @commands.command()
    @commands.guild_only()
    async def santa_join(self, ctx):
        '''
        add user to the list, take their input as their wishes.
        '''
    
    @commands.command()
    @commands.guild_only()
    async def santa_update(self, ctx):
        '''
        allows the user to update their wishes in the database. Will replace whatever was written previously
        '''

    @commands.command(hidden=True)
    @commands.guild_only()
    @commands.is_owner()
    async def santa_match(self, ctx):
        '''
        matches all the people with their secret santa for the guild
        will send out a dm to each person with the one they give a gift to
        add them all to a database with their matches, guilds, etc
        use guild names to keep track of what gift is for what server
        accept links or images as a gift. Must be either of those
        '''
    
    @commands.command(hidden=True)
    @commands.guild_only()
    @commands.is_owner()
    async def santa_end(self, ctx):
        '''
        closes the event for this server
        send all of the gifts via dm including the guild name
        '''
    
    @commands.command(hidden=True)
    @commands.is_owner()
    async def santa_cleanup(self, ctx):
        '''
        will clean up the tables
        gets rid of all saved files
        this is to be run after a bit, once everonye ahs had a chacne to get their gifts
        don't do it right away, just ot make sure everyone got theirs correctly
        '''


    