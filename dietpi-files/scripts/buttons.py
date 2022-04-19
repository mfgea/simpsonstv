import RPi.GPIO as GPIO
import os
from time import sleep

from modules.toggle_button import ToggleButton
from modules.encoder import Encoder
from modules.screen import Screen

DIR='/home/bart/bin/'

BUTTON = 26
SCREEN = 18
ENCODER_A = 27
ENCODER_B = 22

def turnOnScreen():
    global screen
    print ("Screen ON")
    os.system('raspi-gpio set 19 op a5')
    os.system(DIR + 'dbuscontrol.sh play') # play video
    screen.on()

def turnOffScreen():
    global screen
    print ("Screen OFF")
    os.system('raspi-gpio set 19 ip')
    os.system(DIR + 'dbuscontrol.sh pause') # pause video
    screen.off()

def playNextVideo():
    print ("Next movie")
    os.system('ps -aux | grep omxplayer | grep -v grep | awk \'{ print $2 }\' | xargs kill -9')

def rewidVideo():
    print ("rewid 15 second")
    position = int(os.popen(DIR + "dbuscontrol.sh status | grep 'Position:' | awk '{print $2}'").read())
    print (position)
    rewidTime = int(15) # 15 second
    newPosition = position - (rewidTime * 1000 * 1000) # position - 15 second (time must be in microsecond)
    print (newPosition)
    os.system(DIR + 'dbuscontrol.sh setposition %s' % (newPosition)) #

# def shutdownSystem():
#     print ("Poweroff")
#     os.system('poweroff')

def onToggle(state):
    if state:
        turnOnScreen()
    else:
        turnOffScreen()

def onEncoderChange(value, direction):
    if direction == "R":
        playNextVideo()
    if direction == "L":
        rewidVideo()

# Without this, backlight control does not work with the official driver
# os.system('echo 1 | tee /sys/class/backlight/*/bl_power')
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

screen = Screen(SCREEN)
ToggleButton(BUTTON, callback=onToggle)
Encoder(ENCODER_A, ENCODER_B, callback=onEncoderChange)

try:
    while True:
        sleep(5)
except Exception:
    pass

GPIO.cleanup()
