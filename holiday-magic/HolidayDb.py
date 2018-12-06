'''
This file contains all of the database fucntions for the holiday commands for now
They are just placeholders at the moment. They will be filled in as I finish the hpoliday commands
'''

from random import shuffle
from pony import orm


def check_user(user, guild):
    '''
    checks the user and guild against the database
    returns True if the user exists and False if they do not
    '''
    #check database for user here
    user = None
    if user == None:
        return False
    else:
        return True


def store_user(user, guild):
    '''
    Stores the user in the database using their user id and the guild id.
    returns nothing
    '''
    pass


def get_matches(guild):
    '''
    gets off the users for the guild and randomly matches them together
    if the users are an odd number, it adds thombot to the user list.
    returns a list of sets that contain user objects
    '''
    #get the matches
    users = []
    matches = []
    if len(users) % 2 != 0:
        users.append("thombot")
    #mathc all users together. 
    #random choice without selecting the same users
    #select one, remove it form the list, select another, remove, add them to a set, add that set to a list, return that list
    for _ in range(len(users)):
        shuffle(users)
        user1 = users.pop()
        shuffle(users)
        user2 = users.pop()
        matches.append(set(user1, user2))
    return matches
