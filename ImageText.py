from PIL import ImageFont
from PIL import Image
from PIl import ImageDraw

font = ImageFont.truetype("comicsans.ttf", 15)

#def textprep(message):


def textadd(message):
    img = Image.open("blankgoo.jpg")
    draw = ImageDraw.Draw(img)
    #message = textprep(message)
    draw.text((407, 191), message, font=font)
    draw = ImageDraw.Draw(img)
    img.save("gootext.png")