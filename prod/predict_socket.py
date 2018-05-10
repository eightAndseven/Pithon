from __future__ import print_function
from datetime import datetime, timedelta
from external_db import db_connection as db
import boto3
import sys
import time as tm

socket = sys.argv[1]

#function to return datenow string
def timeNow():
    return datetime.now().replace(microsecond = 0)

def getWatt(db, n, t, s):
    cur = db.cursor()
    sql = "SELECT watt_cons FROM power_con WHERE date_time>=%s AND date_time<%s AND socket_id=%s"
    cur.execute(sql, (n,t,s))
    count = cur.rowcount
    results = cur.fetchall()
    cur.close()
    plist = []
    for row in results:
        plist.append(row[0])
    return (count,plist)

now = timeNow()
tm.sleep(10)
then = now + timedelta(0,10)
conn = db()

result = getWatt(conn, now, then, socket)
watt_list = result[1]
predict = {}
for i in watt_list:
    predict[str(watt_list.index(i) + 1) + 's'] = i

print(predict)

