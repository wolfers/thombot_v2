from discord.ext import commands
import asyncio

class VoiceEntry:
    def __init__(self,message,player):
        self.requester = message.author
        self.channel = message.channel
        self.player = player

class VoiceState:
    def __init__(self,bot):
        self.current = None
        self.voice = None
        self.bot = bot
        self.play_next_song = asyncio.Event()
        self.songs = asyncio.Queue()
        self.audio_player = self.bot.loop.create_task(self.audio_player_task())

    def is_playing(self):
        if self.voice is None or self.current is None:
            return False

        player = self.current.player
        return not player.is_done()

    @property
    def player(self):
        return self.current.player

    def skip(self):
        if self.is_playing():
            self.player.stop()

    def toggle_next(self):
        self.bot.loop.call_soon_threadsafe(self.play_next_song.set)

    async def audio_player_task(self):
        while True:
            self.play_next_song.clear()
            self.self.current = await self.songs.get()
            await self.bot.send_message(self.current.channel, 'Now playing {0}'.format(str(self.current))
            self.current.player.start()
            await self.play_next_song.wait()

class Music:
    """
    Various voice commands
    """
