from PIL import ImageFont, Image, ImageDraw

font = ImageFont.truetype("comic-sans.ttf", 60)

def textadd(message):
    img = Image.open("/home/pi/thombot_v2/pictures/blankgoo.png")
    draw = ImageDraw.Draw(img)
    message = textprep(message)
    draw.text((400, 110), message, fill=(0,0,0,0), font=font)
    draw = ImageDraw.Draw(img)
    img.save("/home/pi/thombot_v2/pictures/gootext.png")

def textprep(message):
    count = 0
    place = 0
    for letter in message:
        if letter != " ":
            count = count + 1
        elif count > 6:
            message[place] = "\n"
        place = place + 1
    return message