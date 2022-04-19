# Class to monitor a rotary encoder and update a value.  You can either read the value when you need it, by calling getValue(), or
# you can configure a callback which will be called whenever the value changes.

import RPi.GPIO as GPIO

class Screen:

    def __init__(self, screenPin, callback=None):
        self.screenPin = screenPin
        self.callback = callback
        self.state = 1
        GPIO.setup(self.screenPin, GPIO.OUT)

        self.on()

    def on(self):
        self.state = 1
        GPIO.output(self.screenPin, self.state)
        return self.state

    def off(self):
        self.state = 0
        GPIO.output(self.screenPin, self.state)
        return self.state

    def getState(self):
        return self.state
