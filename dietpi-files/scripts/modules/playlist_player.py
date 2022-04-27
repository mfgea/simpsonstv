# Class to manage and handle a videos playlist It will use OMXPlayer to reproduce

from fileinput import close
import json
import logging
import subprocess
from os import path, listdir, remove
from getpass import getuser
from random import shuffle
import tempfile
from time import sleep
from PIL import Image, ImageDraw, ImageFont
from omxplayer.player import OMXPlayer

#logging.basicConfig(level=logging.DEBUG)

SUBTITLE_TEMPLATE = '''
1
00:00:00,000 --> 00:00:{length},000
{text}
'''

USER=getuser()

def cleanupDbusFiles():
    global USER
    try:
        remove('/tmp/omxplayerdbus.' + USER + '.pid')
        remove('/tmp/omxplayerdbus.' + USER)
    except FileNotFoundError:
        print("All clean")

cleanupDbusFiles()

def genBackdropImage(channelName):
    global USER
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

class Channel:
    def __init__(self, root: str, label: str, uri: str, shuffle: bool=True):
        self.root: str = root
        self.label: str = label
        self.uri: str = uri
        self.shuffle: bool = shuffle
        self.items = []
        self.currentIndex = -1
        self.backdropImage = ''
        self.load()
    
    def getLen(self):
        return len(self.items);

    def getLabel(self):
        return self.label;

    def getType(self):
        if(self.uri.lower().startswith(tuple(['file', 'http', 'rtsp', 'rtmp']))):
            return 'url'
        return 'directory';
    
    def load(self):
        self.backdropImage = genBackdropImage(self.label)
        if(self.getType() == 'directory'):
            for file in listMp4(path.join(self.root, self.uri)):
                self.items.append(path.join(self.root, self.uri, file))

        elif(self.getType() == 'url'):
            self.items.append(self.uri)

        if(self.shuffle):
            shuffle(self.items)
        else:
            self.items.sort()
    
    def getItems(self):
        return self.items
    
    def nextVideo(self):
        self.currentIndex += 1
        if (self.currentIndex >= len(self.items)):
            self.currentIndex = 0;
        return self.items[self.currentIndex]

    def getBackdrop(self):
        return self.backdropImage


class PlaylistPlayer:
    def __init__(self, rootPath=''):
        self.rootPath: str = rootPath
        self.channels: list[Channel] = []
        self.labelDuration = '05'
        self.currentIndex: int = 0
        self.player: OMXPlayer = None
        self.backdropProc = None
        self.channelLoaded = False

        self.playlistOptions = {
            'scanDirectories': True,
            'scanRoot': False
        };
        self.showChannelLabel = True

        ## Check if config file exists. If so, then load the config options
        if(path.isfile(self.rootPath + '/player.json')): # if player.json exists
            print("Loading player.json file")
            jsonFile = open(self.rootPath + '/player.json')
            data = json.load(jsonFile)
            self.playlistOptions = data["playlistOptions"]
            self.showChannelLabel = data["showChannelLabel"]
            self.labelDuration = data["labelDuration"]

            for channel in data["appendChannels"]:
                self.channels.append(Channel(self.rootPath, channel['label'], channel['uri'], channel['shuffle']))
        
        ## Scan the root path. Each directory turns into a channel 
        if(self.playlistOptions['scanDirectories']):
            dirs = listDirs(self.rootPath)
            tmpChannels = []
            for dirName in dirs:
                channel = Channel(self.rootPath, dirName, dirName)
                if (channel.getLen() > 0):
                    tmpChannels.append(channel)
            tmpChannels.extend(self.channels)
            self.channels = tmpChannels

        ## Scans the root video files and adds them as a new channel 
        if(self.playlistOptions['scanRoot']):
            channel = Channel(self.rootPath, 'Root', '.')
            if (channel.getLen() > 0):
                self.channels.insert(0, channel)

    def _playbackFinished(self, _, exit_status):
        try:
            self.player.quit()
        except RuntimeError:
            pass
        finally:
            self.player=None
            if (exit_status==0):
                self.playNext()
    
    def loadChannel(self):
        channel: Channel = self.channels[self.currentIndex]
        print("Playing channel", channel.getLabel())
        if (self.backdropProc != None):
            subprocess.run(["sudo", "kill", "-9", str(self.backdropProc.pid)])
            self.backdropProc = None

        backdropPath = channel.getBackdrop()
        if (backdropPath):
            print("Showing backdrop", backdropPath)
            self.backdropProc = subprocess.Popen(["sudo", "fbi", "--noverbose", "-T", "1", backdropPath])

        self.channelLoaded = True

    def playNext(self):
        if len(self.channels) == 0:
            print("No videos")
            return
        if(not self.channelLoaded):
            self.loadChannel()
        channel: Channel = self.channels[self.currentIndex]
        video = channel.nextVideo()
        print("Playing file", video)
        if (self.player != None):
            print("Reusing old player", self.player)
            self.player.load(video)
        else:
            print("Spawning new player", self.player)
            self.player = OMXPlayer(video, args=['--no-osd', '--aspect-mode', 'fill'], dbus_name='org.mpris.MediaPlayer2.omxplayer2',pause=False)
            self.player.exitEvent += self._playbackFinished 

    def play(self):
        if self.player != None:
            self.player.play()
        else:
            self.playNext()

    def pause(self):
        if self.player != None: self.player.pause()

    def nextChannel(self):
        self.currentIndex += 1
        if (self.currentIndex >= len(self.channels)):
            self.currentIndex = 0
        self.loadChannel()
        self.playNext()

    def prevChannel(self):
        self.currentIndex -= 1
        if (self.currentIndex < 0):
            self.currentIndex = len(self.channels) - 1
        self.loadChannel()
        self.playNext()

    def cleanup(self):
        if (self.backdropProc != None):
            subprocess.run(["sudo", "kill", "-9", self.backdropProc.pid])
        if (self.player and "quit" in self.player):
            self.player.quit()
