import RPi.GPIO as GPIO

#START
#set GPIO board as BCM
GPIO.setmode(GPIO.BCM)
pinList = [18, 23, 24, 4, 17] 

# set GPIO pin as OUTPUT and turn off
for i in pinList:
    GPIO.setup(i, GPIO.OUT)
    GPIO.output(i, GPIO.HIGH)
#END
