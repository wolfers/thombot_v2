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


@db_session
def check_guild(guild_id):
    '''
    returns the status of the guild

    paramters
    ----------
    guild_id: int
        the id of the guild to check
    
    returns
    --------
    status: str
        can either be active, inactive, or missing
    '''
    if GuildSanta2019.exists(guild_id=guild_id):
        return GuildSanta2019.get(guild_id=guild_id).status
    else:
        return "missing"


@db_session
def update_guild(guild_id, status="active"):
    '''
    updates the status of the guild
    will add the guild if it does not already exist.

    parameters
    -----------
    guild_id: int
        id of the guild to update
    
    status: str
        default active
        status to update the guild to. Can be active or inactive
    '''
    statuses = ['active', 'inactive']
    if status not in statuses:
        return print("did not update, invalid status")
    if GuildSanta2019.exists(guild_id=guild_id):
        GuildSanta2019.status = status
    else:
        GuildSanta2019(guild_id=guild_id, status=status)


@db_session
def check_user(user_id, guild_id):
    pass


@db_session
def get_user(user):
    pass


@db_session
def add_user(user):
    pass


@db_session
def update_user(user):
    pass


class Santa:
    def __init__(self, bot):
        self.bot = bot
    
    @commands.group()
    @commands.guild_only()
    async def santa(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send("invalid santa command! Use !help Santa to see the commands you can use")
    
    @santa.command(hidden=True)
    @commands.guild_only()
    @commands.is_owner()
    async def start(self, ctx):
        '''
        Adds the guild to the database and sets to active.
        sends the starting message to the guild channel
        '''
        guild = ctx.guild.id
        status = check_guild(guild)
        if status == "active":
            await ctx.send("This guild is already a part of the event! No need to start it again!")
        else:
            update_guild(guild)
            await ctx.send(santa_start)
    
    @santa.command()
    @commands.guild_only()
    async def join(self, ctx, *, wishes):
        '''
        add user to the list, take their input as their wishes.
        '''
        user_id = ctx.author.id
        guild_id = ctx.guild.id
        guild_name = ctx.guild.name

        if check_user(user_id, guild_id):
            return await ctx.send("You've already joined the secret santa!"
                           "If you would like to change your wishes you can use the update subcommand!")
        add_user(user_id, guild_id, guild_name, wishes)
        return await ctx.send("You have been enetered into the secret santa!"
                              "Keep an eye on your DMs for who you'll be giving a gift to!"
                              "Be sure to use the update subcommand if you ever want to update your wishes before santas are chosen.")
    
    @santa.command()
    @commands.guild_only()
    async def update(self, ctx, *, wishes):
        '''
        allows the user to update their wishes in the database. Will replace whatever was written previously
        '''
        user_id = ctx.author.id
        guild_id = ctx.guild.id

        update_user(user_id, guild_id, wishes)
        return await ctx.send("Your wishes have been updated!")

    @santa.command(hidden=True)
    @commands.guild_only()
    @commands.is_owner()
    async def match(self, ctx):
        '''
        matches all the people with their secret santa for the guild
        will send out a dm to each person with the one they give a gift to
        add them all to a database with their matches, guilds, etc
        use guild names to keep track of what gift is for what server
        accept links or images as a gift. Must be either of those
        '''
    
    @santa.command(hidden=True)
    @commands.guild_only()
    @commands.is_owner()
    async def end(self, ctx):
        '''
        closes the event for this server
        send all of the gifts via dm including the guild name
        '''
    
    @santa.command(hidden=True)
    @commands.is_owner()
    async def cleanup(self, ctx):
        '''
        will clean up the tables
        gets rid of all saved files
        this is to be run after a bit, once everonye ahs had a chacne to get their gifts
        don't do it right away, just ot make sure everyone got theirs correctly
        unsure if I will do all of this
        '''


    