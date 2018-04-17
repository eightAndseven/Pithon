import RPi.GPIO as gpio
import time


#set GPIO board as BCM
gpio.setmode(gpio.BCM)
pinList = [18, 23, 24, 4, 17]
# 18, 
# set GPIO pin as OUTPUT
for i in pinList:
	gpio.setup(i, gpio.OUT)

pin_dict = {str(pinList.index(x) + 1) : x for x in pinList}

print (pin_dict)

while True:
    try:
        uinput = str(input("On/Off: "))
        print pin_dict[uinput]
        if gpio.input(pin_dict[uinput]) == 0:
            gpio.output(gpio.input(pin_dict[uinput]), gpio.HIGH)
        elif gpio.input(pin_dict[uinput]) == 1:
            gpio.output(pin_dict[uinput], gpio.LOW)
        elif uinput == 'exit'
            gpio.cleanup()
            break
        else
            print ('Wrong input')
    except Exception as e:
        print (e)
        

