from __future__ import print_function
from datetime import datetime, timedelta
from external_db import db_connection as db
import boto3
import sys
import time as tm

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

def saveAppliance(db, t, s)
    cur = db.cursor()
    sql = """UPDATE socket SET appliance=%s WHERE id=%s"""
    cur.execute(sql, (t,s))
    db.commit()

# START
socket = sys.argv[1]

conn = db()
saveAppliance(conn, 'Please wait...', socket)

now = timeNow()
tm.sleep(10)
then = now + timedelta(0,10)

result = getWatt(conn, now, then, socket)
watt_list = result[1]
predict = {}
for i in watt_list:
    predict[str(watt_list.index(i) + 1) + 's'] = str(float(i))

client = boto3.client('machinelearning', 
                    region_name='us-east-1', 
                    aws_access_key_id='XXXXX', 
                    aws_secret_access_key='XXXXXXXX')
response = client.predict(
    MLModelId='ml-kBBGcVrOxIf',
    Record=predict,
    PredictEndpoint='https://realtime.machinelearning.us-east-1.amazonaws.com'
)

predictedlabel = response['Prediction']['predictedLabel']

saveAppliance(conn, predictedlabel, socket)
print('Predicted is ' + response['Prediction']['predictedLabel'])
print(response)