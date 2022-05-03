from os import path, listdir
from getpass import getuser
from PIL import Image, ImageDraw, ImageFont

def genBackdropImage(channelName):
    USER=getuser()
    loadingMsg = "loading..."
    width, height = (480, 320)

    fontPrimary = ImageFont.truetype("DejaVuSans-Bold.ttf", size=40)
    fontSecondary = ImageFont.truetype("DejaVuSans-Bold.ttf", size=16)
    img = Image.new('RGB', (width, height), color='black')
    draw = ImageDraw.Draw(img)

    tw, th = draw.textsize(channelName, font=fontPrimary)
    draw.text((10, ((height-th)/2)), channelName, font=fontPrimary, fill=(255, 255, 255))

    lw, lh = draw.textsize(loadingMsg, font=fontSecondary)
    draw.text((width-lw-10, height-lh-10), loadingMsg, font=fontSecondary, fill=(160, 160, 160))

    filename = '/tmp/backdrop.' + channelName + '.' + USER + '.png'
    img.save(filename)
    return filename

def listMp4(rootpath):
    entries = []
    for entry in listdir(rootpath):
        if entry.lower().endswith('.mp4'):
            entries.append(entry)
    return entries

def listDirs(rootpath):
    entries = []
    for entry in listdir(rootpath):
        fullpath = path.join(rootpath, entry)
        if path.isdir(fullpath):
            entries.append(entry)
    return entries

def hasMethod(o, name):
    return (o is not None) and callable(getattr(o, name, None))