import pandas as pd
import pickle
from pymongo import MongoClient


def in_voice_channels(guild_id, voice_id):
    '''
    takes guild_id and voice_id as inputs

    If voice_id and guild_id both in database it returns True.
    (user using command in the correct channel)

    If guild_id is in database but voice_is is not it returns False.
    (channel set for users to do voice commands but user is in wrong channel)

    if guild_id is not in the database it returns None.
    (no channel set so user can use commands in any channel)
    '''
    mc = MongoClient()
    for guild_id_db in mc.voice_channels.guild_id.find():
        if guild_id in guild_id_db['guild_id']:
            if voice_id in guild_id_db['voice_id']:
                mc.close()
                return True
            mc.close()
            return False
    mc.close()
    return True


def delete_voice_channel(guild_id):
    '''
    removes a channel from the database
    commands can be executed from anywhere
    a new channel can be set
    '''
    mc = MongoClient()
    for guild_id_db in mc.voice_channels.guild_id.find():
        if guild_id in guild_id_db['guild_id']:
            mc.thombot.voice_channels.deleteOne({'guild_id': guild_id})
            mc.close()
            return True
    mc.close()
    return False

def save_voice_channel(guild_id, channel_id):
    '''
    if guild_id is in the database it returns False.
    (if there is alreayd a channel set for voice commands)

    if guild_id is not in the database it returns True.
    (there was no cahnnel set for voice commands and it is now set correctly)
    '''
    mc = MongoClient()
    thombot_db = mc['thombot']
    voice_channels_db = thombot_db['voice_channels']
    for guild_id_db in voice_channels_db.find():
        if guild_id in guild_id_db['guild_id']:
            mc.close()
            return False
    voice_channels_db.db.insert_one({'guild_id': guild_id, 'channel_id': channel_id})
    mc.close()
    return True

