from PIL import ImageFont, Image, ImageDraw
import os
import discord
import psycopg2
import random


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
    created_gift = False
    conn = connect_to_db()
    cur = conn.cursor()
    #checks the database for a users gift. Returns None if no gift
    gift_id = cur.execute("""SELECT gift FROM user_gifts WHERE user_id = {};""".format(user))
    if gift_id == None:
        gift_id = create_gift_for_user(user)
        created_gift = True
    gift = cur.execute("""SELECT * FROM gifts WHERE gift_id = {};""".format(gift_id))
    conn.close()
    return gift, created_gift

def create_gift_for_user(user):
    '''
    selects a random gift for a user and then adds them to the database.
    returns the gift that they were given.
    '''
    conn = connect_to_db()
    cur = conn.cursor()
    gift_count = cur.execute("""SELECT COUNT(*) FROM gifts;""")
    gift_id = random.randint(0, gift_count-1)
    cur.execute("""INSERT INTO user_gifts VALUES({}, {});""".format(user, gift_id))
    conn.close()
    return gift_id

def remove_gift(user):
    '''
    removes the user from the gift database so that they can select another gift
    '''
    conn = connect_to_db()
    cur = conn.cursor()
    cur.execute("""DELETE FROM user_gifts WHERE user_id = {};""".format(user))

def add_gifts_to_db(gift_list):
    '''
    temporary function to add the gifts dictionary to the database
    '''
    conn = connect_to_db()
    cur = conn.cursor()
    for gift in gift_list:
        cur.execute("""INSERT INTO gifts(title, url, img, description) VALUES("{}", "{}", "{}", "{}");""".format(gift['title'], gift['url'],
                                                                                                        gift['img'], gift['description']))
        print(gift['title'], "added")
    conn.close()
    


