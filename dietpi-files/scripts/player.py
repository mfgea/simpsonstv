import os
import random
import RPi.GPIO as GPIO
from time import sleep

from modules.toggle_button import ToggleButton
from modules.encoder import Encoder
from modules.screen import Screen
from modules.playlist_player import PlaylistPlayer

VIDS_DIR='/home/bart/videos/'

BUTTON = 26
SCREEN = 18
ENCODER_A = 27
ENCODER_B = 22

libraries = []

# import logging
# logging.basicConfig()
# logging.getLogger().setLevel(logging.DEBUG)

def turnOnScreen():
    global screen
    global player
    print ("Screen ON")
    os.system('raspi-gpio set 19 op a5')
    playlist.play()
    screen.on()

def turnOffScreen():
    global screen
    global player
    print ("Screen OFF")
    os.system('raspi-gpio set 19 ip')
    playlist.pause()
    screen.off()

def playNextVideo():
    global playlist
    playlist.nextChannel()

def playPrevVideo():
    global playlist
    playlist.prevChannel()

def onToggle(state):
    if state:
        turnOnScreen()
    else:
        turnOffScreen()

def onEncoderChange(value, direction):
    if direction == "R":
        playNextVideo()
    if direction == "L":
        playPrevVideo()

GPIO.setwarnings(False)
GPIO.cleanup()
GPIO.setmode(GPIO.BCM)

screen = Screen(SCREEN)
ToggleButton(BUTTON, callback=onToggle)
Encoder(ENCODER_A, ENCODER_B, callback=onEncoderChange)
playlist = PlaylistPlayer(VIDS_DIR)

turnOnScreen()

try:
    while True:
        sleep(5)
except Exception:
    pass

GPIO.cleanup()
