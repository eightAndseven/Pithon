import MySQLdb as mysql
from datetime import datetime as dt
import time as tm
import decimal
import random

#function to return datenow string
def timeNow():
    return str(dt.now().replace(microsecond = 0))

#function to get mysql connection
def dbConn():
    db = mysql.connect(host="localhost", user="root", passwd="", db="powerboard")
    return db
def randDecimal():
    return float(decimal.Decimal(random.randrange(10000))/100)

# START
# get connection and get cursor for db
conn = dbConn()
cur = conn.cursor()

# # get arduino value from serial
# arduino = serial.Serial("/dev/ttyACM0")
# arduino.baudrate=9600
tm.sleep(2)

#infinite loop
while True:
    try:
        # get value from serial
        # data = arduino.readline()

        #data from arduino must be
        '''
            data = '1:0.0001;2:3.0213;3:1.2301;4:2.1302;5:2.3124'
        '''
        #dummy data (Just comment out if there is value from arduino)
        list_data = [randDecimal() for x in range(1,6)]
        data = ""
        for x in list_data:
            i = list_data.index(x) + 1
            data = data + str(i) + ":" + str(x)
            if i < 5:
                data = data + ";"
        #dummy data ends

        #get value separated by tab
        d = dict(x.split(":") for x in data.split(";"))

        #gets current time
        now = timeNow()
        sql = "INSERT INTO power_con (socket_id, watt_cons, date_time) VALUES (1, %s, %s), (2, %s, %s), (3, %s, %s), (4, %s, %s), (5, %s, %s)"
        #prepare statemt and execute
        cur.execute(sql, (d['1'], now, d['2'], now, d['3'], now, d['4'], now, d['5'], now))
        #commit to database
        conn.commit()
        print "DB SAVED"
        tm.sleep(1)

    except Exception as e:
        print e
        tm.sleep(1)

#end