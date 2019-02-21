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
from collections import deque
from pony import o
from pony.orm import db_session, Required, PrimaryKey, Database, Optional, select

santa_start = '''

'''
santa_info = '''

'''

with open("./db_info.txt", "r")as f:
    db_user = f.readline()[:-1]
    db_password = f.readline()[:-1]
    db_port = f.readline()[:-1]
    db_database = f.readline()[:-1]

db = Database()
db.bind(provider='postgres', user=db_user, password=db_password, host="postgres", database=db_database, port=db_port)

class UserSanta2019(db.Entity):
    user_id = Required(int, size=64)
    guild_id = Required(int, size=64)
    PrimaryKey(user_id, guild_id)
    guild_name = Required(str)
    wishes = Required(str)
    giftee_id = Optional(int, size=64)
    submission_url = Optional(str)

class GuildSanta2019(db.Entity):
    guild_id = PrimaryKey(int, size=64)
    status = Required(str)

db.generate_mapping(create_tables=True)


@db_session
def get_guild_status(guild_id):
    '''
    returns the status of the guild

    paramters
    ----------
    guild_id: int
        discord guild id
    
    returns
    --------
    status: str
        can be active, matched, inactive, or missing
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
        discord guild id
    
    status: str
        default active
        status to update the guild to. Can be active, matched, or inactive
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
    """
    checks if the user exists

    paramters
    ----------
    user_id: int
        discord user id
    
    guild_id: int
        discord guild id

    returns
    ---------
    True if user exists, otherwise False
    """
    return UserSanta2019.exists(user_id=user_id, guild_id=guild_id)


@db_session
def get_user_submission(user_id, guild_id):
    if UserSanta2019.exists(user_id=user_id, guild_id=guild_id):
        return UserSanta2019.get(user_id=user_id, guild_id=guild_id).submission_url


@db_session
def add_user(user_id, guild_id, guild_name, wishes):
    """
    adds a user to the database

    paramters
    ----------
    user_id: int
        discord user id
    
    guild_id: int
        discord guild id
    
    guild_name: str
        str representation of the discord guild name
    
    wishes: str
        contains the user input for wishes
    """
    UserSanta2019(user_id=user_id, guild_id=guild_id, guild_name=guild_name, wishes=wishes)


@db_session
def update_user(user_id, guild_id, wishes=None, giftee_id=None):
    """
    updates the users wishes, overwritting their previous wishes

    parameters
    -----------
    user_id: int
        discord user id
    
    guild_id: int
        discord guild id
    
    wishes: str
        the wishes the user submitted
    """
    if giftee_id == None:
        UserSanta2019(user_id, guild_id).wishes = wishes
    elif wishes == None:
        UserSanta2019(user_id, guild_id).giftee_id = giftee_id

@db_session
def update_gift(user_id, guild_id, link):
    UserSanta2019(user_id=user_id, guild_id=guild_id).submission_url = link

@db_session
def get_users(guild_id):
    '''
    takes in a guild id and return the user ids for that guild

    parameters
    ----------
    guild_id: int
        discord guild id
    
    returns
    ---------
    user_list: list
        list of discord user ids
    '''
    query = select(u.user_id for u in UserSanta2019 if u.guild_id == guild_id)
    return list(query)


def make_matches(guild_id):
    '''
    creates the matches for all users in the database
    
    parameters
    ------------
    guild_id: int
        discord guild id
    '''
    users = get_users(guild_id)
    shuffle(users)
    users = deque(users)
    first = users[0]
    for _ in len(users):
        if len(users) == 1:
            update_user(first, guild_id, giftee_id=users[0])
        else:
            user_id = users.popleft()
            giftee_id = users[0]
            update_user(user_id, guild_id, giftee_id=giftee_id)

@db_session
def get_matches(guild_id):
    '''
    gets the matches for all users and returns them as a list of lists
    '''
    query = select([u.user_id, u.giftee_id] for u in UserSanta2019 if u.guild_id == guild_id)
    return list(query)


def check_guild(ctx):
    guild_id = ctx.guild.id
    guild_status = get_guild_status(guild_id)

    if guild_status in ["inactive", "missing"]:
        return "The event is not active on this server"
    elif guild_status == "matched":
        return "This server has already gotten their matches"
    else:
        return "active"

class Santa:
    def __init__(self, bot):
        self.bot = bot
    
    @commands.group()
    @commands.guild_only()
    async def santa(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send("invalid santa command! Use '!help santa' to see the commands you can use")
    
    @santa.command(hidden=True)
    @commands.guild_only()
    @commands.is_owner()
    async def start(self, ctx):
        '''
        Adds the guild to the database and sets to active.
        sends the starting message to the guild channel
        '''
        guild = ctx.guild.id
        status = get_guild_status(guild)
        if status in ["active", "matched"]:
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

        guild_status = get_guild_status(guild_id)
        if guild_status == "matched":
            return await ctx.send("This guild has already matched users! It's too late to join, sorry!")
        elif guild_status in ["inactive", "missing"]:
            return await ctx.send("The event is currently not running in this guild!")
        elif check_user(user_id, guild_id):
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
        guild_name = ctx.guild.name

        guild_status = get_guild_status(guild_id)
        if guild_status == 'matched':
            return await ctx.send("This guild has already matched people! It's too late to update your wishes, sorry.")
        elif guild_status in ["inactive", "missing"]:
            return await ctx.send("This event isn't currently active in this guild!")

        if not check_user(user_id, guild_id):
            add_user(user_id, guild_id, guild_name, wishes)
            return await ctx.send("You weren't entered for the event! I entered you and added your wishes.")

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
        guild_id = ctx.guild.id
        guild_name = ctx.guild.name
        guild_status = check_guild(guild_id)

        if guild_status in ["inactive", "missing"]:
            return await ctx.send("The event is not active on this server")
        elif guild_status == "matched":
            return await ctx.send("This server has already gotten their matches")

        make_matches(guild_id)
        matches = get_matches(guild_id)
        for match in matches:
            #match[0] is the secret santa, match[1] is the one who will recieve a gift
            await ctx.send_message(match[0], message="You will be giving a gift to: " + match[1])
            

        return await ctx.send("All matches have been made and sent!"
                              "if you signed up and did not recieve a match, please notify trevor and he'll look into it")

    @santa.command()
    async def submit(self, ctx, *, link):
        '''
        lets the user DM the bot in order to submit their gift
        takes in a link and saves it in the database.
        will overwrite previous gift if used again
        '''
        guild_check = check_guild(ctx)
        if guild_check != "active":
            return await ctx.send(guild_check)
        if ctx.message.server != None:
            return await ctx.send("This command only works in DMs, please DM to use it!")
        update_gift(ctx.author.id, ctx.guild.id, link)
        return await ctx.send("Your submission has been saved! If you want to view what you've submitted you can use '!santa submission'. If you want to change or update your gift, use this command again to rewrite.")
    
    @santa.command()
    async def submission(self, ctx):
        '''
        shows the user what they have already submitted
        '''
        guild_check = check_guild(ctx)
        if guild_check != "active":
            return await ctx.send(guild_check)
        if ctx.message.server != None:
            return await ctx.send("This command only works in DMs, please DM to use it!")
        submission = get_user_submission(ctx.author.id, ctx.guild.id)
        if submission == None:
            return await ctx.send("It appears that you haven't submitted anything yet, please use the submit command to submit a gift")
        return await ctx.send("The gift you ahve submitted: " + submission)

    @santa.command()
    @commands.guild_only()
    async def check_wish(self, ctx):
        '''
        shows the user what their wish is
        '''
        #check if guild is active
        #check if user has wished
        #if not, tell them
        #send their wish as a message to the server
    
    @santa.command()
    async def more_info(self, ctx):
        '''
        sends more info the the channel or to a dm
        '''
        #check if guild is active
        #check if channel or dm
        #send message to channel or to dm

    @santa.command(hidden=True)
    @commands.guild_only()
    @commands.is_owner()
    async def end(self, ctx):
        '''
        closes the event for this server
        send all of the gifts via dm including the guild name
        call out anyone who signed up but didn't send a gift for someone
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


    