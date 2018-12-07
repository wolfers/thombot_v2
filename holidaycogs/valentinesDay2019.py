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
    db_host = f.readline()[:-1]
    db_database = f.readline()[:-1]

db = orm.Database()
db.bind(provider='postgres', user=db_user, password=db_password, host=db_host, database=db_database)

class User(db.Entity):
    user_id = orm.Required(int)
    user_guild = orm.Required(int)

class GuildStatus(db.Entity):
    guild = orm.Primary_Key(int)
    status = orm.Required(str)

db.generate_mapping(create_tables=True)


@orm.db_session
def check_guild(guild):
    '''
    checks and returns the status of the guild as a str
    if it is active it returns active
    if it is not active it returns ended
    if it is not found in the database it returns missing
    '''
    if GuildStatus.exists(guild=guild):
        return GuildStatus.get(guild=guild).status
    else:
        return "missing"


@orm.db_sesion
def update_guild(guild, status="active"):
    '''
    updates the guilds status in the database.
    can be either active or ended
    '''
    statuses = ["active", "ended"]
    if status not in statuses:
        print("did not udate, invalid status")
        return None
    if GuildStatus.exists(guild=guild):
        GuildStatus.status = status
    else:
        GuildStatus(guild=guild, status=status)


@orm.db_session
def check_user(user_id, user_guild):
    '''
    checks the user and guild against the database
    returns True if the user exists and False if they do not
    '''
    return User.exists(user_id=user_id, user_guild=user_guild)


@orm.db_session
def store_user(user_id, user_guild):
    '''
    Stores the user in the database using their user id and the guild id.
    '''
    User(user_id=user_id, user_guild=user_guild)


@orm.db_session
def get_users_by_guild(guild):
    '''
    get a list of all the user ids for the guild
    '''
    return User.select(u.user_id for u in User if u.user_guid == guild)[:]


def get_matches(guild):
    '''
    Takes in the guild and returns matches for all users that
    registered in that guild
    '''
    users = get_users_by_guild(guild)
    matches = []
    if len(users) % 2 != 0:
        users.append("240932500728315904")
    for _ in range(len(users)/2):
        shuffle(users)
        user1 = users.pop()
        shuffle(users)
        user2 = users.pop()
        matches.append(set(user1, user2))
    return matches


class valentinesDay2019:
    def __init__(self, bot):
        self.bot = bot

    @commands.command(hidden=True)
    @commands.guild()
    @commands.is_owner()
    async def vday_setup(self, ctx):
        '''
        will start the vday submission process.
        will let people isgn up to recieve a valentine
        '''
        guild = ctx.guild.id
        status = check_guild(guild)
        if status == "active":
            self.ctx.send("This guild is already part of the event! no need to start it again!")
        else:
            update_guild(guild)
        await self.ctx.send(vday_start)

    @commands.command()
    @commands.guild()
    async def vday_join(self, ctx):
        '''
        adds the user to the database.
        '''
        user = ctx.author.id
        guild = ctx.guild.id
        status = check_guild(guild)
        if status == "ended":
            self.ctx.send("This server event has already ended!")
        elif status == "missing":
            self.ctx.send("This event hasn't started yet! There will be an announcment when it has!")
        else:
            if check_user(user, guild) == True:
                self.ctx.send("You've already joined!")
            else:
                store_user(user, guild)
                await self.ctx.send("You've been added to the pool of valentines!")
    
    @commands.command(hidden=True)
    @commands.guild()
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
            self.ctx.send("It's time to announce the winners and losers of the valentines day contest! The pairs will be below:")
            for m in matches:
                self.ctx.send("<@{m[0]}> :heart: <@{m[1]}>")
            self.ctx.send("Hope you had fun! Enjoy your valentines!")
        else:
            self.ctx.send("This server isn't currently active in the event.")

def setup(bot):
    bot.add_cog(valentinesDay2019(bot))