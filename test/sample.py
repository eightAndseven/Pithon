import MySQLdb as mysql
from datetime import datetime as dt

#function to return datenow string
def timeNow():
    return str(dt.now().replace(microsecond = 0))

#function to get mysql connection
def dbConn():
    db = mysql.connect(host="localhost", user="root", passwd="", db="powerboard")
    return db

#start
try:
    conn = dbConn()
    cur = conn.cursor()
    sql = "INSERT INTO power_con(socket_id, watt_cons, date_time) VALUES (%s, %s, %s)"
    cur.execute(sql, (1,0.2313,timeNow()))
    conn.commit()
    conn.close()
except Exception as e:
    print e