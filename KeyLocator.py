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
        
        k.setup(self.pinLed, k.OUT)
        k.setup(self.pinKey, k.IN)
        k.setup(self.pinDoor, k.IN)
        
        k.output(self.pinLed, 1)
        
        self.keyState = None
        self.doorState = None
        
        self.lastKeyState = None
        self.lastDoorState = None
        
        self.emergency = None
        
        self.smsGood = "Key is back and everything is back to normal!"
        
        
        # Hahaha, much secure
        self.checksum = "67fgd83kdn3249f34nnjf27d2lmkcds"
    
    
    def doCurl(self, keyValue = -1, doorValue = -1, messageType = "ping", format = 'json'):
        buffer = StringIO()
        c = pycurl.Curl()
        address = 'http://rneventteknik.se/stage/io/key.php?key='+str(keyValue)+"&door="+str(doorValue)+"&msgType="+str(messageType)+"&format=" + str(format)+ "&checksum=" + self.checksum
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
                
                response = self.doCurl(self.keyState, self.doorState, "changed")
                if self.emergency and self.keyState and not self.doorState:
                    
                    self.emergency = False
                    
                    # send back to normal message
                    self.doSMS(self.smsGood)
                    
                        

                
                
                
            
            
            
            
            
            
            self.lastKeyState = self.keyState
            self.lastDoorState = self.doorState
            self.lastTime = time.time()
                
        
            
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        # TODO better name for variable
        pinKeyValue = k.input(self.pinKey)
        pinDoorValue = k.input(self.pinAlarm)
        done = False
        lastState = 0
        lastAlarm = 0
        sentSMS = False
        response = self.doCurl(keyValue = pinKeyValue, doorValue = pinDoorValue, messageType = "ping")
        
        while not done:
            # TODO could prabably improve
            pinKeyValue = k.input(self.pinKey)
            pinDoorValue = k.input(self.pinAlarm)
            if not lastState == pinKeyValue:
                k.output(self.pinLed, pinKeyValue)
                self.switchLED(0 if pinKeyValue else 1)
                response = self.doCurl(keyValue = pinKeyValue, doorValue = pinDoorValue, messageType = "changed")
                
                
                
                
                
                
            
            if lastAlarm != pinDoorValue:
                
                if pinDoorValue:
                    
                    if not pinKeyValue and not sentSMS:
                        
                        response = self.doCurl(keyValue = pinKeyValue, doorValue = pinDoorValue, messageType = "key_alarm_alert_emergency")
                        
                        if self.smsEnabled:
                            self.doSMS(response['feedback'])
                        sentSMS = True
                else:
                    response = self.doCurl(keyValue = pinKeyValue, doorValue = pinDoorValue, messageType = "key_alarm_alert_emergency_averted")
                
                
            
            if not pinDoorValue and sentSMS:
                sentSMS = False
            
            
            currentTime = time.time()
            
            if currentTime - self.lastTime > 3600:
                response = self.doCurl(keyValue = pinKeyValue, doorValue = pinDoorValue, messageType = "ping")
            
            
            lastState = pinKeyValue
            lastAlarm = pinDoorValue
            
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
