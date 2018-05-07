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
file = open('test.csv', 'wb')
writer = csv.writer(file)
writer.writerow(['1s', '2s', '3s', '4s', '5s', '6s', '7s', '8s', '9s', '10s', 'appliance'])
app_list = [x[0] for x in getUniqAppliance(db)[1]]

for i in app_list:
    watt_consumed = getConAppliance(db, i)
    watt = [float(x[0]) for x in watt_consumed[1]]
    watt_start = 0
    # print(i, watt_consumed[0])

    for ii in range(watt_consumed[0]/10):
        row = watt[watt_start:watt_start+10]
        row.append(i)
        # print(row)
        writer.writerow(row)
        watt_start += 10