#main text commands for the bot

from disco.bot import Plugin

class TextPlugins(Plugin):
    @Plugin.command('ping')
    def on_ping(self, event):
        return event.msg.reply('pong!')