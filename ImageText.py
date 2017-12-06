from PIL import ImageFont, Image, ImageDraw

font = ImageFont.truetype("comic-sans.ttf", 15)

#def textprep(message):


def textadd(message):
    img = Image.open("/home/pi/thombot_v2/pictures/blankgoo.png")
    draw = ImageDraw.Draw(img)
    #message = textprep(message)
    draw.text((407, 191), message, font=font)
    draw = ImageDraw.Draw(img)
    img.save("/home/pi/thombot_v2/pictures/gootext.png")