if __name__ == "__main__":
    #testing
    gift_list = [
        {"title": 'Pet Collar', "url": "https://amzn.to/2r4SvvR", "img": "https://images-na.ssl-images-amazon.com/images/I/51FGmeCJvbL._SX300_QL70_.jpg", "description": "Get a nice collar for your favorite pet. You'll love to see them wear it around the house during the holidays!"},
        {"title": "Golden Garbage Bags", "url": "https://amzn.to/2RbONfd", "img": "https://images-na.ssl-images-amazon.com/images/I/415E4uTDcaL._SY300_QL70_.jpg", "description": "These garbage bags are probably made of solid gold! Waste disposal fit for a king."},
        {"title": "Log Pillow", "url": "https://amzn.to/2RdlokR", "img": "https://images-na.ssl-images-amazon.com/images/I/41ucR69UX%2BL._SX300_QL70_.jpg", "description": "Thought you would love this log pillow since you hate going outside but nature is still important."},
        {"title": "Lock Pick Kit", "url": "https://amzn.to/2FQcatk", "img": "https://images-na.ssl-images-amazon.com/images/I/51pcZ%2BvghHL._SY300_QL70_.jpg", "description": "Instead of putting thought into getting you a nice gift, I got you this lockpicking set! I figure you can jsut go steal whatever you want, I got you the gift of anything that's secured using a simple lock!"},
        {"title": "Corn that never goes bad!", "url": "https://amzn.to/2TJymZm", "img": "https://images-na.ssl-images-amazon.com/images/I/41vyS4t0TML._SY300_QL70_.jpg", "description": "Corn that doesn't go bad. I knew you'd love it. Just don't eat it. Put it on the shelf! yeah! Great conversation piece."},
        {"title": "BEES??", "url": "https://mountainsweethoney.com/bees/", "img": "https://s3.wp.wsu.edu/uploads/sites/609/2018/04/Bee-colony-1188x792-72dpi-1-1188x792.jpg", "description": "RUN."},
        {"title": "Gross Poop Car", "url": "https://amzn.to/2r0xdPU", "img": "https://images-na.ssl-images-amazon.com/images/I/41dqtK1K7ZL._SY300_QL70_.jpg", "description": "I didn't want this either, you can have it."},
        {"title": "pez", "url": "https://amzn.to/2DZO7GE", "img": "https://images-na.ssl-images-amazon.com/images/I/61vhao7jiKL._SX300_QL70_.jpg", "description": "You know I love collectables, so you can have this part."},
        {"title": "Neon Sign", "url": "https://amzn.to/2E0EYxI", "img": "https://images-na.ssl-images-amazon.com/images/I/51owjQoagtL._SX300_QL70_.jpg", "description": "For that garage bar you've been wanting to set up. You know, the hangout for all the lads."},
        {"title": "Honda parts", "url": "https://sfbay.craigslist.org/sby/mpo/d/honda-parts/6734958149.html", "img": "https://images.craigslist.org/00V0V_aR96bRInEJt_1200x900.jpg", "description": "it's, uh, for you. You have a car, right?"},
        {"title": "Slap Bracelet", "url": "https://amzn.to/2SfpNnx", "img": "https://images-na.ssl-images-amazon.com/images/I/41OjJHI-2QL._SY300_QL70_.jpg", "description": "You had one of thses when you were a kid and well, I didn't get to see you while I was in jail, hope you still like these."},
        {"title": "Placenta Face Mask", "url": "https://amzn.to/2S7DWD8", "img": "https://images-na.ssl-images-amazon.com/images/I/51i85j5zltL._SY300_QL70_.jpg", "description": "It's gotta be good for you skin or they wouldn't make it, right? I ahven't tried it, but I thought you could really use it."},
        {"title": "Beans", "url": "http://bit.ly/2Bx93m1", "img": "https://cdnimg.webstaurantstore.com/images/products/large/26470/156537.jpg", "description": "Things aren't looking so good, save these for a rough time. Might need them sooner rather than later."},
        {"title": "Burlap Sacks", "url": "https://www.ebay.com/i/292095591352?chn=ps", "img": "https://i.ebayimg.com/images/g/foYAAOSwT~9WkAme/s-l640.jpg", "description": "Used to use these all the time when I was a kid. Hope you enjoy themm as much as I did."},
        {"title": "Tire Valve Caps", "url": "https://amzn.to/2RdC9wh", "img": "https://images-na.ssl-images-amazon.com/images/I/41TvV6Fv77L._SY300_QL70_.jpg", "description": "Have fun, kid."},
        {"title": "Smile Trainer", "url": "https://amzn.to/2BxhGNG", "img": "https://images-na.ssl-images-amazon.com/images/I/311zOM06RfL._SY300_QL70_.jpg", "escription": "Your mom told me you really needed one of these."},
        {"title": "Pig Ski Mask", "url": "https://amzn.to/2DGzbwa", "img": "https://images-na.ssl-images-amazon.com/images/I/4145K3cmenL._SY300_QL70_.jpg", "description": "It's got pigs on it."},
        {"title": "Cow Heart", "url": "https://amzn.to/2DGzxTw", "img": "https://images-na.ssl-images-amazon.com/images/I/31wKcwwiEXL.jpg", "description": "At least it's warmer than my wifes heart, HAHAHAHAHAHA, GET IT? Please help me."},
        {"title": "Stylish Shirt", "url": "https://amzn.to/2Alduyx", "img": "https://images-na.ssl-images-amazon.com/images/I/41PMuYpvLUL._SX342_QL70_.jpg", "description": "Did a lot of research into waht kinds like these days, I tried really hard on this one."},
        {"title": "Bird Mask", "url": "https://amzn.to/2P3eKMb", "img": "https://images-na.ssl-images-amazon.com/images/I/51JWSGsxGWL._SY300_QL70_.jpg", "description": "Coo coo, motherfucker!"},
    #  {"title": "Microwave Cooking for One", "url": "https://amzn.to/2QhTpDd", "img": "", "description": "Maybe you wont need this someday."},
        {"title": "Waist Pouch", "url": "https://amzn.to/2r6jaby", "img": "https://images-na.ssl-images-amazon.com/images/I/519E4orYEUL._SY300_QL70_.jpg", "description": "This is so you can store you vape."},
        {"title": "Fruit Cake", "url": "https://amzn.to/2PXQSPd", "img": "https://images-na.ssl-images-amazon.com/images/I/61uXqo1TEOL._SX300_QL70_.jpg", "description": "I got you your favorite food!"},
        {"title": "A new yard", "url": "https://amzn.to/2RdW6Dh", "img": "https://images-na.ssl-images-amazon.com/images/I/61xKuuxoAxL._SY300_QL70_.jpg", "description": "I know you were going for that nature theme in the bathroom, I figured you could use this as a rug."},
        {"title": "Stained Glass", "url": "https://amzn.to/2DUrtjf", "img": "https://images-na.ssl-images-amazon.com/images/I/51T8ORa%2Bn4L._SX300_QL70_.jpg", "description": "Walk on this to show your friends you're a badass."},
        {"title": "Shift Knob", "url": "https://amzn.to/2DNxKwj", "img": "https://images-na.ssl-images-amazon.com/images/I/41tV8RdwEQL._SY300_QL70_.jpg", "description": "This was my first beer when I turned 21. You'll pass this on to your kids when they're old enough too."},
        {"title": "Celery Seed", "url": "https://amzn.to/2AoXvzk", "img": "https://images-na.ssl-images-amazon.com/images/I/412Atd%2BFhfL._SY300_QL70_.jpg", "description": "Your dad said you cook, so here's something that says celery in it."},
        {"title": "Urn", "url": "http://bit.ly/2QmiEUW", "img": "https://www.stardust-memorials.com/assets/images/mii-102-a-1.jpg", "description": "Ashes not included."},
        {"title": "Roof Wash", "url": "https://amzn.to/2DJ74wp", "img": "https://images-na.ssl-images-amazon.com/images/I/41fhk8O5mOL._SY445_QL70_.jpg", "description": "I'd love it if you came over after Christmas."},
        {"title": "Branding Irons", "url": "http://bit.ly/2zpzjx4", "img": "https://www.callisters.com/inet/storefront/getimage.php?recid=48449", "description": "For that long term relationship."},
        {"title": "Dancing Pole", "url": "https://amzn.to/2r29xdS", "img": "https://images-na.ssl-images-amazon.com/images/I/51hj4lWqlQL._SY300_QL70_.jpg", "description": "Uncle Thom-bot thinks you'd be REALLY good at this."},
        {"title": "Aluminum Wire", "url": "https://amzn.to/2RfQ44U", "img": "https://images-na.ssl-images-amazon.com/images/I/51mHjBYsT0L._SY300_QL70_.jpg", "description": "It's got lots of uses! hitting people, bondage, making daigrams in the dirt, and uh, making fursuits, probably."}
    ]
    add_gifts_to_db(gift_list)
