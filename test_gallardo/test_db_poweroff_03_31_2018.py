# import RPi.GPIO as GPIO
import time as tm
import decimal
import random
import serial
import MySQLdb as mysql

# # set GPIO board as BCM -> gpio readall
# GPIO.setmode(GPIO.BCM)
# pinList = [18, 23, 24, 4, 17, 27]

# # set GPIO pin as OUTPUT to write
# for i in pinList:
# 	GPIO.setup(i, GPIO.OUT)
# 	GPIO.output(i, GPIO.HIGH)

# # dictionary to set GPIO pin to their socket number {'socket number' : 'GPIO pin'}
# pin_dict = {'1':[pinList[0], 0], '2':[pinList[1], 0],'3':[pinList[2], 0],
# '4':[pinList[3], 0],'5':[pinList[4], 0],'6':[pinList[5], 0]}

# function to get date and time now
def timeNow():
    return str(dt.now().replace(microsecond = 0))

# function to get database connection
def dbConn():
    #connect to localhost as user and password using powerboard as database
    db = mysql.connect(host="localhost", user="root", passwd="", db="powerboard")
    return db

# function to get random decimal
def randDecimal():
    return float(decimal.Decial(random.randrange(10000))/100)

# START script
conn = dbConn()
cur = conn.cursor()

# arduino = serial.Serial("/dev/ttyACM0")
# arduino.baudrate=9600
# tm.sleep(2)

# infinite loop
while True:
    # pin_input = raw_input('On/Off: ')
    # try:
    #     if pin_input in pin_dict.keys():
    #         pin_me = pin_dict[pin_input][0]
    #         if pin_dict[pin_input][1] == 0:
    #             GPIO.output(pin_me, GPIO.LOW)
    #             pin_dict[pin_input][1] = 1                                       
    #         else:
    #             GPIO.output(pin_me, GPIO.HIGH)
    #             pin_dict[pin_input][1] = 0
                
                #infinite loop
                while True:
                    if (GPIO.output(pin_me) == False):
                        try:
                            data=arduino.readline()
                            d=dict(x.split(':') for x in data.split(';'))
                            now = timeNow()
                            sql = "INSERT INTO power_con (socket_id, watts_cons, date_time) VALUES (1, %s, %s), (2, %s, %s), (3, %s, %s), (4, %s, %s), (5, %s, %s)"
                            cur.execute(sql, (d['1'], now, d['2'], now, d['3'], now, d['4'], now, d['5'], now))
                            conn.commit()
                            print ('DB Saved')
                            tm.sleep(1)
                        except Exception as e:
                            print (e)
                            tm.sleep(0.7000)
        else:
            if pin_input == 'exit':
                break
            else:
                print('No')
    except:
        print('print has not been setup')
GPIO.cleanup()
print('Bye')
                    
# END script