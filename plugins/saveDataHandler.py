import pandas as pd
import pickle
from pymongo import MongoClient


def load_voice_channels(guild_id, voice_id):
    pass

def delete_voice_channel(guild_id):
    pass

def save_voice_channel(guild_id, channel_id):
    #returns false if alreayd in database else returns true if added to database
    mc = MongoClient()
    thombot_db = mc['thombot']
    voice_channels_db = thombot_db['voice_channels']
    for guild_id_db in voice_channels_db.find():
        if guild_id in guild_id_db['guild_id']:
            return False
    voice_channels_db.db.insert_one({'guild_id': guild_id, 'channel_id': channel_id})
    mc.close()
    return True

