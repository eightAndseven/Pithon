import RPi.GPIO as GPIO
from external_db import db_connection as db
from datetime import datetime as dt
import time as tm
import decimal
import random
import serial

#function to return datenow string
def timeNow():
    return str(dt.now().replace(microsecond = 0))

# START

#set GPIO board as BCM
GPIO.setmode(GPIO.BCM)
pinList = [18, 23, 24, 4, 17] 

# set GPIO pin as OUTPUT
for i in pinList:
	GPIO.setup(i, GPIO.OUT)


# get connection and get cursor for db
conn = db()
cur = conn.cursor()

# get arduino value from serial
arduino = serial.Serial("/dev/ttyACM0")
arduino.baudrate=57600
tm.sleep(2)

#infinite loop
while True:
    try:
        # get value from serial
        data = arduino.readline()
        data = data.replace('\r\n', '')
        print data
        #get value separated by tab
        d = dict(x.split(":") for x in data.split(";"))

        #check GPIO pin and put to dictionary with key matching socket number
        pin_d = {str(pinList.index(x) + 1) : GPIO.input(x) for x in pinList}
        
        #loop to get 1, 2, 3, 4, 5 for socket pins
        for pin_count in range(1,6):
            #if pin_d is equal to ON
            if str(pin_d[str(pin_count)]) == '0':
                #get time now
                now = timeNow()
                #sql string to execute
                sql = "INSERT INTO power_con (socket_id, watt_cons, date_time) VALUES (%s, %s, %s)"
                #check if value from arduino is less than 1.000
                if float(d[str(pin_count)]) > 1.00:
                    #sql execute with values (socket id, wattage consumed from arduino, date_time)
                    cur.execute(sql, (pin_count, d[str(pin_count)], now))
                    #commit to database
                    conn.commit()
            else:
                #save into socket if socket is off
                curinsert = conn.cursor()
                curinsert.execute("""UPDATE socket SET appliance='NONE' WHERE id=%s""", (pin_count,))
                conn.commit()
                curinsert.close()
        #sleep for 1 second
        tm.sleep(.5)

    except Exception as e:
        print e
        tm.sleep(.5)

# END SCRIPT