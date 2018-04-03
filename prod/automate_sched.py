# import RPi.GPIO as GPIO
import MySQLdb as mysql
from datetime import datetime as dt
import time as tm

#functions
# #function to return date Yesterday string
def timeNow():
    return dt.now().replace(microsecond=0)

#function to get mysql connection
def dbConn():
    db = mysql.connect(host="localhost", user="root", passwd="", db="powerboard")
    return db

#START
#set GPIO board as BCM
# GPIO.setmode(GPIO.BCM)
pinList = [18, 23, 24, 4, 17] 

# # set GPIO pin as OUTPUT
# for i in pinList:
# 	GPIO.setup(i, GPIO.OUT)

# get database connection
conn = dbConn()

#infinite loop
while True:
    try:
        cur = conn.cursor()
        now = timeNow()

        #check GPIO pin and put to dictionary with key matching socket number
        pin_d = {str(pinList.index(x) + 1) : x for x in pinList}
        sql = "SELECT id, socket_id, date_time_sched, action, description FROM schedule WHERE date_time_sched=%s AND state=%s"
        cur.execute(sql, (now, "READY"))
        results = cur.fetchall()
        count = cur.rowcount
        print count
        if (count >= 1):
            for row in results:
                pid, socket_id, date_sched, action, description = row
                print "Executed id", pid, "of socket", socket_id, "turn", action
                
                #do in GPIO here

                curdel = conn.cursor()
                sql2 = "DELETE FROM schedule WHERE id=%s"
                curdel.execute(sql, (pid))
                conn.commit()
                curdel.close()
        else:
            print now
        cur.close()
        tm.sleep(1)
    except Exception as e:
        print e
        tm.sleep(1)


#END