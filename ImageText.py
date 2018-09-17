from PIL import ImageFont, Image, ImageDraw


font = ImageFont.truetype("comic-sans.ttf", 40)


def textadd(message):
    '''
    draws the text onto the goo image.
    '''
    img = Image.open("/home/ubuntu/thombot_v2/pictures/blankgoo.png")
    draw = ImageDraw.Draw(img)
    message = textprep(message)
    draw.text((420, 150), message, fill=(0,0,0,0), font=font)
    draw = ImageDraw.Draw(img)
    img.save("/home/ubuntu/thombot_v2/pictures/gootext.png")


def textprep(message):
    '''
    tries to fit the text onto the page.
    This function needs to be updated. It works but not well.
    '''
    count = 0
    place = 0
    for letter in message:
        if letter != " ":
            count = count + 1
        elif count >= 3:
            message = message[:place] + "\n" + message[place + 1:]
        place = place + 1
    return message