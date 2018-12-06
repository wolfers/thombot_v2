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
    From there, it's up to you. ;) Use "!vday_info" to get some more infomration sent to you in a dm.
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
with open("db_info.txt", "r")as f:
    db_user = f.readline()[:-2]
    db_password = f.readline()[:-2]
    db_host = f.readline()[:-2]
    db_database = f.readline()[:-2]


class User(db.Entity):
    user_id = orm.Required(str)
    user_guild = orm.Required(str)

class GuildStatus(db.Entity):
    guild_id = orm.Primary_Key(str)
    active = orm.Required(bool)


db = orm.Database()
db.bind(provider='postgres', user=db_user, password=db_password, host=db_host, database=db_database)
db.generate_mapping(create_tables=True)


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
    returns nothing
    '''
    User(user_id=user_id, user_guild=user_guild)


@orm.db_session
def get_users_by_guild(guild):
    return User.select(u.user_id for u in User if u.user_guid == guild)[:]


def get_matches(guild):
    '''
    Takes in the guild and returns matches for all users that
    registered in that guild
    '''
    users = get_users_by_guild(guild)
    matches = []
    if len(users) % 2 != 0:
        users.append("thombot")
    for _ in range(len(users)):
        shuffle(users)
        user1 = users.pop()
        shuffle(users)
        user2 = users.pop()
        matches.append(set(user1, user2))
    return matches


class ValentinesDay2019:
    def init(self, bot):
        self.bot = bot
        self.active = False

    @commands.command(pass_context=True)
    async def vday_setup(self, ctx):
        '''
        will start the vday submission process.
        will let people isgn up to recieve a valentine
        '''
        self.active = True
        await self.bot.say(vday_start)
    
    @commands.command(pass_context=True)
    async def vday_info(self, ctx):
        '''
        sends a dm to the users that sent this message explaining some things about
        the valentines day event
        '''
        #figure out how to actually send things to users in a dm when I get internet again
        pass

    @commands.command(pass_context=True)
    async def vday_join(self, ctx):
        '''
        adds the user to the database.
        '''
        #also need to figure out the exact way to get the guild so I can make it on a server basis.
        user = ctx.message.author
        guild = ctx.message.guild_id
        if check_user(user, guild) == True:
            self.bot.say("You've already joined!")
        else:
            store_user(user, guild)
            await self.bot.say("You've been added to the pool of valentines!")
    
    @commands.command(pass_context=True)
    async def vday_matches(self, ctx):
        '''
        gets all the users from the database
        matches all the users together
        if there is an odd number of users it includes thombot to even it out
        displays the matches to the discord channel
        '''
        guild = ctx.message.guild_id
        matches = get_matches(guild)
        self.bot.say("It's time to announce the winners and losers of the valentines day contest! The pairs will be below:")
        for m in matches:
            self.bot.say("<@{m[0]}> :heart: <@{m[1]}>")
        self.bot.say("Hope you had fun! Enjoy your valentines!")


def setup(bot):
    bot.add_cog(ValentinesDay2019(bot))
