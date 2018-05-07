from __future__ import print_function
import csv
import MySQLdb as mysql

def db_connection():
    db = mysql.connect(host="localhost", user="root", passwd="", db="powerboard")
    return db

def getUniqAppliance(db):
    cur = db.cursor()
    sql = 'SELECT DISTINCT train_appliance FROM power_con WHERE train_appliance IS NOT NULL;'
    cur.execute(sql)
    count = cur.rowcount
    results = cur.fetchall()
    cur.close()
    return (count, results)

def getConAppliance(db, app):
    cur = db.cursor()
    sql = "SELECT watt_cons FROM power_con WHERE train_appliance=%s"
    cur.execute(sql, (app,))
    count = cur.rowcount
    results = cur.fetchall()
    cur.close()
    return (count, results)

db = db_connection()
app_list = [x[0] for x in getUniqAppliance(db)[1]]

for i in app_list:
    watt_consumed = getConAppliance(db, i)
    watt = [float(x[0]) for x in watt_consumed[1]]
    watt_start = 0
    print(i, watt_consumed[0])