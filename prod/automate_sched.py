import RPi.GPIO as GPIO
from external_db import db_connection as db
from datetime import datetime as dt
import time as tm

#functions

#function to return date Yesterday string
def timeNow():
    return str(dt.now().replace(microsecond=0))

#function to return a sched
def schedNow(db, now):
    cur = db.cursor()
    sql = "SELECT id, socket_id, date_time_sched, action, description FROM schedule WHERE date_time_sched='"+now +"' AND state='READY'"
    cur.execute(sql)
    result = cur.fetchall()
    count = cur.rowcount
    cur.close()
    return (count, result)

#function to delete a sched
def deleteSched(db, pid, socket_id):
    cur = db.cursor()
    sql = "DELETE FROM schedule WHERE id=%s AND socket_id=%s"
    cur.execute(sql, (pid, socket_id))
    db.commit()
    cur.close()

#function to do something in rpi GPIO
def doGPIOhere(row, pin_d):
    pid, socket_id, date_sched, action, description = row

    if action == "off":
        GPIO.output(pin_d[str(socket_id)], GPIO.HIGH)
    elif action == "on":
        GPIO.output(pin_d[str(socket_id)], GPIO.LOW)

    print "Executed id", pid, "of socket", socket_id, "turn", action
    return (pid, socket_id)


#START
#set GPIO board as BCM
GPIO.setmode(GPIO.BCM)
pinList = [18, 23, 24, 4, 17] 

# set GPIO pin as OUTPUT
for i in pinList:
	GPIO.setup(i, GPIO.OUT)

#check GPIO pin and put to dictionary with key matching socket number
pin_d = {str(pinList.index(x) + 1) : x for x in pinList}

#infinite loop
while True:
    try:
        # get database connection
        conn = db()
        now = timeNow()
        # get schedule for now
        count, results = schedNow(conn, now)
        if (count >= 1):
            for row in results:
                #do GPIO here
                pid, socket_id = doGPIOhere(row, pin_d)

                #delete schedule task
                deleteSched(conn, pid, socket_id)
        else:
            print now
        conn.close()
        tm.sleep(1)
    except Exception as e:
        print e
        tm.sleep(1)
#END