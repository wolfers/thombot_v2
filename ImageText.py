from PIL import ImageFont, Image, ImageDraw

font = ImageFont.truetype("comic-sans.ttf", 40)

def textadd(message):
    img = Image.open("/home/pi/thombot_v2/pictures/blankgoo.png")
    draw = ImageDraw.Draw(img)
    message = textprep(message)
    draw.text((420, 110), message, fill=(0,0,0,0), font=font)
    draw = ImageDraw.Draw(img)
    img.save("/home/pi/thombot_v2/pictures/gootext.png")

def textprep(message):
    count = 0
    place = 0
    for letter in message:
        if letter != " ":
            count = count + 1
        elif count > 5:
            message = message[:place] + "\n" + message[place + 1:]
        place = place + 1
    return message