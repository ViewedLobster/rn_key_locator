import wiringpi2 as wp


wp.piBoardRev()

wp.wiringPiSetupGpio()

pinKey = 1
pinLed = 2

# pin x som 0: input 1:
wp.pinMode(pinKey, 0)
wp.pinMode(pinLed, 1)

# (Pin x, pullDown
wp.pullUpDnControl(pinKey, 1)

