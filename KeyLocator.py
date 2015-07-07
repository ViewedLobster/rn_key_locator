# This optimized piece of code is possible thanks to:
# pycurl
# RPi.GPIO

import RPi.GPIO as k
import time
import pycurl as pc

GPIO.setmode(GPIO.BCM)

pinKey = 18
pinLed = 27

k.setup(pinLed, k.OUT)
k.setup(pinKey, k.IN)

i=0


def sendAction():
    


def main():
    # TODO better name for variable
    pinKeyValue = 0
    done = False
    while not done:
        # TODO could prabably improve
        pinKeyValue = k.input(pinKey)
        if pinKeyValue == 1:
            
        
        
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


main()


