from .saveDataHandler import (in_voice_channels,
                             save_voice_channel,
                             delete_voice_channel)
from disco.bot import Bot, Plugin
from disco.bot.command import CommandError
from disco.voice.player import Player
from disco.voice.playable import (YoutubeDLInput,
                                  BufferedOpusEncoderPlayable,
                                  OpusFilePlayable)
from disco.voice.client import VoiceException


'''
very broken, does some funky stuff, needs some work for sure.
used kill while connected ot voice channel and now the bot wont rejoin any channels, it thinks it's alreayd playing something.
have yet to try actually playing music.
find reason for kill being funky and for leave also being weird.
-------------------------------------------------------------------
added the del guilds command into the leave and kill command themselves instead of in the join one. Not sure if it will work ok that way
should be able to, but I don't know if I need the wait command for it to work properly

blep got an error with an opus object, either it didn't find the file correctly, or it isn't reading it right, it's hard to tell
probably not reading it right sinc eit gave me an object error, but the bot was having some trouble reading files from that location with the pictures
it also did not leave the voice channel even though it got an error, probably need to amke sure the and add some try except clauses to make sure things get done
'''

class MusicPlugin(Plugin):
    def load(self, ctx):
        super(MusicPlugin, self).load(ctx)
        self.guilds = {}

    @Plugin.command('join')
    def on_join(self, event):
        if in_voice_channels(event.guild.id, event.msg.channel) is False:
            return event.msg.reply('Can\'t do voice commands here!')
        if event.guild.id in self.guilds:
            return event.msg.reply("I'm already playing something")

        state = event.guild.get_member(event.author).get_voice_state()
        if not state:
            return event.msg.reply("You must be in a voice channel to do that")

        try:
            client = state.channel.connect()
        except VoiceException as e:
            return event.msg.reply(f"failed to connect to voice: {e}")

        self.guilds[event.guild.id] = Player(client)
        #self.guilds[event.guild.id].complete.wait()
        #del self.guilds[event.guild.id]

    def get_player(self, guild_id):
        if guild_id not in self.guilds:
            raise CommandError("I'm not currently playing any music here!")
        return self.guilds.get(guild_id)

    @Plugin.command('leave')
    def on_leave(self, event):
        if in_voice_channels(event.guild.id, event.msg.channel) is False:
            return event.msg.reply('Can\'t do voice commands here!')
        player = self.get_player(event.guild.id)
        player.disconnect()
        del self.guilds[event.guild.id]

    @Plugin.command('play', '<url:str>')
    def on_play(self, event, url):
        if in_voice_channels(event.guild.id, event.msg.channel) is False:
            return event.msg.reply('Can\'t do voice commands here!')
        item = YoutubeDLInput(url).pipe(BufferedOpusEncoderPlayable)
        self.get_player(event.guild.id).queue.append(item)

    @Plugin.command('pause')
    def on_pause(self, event):
        if in_voice_channels(event.guild.id, event.msg.channel) is False:
            return event.msg.reply('Can\'t do voice commands here!')
        self.get_player(event.guild.id).pause()

    @Plugin.command('resume')
    def on_resume(self, event):
        if in_voice_channels(event.guild.id, event.msg.channel) is False:
            return event.msg.reply('Can\'t do voice commands here!')
        self.get_player(event.guild.id).resume()

    @Plugin.command('kill')
    def on_kill(self, event):
        if in_voice_channels(event.guild.id, event.msg.channel) is False:
            return event.msg.reply('Can\'t do voice commands here!')
        self.get_player(event.guild.id).client.ws.sock.shutdown()
        del self.guilds[event.guild.id]

    '''
    could be dangerous depending on what the state of the voice client is in, need to do some more thinking and looking to make sure it's safe to use
    '''
    @Plugin.command('blep')
    def on_blep(self, event):
        if in_voice_channels(event.guild.id, event.msg.channel) is False:
            return event.msg.reply('Can\'t do voice commands here!')
        if event.guild.id in self.guilds:
            return event.msg.reply('I\'m busy, fuck off!')

        state = event.guild.get_member(event.author).get_voice_state()
        if not state:
            return event.msg.reply(
                f"You must be in a voice channel, you must suffer too {event.author}."
            )

        try:
            client = state.channel.connect()
        except VoiceException as e:
            return event.msg.reply(f"sorry, no dumb noises today: {e}")

        player = Player(client)
        item = OpusFilePlayable('../sounds/op.opus').pipe(BufferedOpusEncoderPlayable)
        player.play(item).complete.wait()
        player.disconnect()
        player.client.ws.sock.shutdown()
        return event.msg.reply("hope you enjoyed my beatiful noises!")

    @Plugin.command('addVoiceChannel')
    def on_addVoiceChannel(self, event):
        result = save_voice_channel(event.guild.id, event.message.channel)
        if result is True:
            return event.msg.reply('You have chosen. It can never be undone. (unless you use the deleteVoiceChannel command)')
        return event.msg.reply('Already a part of a channel! Use deleteVoiceChannel command to reset the channel')

    @Plugin.command('deleteVoiceChannel')
    def on_deleteVoiceChannel(self, event):
        result = delete_voice_channel(event.guild.id)
        if result is True:
            return event.msg.reply('Removed channel restrictions, you can be annoying anywhere now!')
        return event.msg.reply('There was no channel set for voice commands.')
