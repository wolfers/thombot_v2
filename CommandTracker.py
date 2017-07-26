# this module should add commands used to a shelve of users. If user or command isn't in the shelve, it will add it.
# can also return how many commands were used as a dictionary

import shelve


def add_entry(user, command):
    """increments number of command used by a specific user when called"""
    tracker = shelve.open('CommandTracker')
    if command in tracker[user]:
        tracker[user][command] += 1
    else:
        tracker[user][command] = 1
    tracker.close()


def used_commands(user):
    """returns dictionary of used commands, if user has not used any commands it will return None"""
    tracker = shelve.open('CommandTracker')
    if user in tracker:
        send_dict = tracker[user]
        tracker.close()
        return send_dict
    else:
        tracker.close()
        return None
