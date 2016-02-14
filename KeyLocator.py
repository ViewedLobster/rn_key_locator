# -*- coding: utf-8 -*-
# This optimized piece of code is possible thanks to:
# pycurl
# RPi.GPIO
# crontab -e
#@reboot sudo python /home/pi/code/key-locator/KeyLocator.py >> /home/pi/code/key-locator/key.log 2>&1

import RPi.GPIO as k
import time

import pycurl
from StringIO import StringIO

import json
import logging
import random

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

        # An assortment of goods to be owed
        self.goodsList = ["bulle", "Guldkällan", "lap dance", "juice", "tårta", "crystal meth", "saft", "lurre till Jurre", "virre", "chirre", "rent mjöl, gärna i påse", "TeX:ad kanallista"]
        
        self.amountList = ["skälig mängd", "fyra dagsböter", "fem fotbollplaner", "fyrtio tusen miljarder", "33 cl", "1 kg"]
        
        self.explanation = ["Straffet bestäms utifrån den misstänktes beräknade årsinkomst vid tidpunkten när straffet skall bestämmas. Med årsinkomst avses inkomst före skatt med avdrag för kostnader för inkomstens förvärvande. Som inkomst räknas också mer kontinuerligt utgående ersättning eller bidrag till den misstänkte. Det gäller till exempel arbetslöshetsersättning, ekonomiskt bistånd, studiebidrag, bostadsbidrag och underhållsbidrag.", 
                "Den misstänktes egna uppgifter om sina ekonomiska förhållanden bör i allmänhet godtas. En kontroll bör dock göras om det finns anledning anta att uppgifterna är felaktiga eller ofullständiga i en omfattning som kan antas påverka straffbeloppet.",
                "Straffets villkor varierar mellan olika nämnder. Anstalten RN ger möjlighet till arbete, utbildning, behandlingsprogram och annan verksamhet. Straff infördes hos RN under 1800-talet och anses bland annat minska risken för fängelsevåldtäkter"]
        
        self.keyState = None
        self.doorState = None
        
        self.lastKeyState = None
        self.lastDoorState = None
        
        self.emergency = None
        self.emergencyFile = "emergencyTime.txt"
        
        self.smsGood = "Källarnyckeln är åter på sin plats. Enligt min formel är du skyldig "
        self.smsGoodPt2 = " bulle"
        self.smsBad = "Källarnyckeln!! Lämna tillbaka den innan du går hem. Annars antar jag att någon köper bulle till nästa tisdag..."
        
        
        # Hahaha, much secure
        self.checksum = "67fgd83kdn3249f34nnjf27d2lmkcds"
    
    def generateMessage(self):
        message = "Kom tillbaka med nyckeln, om den ej är tillbaka inom 10 minuter blir påföljden ett vite i form av "
        i = random.randrange(len(self.amountList));
        message = message + self.amountList[i]

        i = random.randrange(len(self.goodsList))
        message = message + " " + self.goodsList[i]

        i = random.randrange(len(self.explanation))
        message = message + " " + self.explanation[i]
    
    def doCurl(self, keyValue = -1, doorValue = -1, emergencyState = -1, messageType = "ping", format = 'json'):
        buffer = StringIO()
        c = pycurl.Curl()
        address = 'http://rneventteknik.se/stage/io/key.php?key='+str(keyValue)+"&door="+str(doorValue)+"&emergency="+str(int(emergencyState))+"&msgType="+str(messageType)+"&format=" + str(format)+ "&checksum=" + self.checksum
        c.setopt(c.URL, address)
        c.setopt(c.WRITEFUNCTION, buffer.write)
        try:
            c.perform()
        except Exception as e:
            logging.error(e.message)
        c.close()
    
        body = buffer.getvalue()
        self.lastTime = time.time()
        
        return self.jsonDecoder.decode(body)
    
    
    def main(self):
        
        # keyState is true if key is in place
        self.keyState = k.input(self.keyPin)
        # DoorState is true if door is locked
        self.doorState = k.input(self.doorPin)
        self.lastKeyState = self.keyState
        self.lastDoorState = self.doorState
        
        self.emergency = not self.keyState and self.doorState
        
        done = False

        self.doSMS("hahaha")
        print "sent message"
        
        while not done:
            self.keyState = k.input(self.keyPin)
            self.doorState = k.input(self.doorPin)
            
            
            
            k.output(self.ledPin, not self.keyState)
            if self.keyState != self.lastKeyState or self.doorState != self.lastDoorState:
                
                if self.emergency and self.keyState and not self.doorState:
                    
                    self.emergency = False

                    # Key is back and all is well

                    """
                    f = open(self.emergencyFile, "r")
                    string = f.readline()
                    f.close()
                    if string != "None":
                        emergencyTime = float(string)
                        timeDiff = time.time()-emergencyTime
                    
                        bulle = round(timeDiff/1) #43200.)
                    
                    f = open(self.emergencyFile, "w")
                    f.write("None")
                    f.close()
                    
                    # send back to normal message
                    if string != "None":
                        self.doSMS(self.smsGood + str(bulle) + self.smsGoodPt2)
                    
                    """
                    
                    
                elif not self.keyState and self.doorState:
                    self.emergency = True
                    
                    # If door locked and key gone fishing
                    
                    smsString = self.generateMessage()
                    self.doSMS(smsString)

                    
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
        pycurl_connect.setopt(pycurl.URL, 'https://api.getsupertext.com/v1/conversations/252585/messages')
        # rn-eventteknik: 44393
        # test-api: 252585
		# send as Magnus: 0a6f4ffcc6322271ecc6b1ddb90d83720700acc69bd61b7f96e248f7765d
		# send as Johan: 803647742c19c29a3e7bbbc0eddef9ad49ccfbd22c7d304bd929637036b3
        #send as: Rn Key Defence System 6cd627bf1b1c7aa9d4a980b73dac83984d7b70b5eaaaf3212c1d968cbec4 0763035548
        pycurl_connect.setopt(pycurl.HTTPHEADER, ['Auth-Token: 803647742c19c29a3e7bbbc0eddef9ad49ccfbd22c7d304bd929637036b3',
                                                  'application/json, text/javascript, */*; q=0.01',
                                                  'Client-Token: web_w3',
                                                  'Client-Version: 1'])
        pycurl_connect.setopt(pycurl.POSTFIELDS, "message="+str(smsString)+"&send_to_self=1")
        try:
            pycurl_connect.perform()
        except Exception as e:
            logging.error(e.message)
        pycurl_connect.close()
       
    def switchLED(self, LEDState):
        k.output(self.pinLed, LEDState)

logging.basicConfig(filename="keydefence.log", level=logging.DEBUG)

keyLocator = KeyLocator()
keyLocator.main()
