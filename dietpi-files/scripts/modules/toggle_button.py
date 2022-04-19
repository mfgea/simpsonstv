import RPi.GPIO as GPIO
from time import time

class ToggleButton():
    def __init__(self, pin, callback, initialState=1, bouncetime=500):
        self.callback = callback
        self.pin = pin
        self.bouncetime = bouncetime
        self.lastcalled = time()
        self.state = initialState

        GPIO.setup(self.pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.add_event_detect(self.pin, GPIO.FALLING, callback=self.onClick)

        self.lastpinval = GPIO.input(self.pin)

    def onClick(self, channel):
        currenttime = time()
        diff = round((currenttime - self.lastcalled) * 1000)
        waiting = diff < self.bouncetime

        if not waiting:
            self.state = not self.state
            self.callback(self.state)
            self.lastcalled = currenttime