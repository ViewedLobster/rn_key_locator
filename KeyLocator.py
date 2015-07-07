# This optimized piece of code is possible thanks to:
# pycurl
# RPi.GPIO

import RPi.GPIO as k
import time

import pycurl
from StringIO import StringIO



k.setmode(k.BCM)

pinKey = 18
pinLed = 27

k.setup(pinLed, k.OUT)
k.setup(pinKey, k.IN)

i=0

k.output(pinLed, 1)


def doCurl(keyValue = -1):
    buffer = StringIO()
    c = pycurl.Curl()
    address = 'http://rneventteknik.se/stage/io/key.php?key_status='+str(keyValue)
    print address
    c.setopt(c.URL, address)
    c.setopt(c.WRITEFUNCTION, buffer.write)
    c.perform()
    c.close()

    body = buffer.getvalue()
    
    print body
    


def main():
    # TODO better name for variable
    pinKeyValue = 0
    done = False
    while not done:
        # TODO could prabably improve
        pinKeyValue = k.input(pinKey)
        
            

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

doCurl()

