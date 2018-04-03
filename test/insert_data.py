import MySQLdb as mysql
from datetime import datetime, timedelta
import time
import decimal
import random

#function to return date Yesterday string
def dateYesterday():
    return str((datetime.today() - timedelta(days=1)).date())

#function to get mysql connection
def dbConn():
    db = mysql.connect(host="localhost", user="root", passwd="", db="powerboard")
    return db
def randDecimal():
    return float(decimal.Decimal(random.randrange(10000))/100)

conn = dbConn()
from_input = raw_input("Input from date: ")
to_input = raw_input("Input to date: ")
try:
    date_from = datetime.strptime(from_input, '%Y-%m-%d %H:%M:%S')
    date_to = datetime.strptime(to_input, '%Y-%m-%d %H:%M:%S')
    while date_from < date_to:
        cur = conn.cursor()
        sql = "INSERT INTO power_con(socket_id, watt_cons, date_time) VALUES (1, %s, %s), (2, %s, %s), (3, %s, %s), (4, %s, %s), (5, %s, %s)"
        cur.execute(sql, (randDecimal(), date_from, randDecimal(), date_from, randDecimal(), date_from, randDecimal(), date_from, randDecimal(), date_from))
        conn.commit()
        cur.close()
        print "Dumping data from ", date_from
        date_from = date_from + timedelta(hours=1)
        time.sleep(.300)
    print "Nothing to dump"
except Exception as e:
    print e