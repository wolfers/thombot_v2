from disco.bot import Plugin
from PIL import ImageFont, Image, ImageDraw
from nltk.sentiment import vader
import os
import requests
import random

#set font for goo edit
font = ImageFont.truetype("comic-sans.ttf", 40)

'''
getting a too many values to unpack (expected 4) error, no idea how to fix it.
looks like a problem in requests module so not sure waht to do there
'''
#draws the message onto blankgoo.png and then saves the new image to gootext.png
def text_add(message):
    with Image.open(os.path.join('pictures/blankgoo.png')) as img:
        draw = ImageDraw.Draw(img)
        to_add = text_prep(message)
        draw.text((420,150), to_add, fill=(0,0,0,0), font=font)
        img.save(os.path.join('pictures/gootext.png'))
    
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
        return event.msg.reply(attachment=os.path.join('pictures/gootext.png'))
    
    @Plugin.command('score')
    def on_score(self, event):
        '''
        takes a message sent from a user and returns the score it got from the vader sentiment spectrum
        
        needs to be made more human readable and maybe parsed into other things.
        '''
        score = sentiment_score(event.msg.content)

        return event.msg.reply(f"The score for that message is {score['compound']} !!!")

    @Plugin.command('cat')
    def on_cat(self, event):
        ran_cat_link = random.choice(['http://thecatapi.com/api/images/get', 'http://random.cat/meow'])
        if ran_cat_link == 'http://random.cat/meow':
            ran_cat = requests.get(ran_cat_link).json()["file"]
        else:
            ran_cat = requests.get(ran_cat_link).url
        return event.msg.reply(ran_cat)

    @Plugin.command('mission')
    def on_mission(self, event):
        return event.msg.reply(attachment=os.path.join('pictures/thom_stargazer.jpg'))
    
    @Plugin.command('skeleton')
    def on_skeleton(self, event):
        skeleton = 'skeleton' + str(random.randint(1,19)) + '.jpg'
        return event.msg.reply(attachment=os.path.join('pictures/skeletons/') + skeleton)

    @Plugin.command('dog')
    def on_dog(self, event):
        return event.msg.reply(requests.get('https://random.dog/woof.json').json()['url'])
