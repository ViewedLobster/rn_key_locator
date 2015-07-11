# -*- coding: utf-8 -*-
# This optimized piece of code is possible thanks to:
# pycurl
# RPi.GPIO

import RPi.GPIO as k
import time

import pycurl
from StringIO import StringIO

import json

class KeyLocator:
    
    def __init__(self):
        
        self.smsEnabled = True
        
        self.lastTime = None

        self.jsonDecoder = json.JSONDecoder()
        k.setmode(k.BCM)
        
        self.keyPin = 18
        self.ledPin = 27
        self.doorPin = 17
        
        self.LEDState = 0
        
        k.setup(self.ledPin, k.OUT)
        k.setup(self.keyPin, k.IN)
        k.setup(self.doorPin, k.IN)
        
        
        self.keyState = None
        self.doorState = None
        
        self.lastKeyState = None
        self.lastDoorState = None
        
        self.emergency = None
        self.emergencyFile = "emergencyTime.txt"
        
        self.smsGood = "Källarnyckeln är åter på sin plats. Enligt min formel är du skyldig  "
        self.smsGoodPt2 = " bulle"
        self.smsBad = "Källarnyckeln!! Lämna tilbaka den innan du går hem. Antar att någon köper bulle till nästa tisdag"
        
        
        # Hahaha, much secure
        self.checksum = "67fgd83kdn3249f34nnjf27d2lmkcds"
    
    
    def doCurl(self, keyValue = -1, doorValue = -1, emergencyState = -1, messageType = "ping", format = 'json'):
        buffer = StringIO()
        c = pycurl.Curl()
        address = 'http://rneventteknik.se/stage/io/key.php?key='+str(keyValue)+"&door="+str(doorValue)+"&emergency="+str(int(emergencyState))+"&msgType="+str(messageType)+"&format=" + str(format)+ "&checksum=" + self.checksum
        c.setopt(c.URL, address)
        c.setopt(c.WRITEFUNCTION, buffer.write)
        c.perform()
        c.close()
    
        body = buffer.getvalue()
        self.lastTime = time.time()
        
        return self.jsonDecoder.decode(body)
    
    
    def main(self):
        
        self.keyState = k.input(self.keyPin)
        self.doorState = k.input(self.doorPin)
        self.lastKeyState = self.keyState
        self.lastDoorState = self.doorState
        
        self.emergency = not self.keyState and self.doorState
        
        done = False
        
        while not done:
            self.keyState = k.input(self.keyPin)
            self.doorState = k.input(self.doorPin)
            
            
            
            k.output(self.ledPin, not self.keyState)
            if self.keyState != self.lastKeyState or self.doorState != self.lastDoorState:
                
                if self.emergency and self.keyState and not self.doorState:
                    
                    self.emergency = False
                    
                    """
                    f = open(self.emergencyFile, "r")
                    string = f.readline()
                    emergencyTime = float(string)
                    timeDiff = time.time()-emergencyTime
                    
                    bulle = round(timeDiff/43200.)
                    
                    f = open(self.emergencyFile, "w")
                    f.write("")
                    """
                    # send back to normal message
                    self.doSMS(self.smsGood)
                    
                    
                    
                elif not self.keyState and self.doorState:
                    self.emergency = True
                    
                    
                    """
                    f = open(self.emergencyFile, "r")
                    string = f.readline()
                    f.close()
                    if string == "":
                        f = open(self.emergencyFile, "w")
                        f.write(str(time.time()))
                    """
                    
                    self.doSMS(self.smsBad)
                    
                response = self.doCurl(self.keyState, self.doorState, self.emergency, "changed")
                
                
                

            self.lastKeyState = self.keyState
            self.lastDoorState = self.doorState
            self.lastTime = time.time()
            
            time.sleep(1)
            
                
    
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
    
    def doSMS(self, smsString):
        
        pycurl_connect = pycurl.Curl()
        pycurl_connect.setopt(pycurl.URL, 'https://api.getsupertext.com/v1/conversations/44393/messages')
        # rn-eventteknik: 44393
        # test-api: 252585
		# send as Magnus: 0a6f4ffcc6322271ecc6b1ddb90d83720700acc69bd61b7f96e248f7765d
		# send as Johan: 803647742c19c29a3e7bbbc0eddef9ad49ccfbd22c7d304bd929637036b3
        pycurl_connect.setopt(pycurl.HTTPHEADER, ['Auth-Token: 0a6f4ffcc6322271ecc6b1ddb90d83720700acc69bd61b7f96e248f7765d',
                                                  'application/json, text/javascript, */*; q=0.01'])
        pycurl_connect.setopt(pycurl.POSTFIELDS, "message="+str(smsString)+"&send_to_self=1")
        pycurl_connect.perform()
        
    def switchLED(self, LEDState):
        k.output(self.pinLed, LEDState)


keyLocator = KeyLocator()
keyLocator.main()
