import MySQLdb as mysql
from datetime import datetime, timedelta
import time as tm
#function to get mysql connection
def dbConn():
    db = mysql.connect(host="localhost", user="root", passwd="", db="powerboard")
    return db

def getStartandEndWeek(x):
    d = datetime.strptime(x, '%Y-%m-%d').date()
    start = d - timedelta(days=d.weekday())
    end = start + timedelta(days=6)
    return (start, end)
def getWattConsumedDaily(db, x, d):
    cur = db.cursor()
    sql = "SELECT socket_id, watt_cons FROM power_daily WHERE socket_id=%s AND date=%s"
    cur.execute(sql, (x, d))
    results = cur.fetchall()
    f = 0.00
    for row in results:
        f = f + float(row[1])
    cur.close()
    return f
def saveWeekly(db, x, f, dstart, dend, w):
    cur = db.cursor()
    sql = "INSERT INTO power_weekly(socket_id, watt_cons, date_from, date_to, week_number) VALUES (%s, %s, %s, %s, %s)"
    try:
        cur.execute(sql, (x, f, dstart, dend, w))
        db.commit()
    except:
        db.rollback()
    cur.close()

conn = dbConn()
uinput = raw_input('Enter date: ')
d = getStartandEndWeek(uinput)
start = d[0]
end = d[1]
week = start.isocalendar()[1]
start_temp = start

for x in range(1,6):
    f = 0.0000
    while start <= end:
        f = f + getWattConsumedDaily(conn, x, start)
        start = start + timedelta(days=1)
    start = start_temp
    saveWeekly(conn, x, f, start, end, week)
    x = x + 1
print "SAVED"
conn.close()