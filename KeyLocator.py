# This optimized piece of code is possible thanks to:
# pycurl
# RPi.GPIO

import RPi.GPIO as k
import time
import pycurl as pc

k.setmode(k.BCM)

pinKey = 18
pinLed = 27

k.setup(pinLed, k.OUT)
k.setup(pinKey, k.IN)

i=0

k.output(pinLed, 1)

time.sleep(10000)
def sendAction():
    pass
    


def main():
    # TODO better name for variable
    pinKeyValue = 0
    done = False
    while not done:
        # TODO could prabably improve
        pinKeyValue = k.input(pinKey)
        if pinKeyValue == 1:
            pass
            

        """
        print GPIO.input(button4)
        time.sleep(1)
        if GPIO.input(button4)==1:
            print "fuck yeah"
            GPIO.output(led, 0)
        else:
            GPIO.output(led, 1)
            
        if GPIO.input(button0)==1:
            print "0"
            break
        """



