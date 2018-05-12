from __future__ import print_function
import MySQLdb as mysql
from datetime import datetime, timedelta
import time as tm
#function to get mysql connection
def dbConn():
    db = mysql.connect(host="localhost", user="power", passwd="board", db="powerboard")
    return db
def getPowerConsumed(db, x, d):
    cur = db.cursor()
    sql = "SELECT watt_cons FROM power_con WHERE CAST(date_time as DATE)=%s and socket_id=%s"
    cur.execute(sql, (d, x))
    count = cur.rowcount
    results = cur.fetchall()
    f = 0.000
    for row in results:
        f = f + float(row[0])
    f = (f/count * ((count/60)/60))
    cur.close()
    curinstert = db.cursor()
    sql = "SELECT INTO power_daily(socket_id, watt_cons, date) VALUES (%s, %s, %s)"
    try:
        curinsert.execute(sql, (x, f, d))
        db.commit()
    except Exception as e:
        db.rollback()
        print(e)
    curinsert.close()


x = raw_input('Enter date: ')
d = datetime.strptime(x, '%Y-%m-%d').date()
db = dbConn()
for i in range(1,6):
    getPowerConsumed(db, i, d)
