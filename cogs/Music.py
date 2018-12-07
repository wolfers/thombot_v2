"""
created using https://gist.github.com/EvieePy/ab667b74e9758433b3eb806c53a19f34
"""

import discord
from discord.ext import commands

import asyncio
import itertools
import sys
import traceback
from async_timeout import timeout
from functools import partial
from youtube_dl import YoutubeDL

ytdlopts = {
    'format': 'bestaudio/best',
    'outtmpl': 'downloads/%(extractor )s-%(id)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'ignoreerrors': False,
    'logto stderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0'
}

ffmpegopts = {
    'before_options': '-nostdin',
    'options': '-vn'
}

ytdl = YoutubeDL(ytdlopts)

class VoiceConnectionError(commands.CommandError):
    '''Custom exception class for connection errors'''

class InvalidVoiceChannel(VoiceConnectionError):
    ''' Custom exception class for connection errors'''

class YTDLSource(discord.PCMVolumeTransformer):

    def __init__(self, source, *, data, requester):
        super().__init__(source)
        self.requester = requester

        self.title = data.get('title')
        self.web_url = data.get('webpage_url')

    def __getitem__(self, item: str):
        """allows accessing attributes similar to a dict"""
        return self.__getattribute__(item)
    
    @classmethod
    async def create_source(cls, ctx, search: str, *, loop, download=False):
        loop = loop or asyncio.get_event_loop()

        to_run = partial(ytdl.extract_info, url=search, download=download)
        data = await loop.run_in_executor(None, to_run)

        if 'entries' in data:
            # take the first item from a playlist
            data = data['entries'][0]
        
        await ctx.send(f'```ini\n[Added {data["title"]} to the Queue.]\n```', delete_after=15)

        if download:
            source = ytdl.prepare_filename(data)
        else:
            return {'webpage_url': data['webpage_url'], 'requester': ctx.author, 'title': data['title']}
    
    @classmethod
    async def regather_stream(cls, data, *, loop):
        """used for preparing a stream instead of downloading"""

        loop = loop or asyncio.get_event_loop()
        requester = data['requester']

        to_run = partial(ytdl.extract_info, url=data['webpage_url'], download=False)
        data = await loop.run_in_executor(None, to_run)

        return cls(discord.FFmpegPCMAudio(data['url']), data=data, requester=requester)


class MusicPlayer:
    """class assigned to each guild for Music
    implements a queue and a loop
    instance is destroyed upon disconnection from voice
    """

    __slots__ = ('bot', '_guild', '_channel', '_cog', 'queue', 'next', 'current', 'np', 'volume')

    def __init__(self, ctx):
        self.bot = ctx.bot
        self._guild = ctx.guild
        self._channel = ctx.channel
        self._cog = ctx.cog

        self.queue = asyncio.Queue()
        self.next = asyncio.Event()

        self.np = None
        self.volume = .5
        self.current = None

        ctx.bot.loop.create_task(self.player_loop())

    async def player_loop(self):
        await self.bot.wait_until_ready()

        while not self.bot.is_closed():
            self.next.clear()

            try:
                #wait for next song, if it times out, cancel the player and disconnect
                async with timeout(300):
                    source = await self.queue.get()
            except asyncio.TimeoutError:
                return self.destroy(self.guild)
            
            if not isinstance(source, YTDLSource):
                try:
                    source = await YTDLSource.regather_stream(source, loop=self.bot.loop)
                except Exception as e:
                    await self._channel.send(f'There was an error processing your song. \n'
                                             f'```css\n[{e}]\n```')
                    continue
            
            source.volume = self.volume
            self.current = source

            self._guild.voice_client.play(source, after=lambda _: self.bot.loop.call_soon_threadsafe(self.next.set))
            self.np = await self._channel.send(f'**Now playing:** `{source.title}` requested by '
                                               f'`{source.requester}`')
            
            await self.next.wait()

            source.cleanup()
            self.current = None

            try:
                await self.np.delete()
            except discord.HTTPException:
                pass
            
    def destroy(self, guild):
        return self.bot.loop.create_task(self._cog.cleanup(guild))

