from external_db import db_connection as db
from datetime import datetime, timedelta
import time as tm
import decimal
# DESCRIPTION : AUTOMATE SAVING IN DATABASE DAILY
# cron job every minute

# #function to return date Yesterday string
def dateYesterday():
    return (datetime.today() - timedelta(days=1)).date()

#function to check the last date saved for socket
def checkLastSavedSocket(db, x):
    cur = db.cursor()
    sql = "SELECT date FROM power_daily WHERE socket_id=%s AND date<%s ORDER BY date DESC"
    d = str(dateYesterday())
    cur.execute(sql, (x, d))
    row = cur.fetchone()
    cur.close()
    return row[0]

#function to save data to date
def saveDate(db, x, d):
    cur = db.cursor()
    sql = "SELECT socket_id, watt_cons FROM power_con WHERE CAST(date_time as DATE)=%s AND socket_id=%s"
    cur.execute(sql, (d, x))
    count = cur.rowcount
    results = cur.fetchall()
    f = 0.000
    for row in results:
        f = f + float(row[1])
    f = (f/count * ((count/60)/60))
    cur.close()
    curinsert = db.cursor()
    sql = "INSERT INTO power_daily(socket_id, watt_cons, date) VALUES (%s, %s, %s)"
    try:
        curinsert.execute(sql, (x, f, d))
        db.commit()
    except Exception as e:
        db.rollback()
    curinsert.close()
    
#function to check if yesterday data is saved
def checkDataDaily(db, x):
    cur = db.cursor()
    sql = "SELECT date FROM power_daily WHERE socket_id=%s AND date=%s"
    d = str(dateYesterday())
    cur.execute(sql, (x, d))
    count = cur.rowcount
    cur.close()
    if count >= 1:
        return False
    else:
        return True

#function to get data from power_con table and save to power_daily table
def getandsaveDataDaily(db, x):
    cur = db.cursor()
    sql = "SELECT socket_id, watt_cons FROM power_con WHERE CAST(date_time as DATE)=%s AND socket_id=%s"
    d = str(dateYesterday())
    cur.execute(sql, (d, x))
    count = cur.rowcount
    results = cur.fetchall()
    f = 0.000
    for row in results:
        f = f + float(row[1])
    if count != 0:
        f = (f/count * ((count/60)/60))
    cur.close()
    curinsert = db.cursor()
    sql = "INSERT INTO power_daily(socket_id, watt_cons, date) VALUES (%s, %s, %s)"
    try:
        curinsert.execute(sql, (x, f, d))
        db.commit()
    except Exception as e:
        db.rollback()
    curinsert.close()


# START
#get db connection
conn = db()
try:
    #check if less than yesterday data is saved
    for x in range(1,6):
        a = checkLastSavedSocket(conn, x)
        a = a + timedelta(days=1)
        d = dateYesterday()
        while a < d:
            saveDate(conn, x, a)
            a = a + timedelta(days=1)
except:
    print "Error in saving less than yesterday data"
try:
    #save yesterday data
    for x in range(1,6):
        if checkDataDaily(conn, x):
            getandsaveDataDaily(conn, x)
    print "Saved"
except:
    print "Error"
# END