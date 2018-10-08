from PIL import ImageFont, Image, ImageDraw
import os


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

if __name__ == "__main__":
    #testing
    text = "this text is pretty long, I want to see it go off the bottom"
    textadd(text)
    with Image.open(cwd + "/pictures/gootext.png") as img:
        img.show()