from __future__ import print_function
import csv
import MySQLdb as mysql

# function to get a connection to mysql
def db_connection():
    db = mysql.connect(host="localhost", user="power", passwd="board", db="powerboard")
    return db

# function to get the distincts in power table's appliance
def getUniqAppliance(db):
    cur = db.cursor()
    sql = 'SELECT DISTINCT train_appliance FROM power_con WHERE train_appliance IS NOT NULL;'
    cur.execute(sql)
    count = cur.rowcount
    results = cur.fetchall()
    cur.close()
    return (count, results)

# function to get the appliance's wattage consumed from the table
def getConAppliance(db, app):
    cur = db.cursor()
    sql = "SELECT watt_cons FROM power_con WHERE train_appliance=%s"
    cur.execute(sql, (app,))
    count = cur.rowcount
    results = cur.fetchall()
    cur.close()
    return (count, results)

# START
db = db_connection()

# create csv file '''aw_a.csv'''
file = open('appliance_data.csv', 'wb')
writer = csv.writer(file)
writer.writerow(['amps', 'watts', 'appliance'])
app_list = [x[0] for x in getUniqAppliance(db)[1]]

# get the smallest data that was collected to be basis
app_count = []
for i in app_list:
    watt_consumed = getConAppliance(db,i)
    app_count.append(watt_consumed[0])
app_count.sort()
smallest = app_count[0]

# get the query and save to csv file 
for i in app_list:
    watt_consumed = getConAppliance(db, i)
    watt = [float(x[0]) for x in watt_consumed[1]]
    # save the data to csv
    for ii in range(smallest):
        # [amps, watt, appliance]
        row = [watt[i]/220, watt[i]]
        row.append(i)
        writer.writerow(row)

# END