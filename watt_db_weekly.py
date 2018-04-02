import MySQLdb as mysql
from datetime import datetime, timedelta
import time as tm
import decimal
# DESCRIPTION : AUTOMATE SAVING IN DATABASE WEEKLY
# cron job every minute

#FUNCTIONS

#function to get mysql connection
def dbConn():
    db = mysql.connect(host="localhost", user="root", passwd="", db="powerboard")
    return db

#function to get last week number
def getYesterweek():
    d = datetime.now().date() - timedelta(days=7)
    start = d - timedelta(days=d.weekday())
    end = start + timedelta(days=6)
    return (start, end, (datetime.now() - timedelta(days=7)).isocalendar()[1])

#function to check last date saved in weekly socket
def checkLastSavedSocketWeekly(db, x, w):
    cur = db.cursor()
    sql = "SELECT date_from, date_to, week_number FROM power_weekly WHERE socket_id=%s AND week_number<%s"
    cur.execute(sql, (x, w))
    row = cur.fetchone()
    cur.close()
    return row


#function to check if last week is saved
def checkDataWeekly(db, x, s, e, w):
    cur = db.cursor()
    sql = "SELECT week_number FROM power_weekly WHERE socket_id=%s AND date_from=%s AND date_to=%s AND week_number=%s"
    cur.execute(sql, (x, s, e, w))
    count = cur.rowcount
    cur.close()
    if count >= 1:
        return False
    else:
        return True

#function to save last week data
def getandsaveDataWeekly(db, x, s, e, w):
    cur = db.cursor()
    sql = "SELECT socket_id, watt_cons FROM power_daily WHERE socket_id=%s AND date>=%s AND date<=%s"
    cur.execute(sql, (x, s, e))
    results = cur.fetchall()
    f = 0.0000
    for row in results:
        f = f + float(row[1])
    cur.close()
    curinsert = db.cursor()
    sql = "INSERT INTO power_weekly(socket_id, watt_cons, date_from, date_to, week_number) VALUES (%s, %s, %s, %s, %s)"
    try:
        curinsert.execute(sql, (x, f, s, e, w))
        db.commit()
    except:
        db.rollback()

#START
conn = dbConn()
start, end, week = getYesterweek()
start, end, week = (str(start), str(end), str(week))

try:
    #get socket number 1, 2, 3, 4, 5
    for x in range(1,6):
        ls, le, lw = checkLastSavedSocketWeekly(conn, x, week)
        ls, le, lw = ls + timedelta(days=7), le + timedelta(days=7), lw + 1
        while lw < int(week):
            getandsaveDataWeekly(conn, x, ls, le, lw)
            ls, le, lw = ls + timedelta(days=7), le + timedelta(days=7), lw + 1
except:
    print "Error"

try:
    for x in range(1,6):
        if checkDataWeekly(conn, x, start, end, week):
            getandsaveDataWeekly(conn, x, start, end, week)
except:
    print "Error"
print "SAVED"

#END