class Music:
    """music related commands"""

    __slots__ = ('bot', 'players')

    def __init__(self, bot):
        self.bot = bot
        self.players = {}

    async def cleanup(self, guild):
        try:
            await guild.voice_client.disconnect()
        except AttributeError:
            pass

        try:
            del self.players[guild.id]
        except KeyError:
            pass

    async def __local_check(self, ctx):
        """ local check for commands in this cog"""
        if not ctx.guild:
            raise commands.NoPrivateMessage
        return True
    
    async def __error(self, ctx, error):
        """ error hadnler for error sin this cog"""
        if isinstance(error, commands.NoPrivateMessage):
            try:
                return await ctx.send('This command cannot be used in a Private Message')
            except discord.HTTPException:
                pass
        elif isinstance(error, InvalidVoiceChannel):
            await ctx.send('Error connecting to voice channel. '
                           'Please make sure you are in a valid channel or provide me with one')

        print('Ignoring exception in command {}'.format(ctx.command), file=sys.stderr)
        traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)
    
    def get_player(self, ctx):
        """retrieve the guild player, or generate one"""
        try:
            player = self.players[ctx.guild.id]
        except KeyError:
            player = MusicPlayer(ctx)
            self.players[ctx.guild.id] = player
        
        return player
    
    @commands.command(name='connect', aliases=['join'])
    async def connect_(self, ctx, *, channel: discord.VoiceChannel=None):
        """Connect to voice

        Parameters
        ------------
        channel: discord.VoiceChannel [Optional]
            The channel to connect to. If a channel is not specified, an attempt
            to join will be made.
        
        This command also ahdnles moving the bot to different channels
        """
        if not channel:
            try:
                channel = ctx.author.voice.channel
            except AttributeError:
                raise InvalidVoiceChannel('No channel to join. Please either specify a valid channel or join one.')
            
        vc = ctx.voice_client

        if vc:
            if vc.channel_id == channel.id:
                return
            try:
                await vc.move_to(channel)
            except asyncio.TimeoutError:
                raise VoiceConnectionError(f'Moving to channel: <{channel}> timed out.')
        else:
            try:
                await channel.connect()
            except asyncio.TimeoutError:
                raise VoiceConnectionError(f'Connecting to channel: <{channel}> timed out.')
        
        await ctx.send(f'Connected to: **{channel}**', delete_after=20)
    
    @commands.command(name='play', aliases=['sing'])
    async def play_(self, ctx, *, search: str):
        """Request a song and add it to the queue

        This command attempts to join a valid voice channel if the bot is not already in one
        uses YTDL to automatically search and retrieve a song

        Parameters
        -----------
        search: str [required]
            The song to search and retrieve using YTDL. This could be a simple search, an ID or URL.
        """
        await ctx.trigger_typing()

        vc = ctx.voice_client

        if not vc:
            await ctx.invoke(self.connect_)
        
        player = self.get_player(ctx)

        source = await YTDLSource.create_source(ctx, search, loop=self.bot.loop, download=False)

        await player.queue.put(source)
    
    @commands.command(name='pause')
    async def pause_(self, ctx):
        """Pauses the currently playing song"""
        vc = ctx.voice_client

        if not vc or not vc.is_playing():
            return await ctx.send('I am not currently playing anything!', delete_after=20)
        elif vc.is_paused():
            return
        
        vc.pause()
        await ctx.send(f'**`{ctx.author}`**: Paused the song!')

    @commands.command(name='resume')
    async def resume_(self, ctx):
        """resume the currently playing song"""
        vc = ctx.voice_client

        if not vc or not vc.is_connected():
            return await ctx.send('I am not currently playing anything!', delete_after=20)
        elif not vc.is_paused():
            return
        
        vc.resume()
        await ctx.send(f'`**{ctx.author}**`: Resumed the song!')

    @commands.command(name='skip')
    async def skip_(self, ctx):
        """SKip the song"""
        vc = ctx.voice_client

        if not vc or not vc.is_connected():
            return await ctx.send('I am not currently playing anything!', delete_after=20)
        
        if vc.is_paused():
            pass
        elif not vc.is_playing():
            return
        
        vc.stop()
        await ctx.send(f'**`{ctx.author}`**: Skipped the song!')

    @commands.command(name='queue', aliases=['q', 'playlist'])
    async def queue_info(self, ctx):
        """Retrieve a basic queue of upcoming songs"""
        vc = ctx.voice_client

        if not vc or not vc.is_connected():
            return await ctx.send('I am not currently connected to voice!', delete_after=20)
        
        player = self.get_player(ctx)
        if player.queue.empty():
            return await ctx.send('There are currently no more queued songs.')
        
        #grab up to 5 entries from the queue
        upcoming = list(itertools.islice(player.queue._queue, 0, 5))

        fmt = '\n'.join(f'**`{_["title"]}`**' for _ in upcoming)
        embed = discord.Embed(title=f'Upcoming - Next {len(upcoming)}', description=fmt)

        await ctx.send(embed=embed)
    
    @commands.command(name='now_playing', aliases=['np', 'current', 'currentsong', 'playing'])
    async def now_playing_(self, ctx):
        """Display information about the currently playing song"""
        vc = ctx.voice_client

        if not vc or not vc.is_connected():
            return await ctx.send('I am not currently connected to voice!', delete_after=20)
        
        player = self.get_player(ctx)
        if not player.current:
            return await ctx.send('I am not currently palying anything!', delete_after=20)
        
        try:
            await player.np.delete()
        except discord.HTTPException:
            pass
        
        player.np = await ctx.send(f'**Now Playing:** `{vc.source.title}` '
                                   f'requested by `{vc.source.requester}`')
    
    @commands.command(name='volume', aliases=['vol'])
    async def change_volume(self, ctx, *, vol: float):
        """Change the player volume

        Parameters
        -----------
        volume: float or int [Required]
            The volume to set the player to in percentage. This must be between 1 and 100.
        """
        vc = ctx.voice_client
        
        if not vc or not vc.is_connected():
            return await ctx.send('I am not currently connected to voice!', delete_after=20)
        
        if not 0 < vol < 101:
            return await ctx.send('please enter a value between 1 and 100')
        
        player = self.get_player(ctx)

        if vc.source:
            vc.source.volume = vol / 100
        
        player.volume = vol / 100
        await ctx.send(f'**`{ctx.author}`**: Set the volume to **{vol}%**')
    
    @commands.command(name='stop')
    async def stop_(self, ctx):
        """Stop the currently playing song and destroy the player

        !Warning!
            This will destroy the player assigned to your guild, also deleting any queued songs
        """
        vc = ctx.voice_client

        if not vc or not vc.is_connected():
            return await ctx.send('I am not currently playing anything!', delete_after=20)
        
        await self.cleanup(ctx.guild)


def setup(bot):
    bot.add_cog(Music(bot))
