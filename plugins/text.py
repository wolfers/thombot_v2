from disco.bot import Plugin
from PIL import ImageFont, Image, ImageDraw
from nltk.sentiment import vader

#set font for goo edit
font = ImageFont.truetype("comic-sans.ttf", 40)

#draws the message onto blankgoo.png and then saves the new image to gootext.png
def text_add(message):
    with Image.open('../img/blankgoo.png') as img:
        draw = ImageDraw.Draw(img)
        to_add = text_prep(message)
        draw.text((420,150), to_add, fill=(0,0,0,0), font=font)
        img.save('../img/gootext.png')
    
#preps the message to be added to the image using /n
def text_prep(message):
    for num, letter in enumerate(message):
        count = 0
        if letter != " ":
            count += 1
        elif count >= 3:
            message = message[:num] + "/n" + message[num + 1]
    return message


def sentiment_score(text):
    analyzer = vader.SentimentIntensityAnalyzer()
    score = analyzer.polarity_scores(text)
    return score


class TextPlugins(Plugin):
    @Plugin.command('ping')
    def on_ping(self, event):
        return event.msg.reply('pong!')

    @Plugin.command('ban')
    def on_ban(self, event):
        for user in event.msg.mentions:
            return event.msg.reply(f'you\'ve been banned, {user}!')

    @Plugin.command('gooedit')
    def on_gooedit(self, event):
        text_add(event.msg.content)
        return event.msg.reply(attachment='../img/gootext.png')
    
    @Plugin.command('score')
    def on_score(self, event):
        '''
        takes a message sent from a user and returns the score it got from the vader sentiment spectrum
        
        needs to be made more human readable and maybe parsed into other things.
        '''
        score = sentiment_score(event.msg.content)

        return event.msg.reply(f"The score for that message is {score['compound']} !!!")

