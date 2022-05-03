# Class to manage and handle a videos playlist It will use OMXPlayer to reproduce

from fileinput import close
import json
import logging
import subprocess
from os import path, remove
from getpass import getuser
from random import shuffle
from time import sleep
from omxplayer.player import OMXPlayer
from channel import Channel
from utils import listDirs
from debounce import debounce

#logging.basicConfig(level=logging.DEBUG)

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

        self.cleanupDbusFiles()

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

    def cleanupDbusFiles(self):
        USER=getuser()
        try:
            remove('/tmp/omxplayerdbus.' + USER + '.pid')
            remove('/tmp/omxplayerdbus.' + USER)
        except FileNotFoundError:
            print("All clean")

    def _playbackFinished(self, _, exit_status):
        try:
            self.player.quit()
        except RuntimeError:
            pass
        try:
            subprocess.run(["pkill", "-9", "omxplayer"])
        except RuntimeError:
            pass
        self.player=None
        sleep(0.5)
        if (exit_status==0):
            self.playNext()

    def loadChannel(self):
        channel: Channel = self.channels[self.currentIndex]
        print("Playing channel", channel.getLabel())
        if (self.backdropProc != None):
            subprocess.run(["pkill", "-9", "fbi"])
            self.backdropProc = None

        backdropPath = channel.getBackdrop()
        if (backdropPath):
            print("Showing backdrop", backdropPath)
            self.backdropProc = subprocess.Popen(["fbi", "--noverbose", "-T", "1", backdropPath])

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
            sleep(3)

    def play(self):
        if self.player != None:
            self.player.play()
        else:
            self.playNext()

    def pause(self):
        if self.player != None: self.player.pause()

    @debounce(1)
    def nextChannel(self):
        self.currentIndex += 1
        if (self.currentIndex >= len(self.channels)):
            self.currentIndex = 0
        self.loadChannel()
        self.playNext()

    @debounce(1)
    def prevChannel(self):
        self.currentIndex -= 1
        if (self.currentIndex < 0):
            self.currentIndex = len(self.channels) - 1
        self.loadChannel()
        self.playNext()

    def cleanup(self):
        if (self.player and "quit" in self.player):
            self.player.quit()
        subprocess.run(["pkill", "-9", 'fbi'])
        subprocess.run(["pkill", "-9", 'omxplayer'])
