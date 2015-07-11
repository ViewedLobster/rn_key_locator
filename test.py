# -*- coding: utf-8 -*-
import RPi.GPIO as k
import time

k.setmode(k.BCM)
pins = [2,3,4,5,6,12,13,16,17,18,19,20,21,22,23,24,25,26]

for pin in pins:
    k.setup(pin, k.IN)
    
while True:
    for pin in pins:
        print pin, k.input(pin)
        
    time.sleep(2)