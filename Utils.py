from PIL import ImageFont, Image, ImageDraw
import os
import discord
import psycopg2


font = ImageFont.truetype("comic-sans.ttf", 40)

cwd = os.getcwd()

def textadd(message):
    '''
    draws the text onto the goo image.
    '''
    with Image.open(cwd + "/pictures/blankgoo.png") as img:
        draw = ImageDraw.Draw(img)
        message = textprep(message)
        draw.text((420, 150), message, fill=(0,0,0,0), font=font)
        draw = ImageDraw.Draw(img)
        img.save(cwd + "/pictures/gootext.png")


def textprep(message):
    '''
    tries to fit the text onto the page.
    This function needs to be updated. It works but not well.
    '''
    letter_list = []
    line_list = []
    for letter in message:
        if len(letter_list) <= 2 or letter != " ":
            letter_list.append(letter)
        else:
            line = "".join(letter_list)
            line_list.append(line)
            letter_list = []
    line = "".join(letter_list)
    line_list.append(line)
    text = "\n".join(line_list)
    return text

def connect_to_db():
    try:
        conn = psycopg2.connect("dbname='gift' user='thombot' host='localhost' password='thombot'")
    except:
        print("Was unable to connect to the database")
        conn = False
    return conn

def create_gift_embed(title, url, description, img):
    '''
    creates the embed for christmas gifts
    '''
    gift_embed = discord.Embed(title=title, type="rich", 
                        description=description, url=url)
    gift_embed.set_image(url=img)
    return gift_embed

def get_gift(user):
    conn = connect_to_db()
    cur = conn.cursor()
    gift = cur.execute("""SELECT gift FROM user_gifts WHERE user_id = {};""".format(user))
    print("gift")


if __name__ == "__main__":
    #testing
    get_gift(12345)
