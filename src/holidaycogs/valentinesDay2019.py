'''
The thom stargazer 2019 valentines day event!
One the event starts, users can submit themselves to be in a pool for valentines
when the match command is used, it will match all users together for the server that the command is used in.
matches are per server, a user can be matched in multiple servers.
'''

import discord
from discord.ext import commands
from random import shuffle
from pony import orm
from pony.orm import db_session



vday_start = ''' 
    Hello @everyone! Welcome to the 2019 Thom Stargazer valentines day event! Type "!vday_join" to have your name entered
    entered into the pool of eligable valentines. The day before valentines day, your match will be posted.
    From there, it's up to you. ;) If you have any questions dm <@88838960175910912>
'''

vday_info = '''
    Hey! This is a more detailed explination of the valalentines day event! Matches are selected on a per server basis.
    This means that you can get another valentine of another server if you're into that. 
    You will be randomly matched with another person in the server. It's completly random.
    If there is an odd number of users, I'll put myself into the pool to even things out.
    Don't be dissapointed if I'm your valentine!
    If you're participating, I hope you enjoy!
    Thanks!
    -Thombot
'''

#either use csv for a text file or something to make this easy. just need to get the info
with open("./db_info.txt", "r")as f:
    db_user = f.readline()[:-1]
    db_password = f.readline()[:-1]
    db_port = f.readline()[:-1]
    db_database = f.readline()[:-1]

db = orm.Database()
db.bind(provider='postgres', user=db_user, password=db_password, host="postgres", database=db_database, port=db_port)

class User_vday2019(db.Entity):
    user_id = orm.Required(int, size=64)
    user_guild = orm.Required(int, size=64)

class Guild_vday2019(db.Entity):
    guild = orm.PrimaryKey(int, size=64)
    status = orm.Required(str)

db.generate_mapping(create_tables=True)


@db_session
def check_guild(guild):
    '''
    checks and returns the status of the guild as a str
    if it is active it returns active
    if it is not active it returns ended
    if it is not found in the database it returns missing
    '''
    if Guild_vday2019.exists(guild=guild):
        return Guild_vday2019.get(guild=guild).status
    else:
        return "missing"


@db_session
def update_guild(guild, status="active"):
    '''
    updates the guilds status in the database.
    can be either active or ended
    '''
    statuses = ["active", "ended"]
    if status not in statuses:
        print("did not udate, invalid status")
        return None
    if Guild_vday2019.exists(guild=guild):
        Guild_vday2019.status = status
    else:
        Guild_vday2019(guild=guild, status=status)


@db_session
def check_user(user_id, user_guild):
    '''
    checks the user and guild against the database
    returns True if the user exists and False if they do not
    '''
    return User_vday2019.exists(user_id=user_id, user_guild=user_guild)


@db_session
def store_user(user_id, user_guild):
    '''
    Stores the user in the database using their user id and the guild id.
    '''
    User_vday2019(user_id=user_id, user_guild=user_guild)


@db_session
def get_users_by_guild(guild):
    '''
    get a list of all the user ids for the guild
    '''
    return orm.select(u.user_id for u in User_vday2019 if u.user_guild == guild)[:]


def get_matches(guild):
    '''
    Takes in the guild and returns matches for all users that
    registered in that guild
    '''
    users = list(get_users_by_guild(guild))
    matches = []
    if len(users) % 2 != 0:
        users.append("240932500728315904")
    for _ in range(len(users)//2):
        shuffle(users)
        user1 = users.pop()
        shuffle(users)
        user2 = users.pop()
        matches.append([user1, user2])
    return matches


class valentinesDay2019:
    def __init__(self, bot):
        self.bot = bot

    @commands.command(alias=['vday_start'], hidden=True)
    @commands.guild_only()
    @commands.is_owner()
    async def vday_start(self, ctx):
        '''
        will start the vday submission process.
        will let people isgn up to recieve a valentine
        '''
        guild = ctx.guild.id
        status = check_guild(guild)
        if status == "active":
            await ctx.send("This guild is already part of the event! no need to start it again!")
        else:
            update_guild(guild)
            await ctx.send(vday_start)

    @commands.command()
    @commands.guild_only()
    async def vday_join(self, ctx):
        '''
        adds the user to the database.
        '''
        user = ctx.author.id
        guild = ctx.guild.id
        status = check_guild(guild)
        if status == "ended":
            await ctx.send("This server event has already ended!")
        elif status == "missing":
            await ctx.send("This event hasn't started yet! There will be an announcment when it has!")
        else:
            if check_user(user, guild) == True:
                await ctx.send("You've already joined!")
            else:
                store_user(user, guild)
                await ctx.send("You've been added to the pool of valentines!")
    
    @commands.command(hidden=True)
    @commands.guild_only()
    @commands.is_owner()
    async def vday_matches(self, ctx):
        '''
        gets all the users from the database
        matches all the users together
        if there is an odd number of users it includes thombot to even it out
        displays the matches to the discord channel
        '''
        guild = ctx.guild.id
        matches = get_matches(guild)
        if check_guild(guild) == "active":
            await ctx.send("It's time to announce the winners and losers of the valentines day contest! The pairs will be below:")
            for m in matches:
                await ctx.send("<@{}> :heart: <@{}>".format(m[0], m[1]))
            await ctx.send("Hope you had fun! Enjoy your valentines!")
            update_guild(guild, status="ended")
        else:
            await ctx.send("This server isn't currently active in the event.")

def setup(bot):
    bot.add_cog(valentinesDay2019(bot))
