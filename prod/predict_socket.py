from __future__ import print_function
from datetime import datetime, timedelta
from external_db import db_connection as db
import boto3
import sys
import time as tm
import numpy as np
import json

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

def saveAppliance(db, t, s):
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
watt_list = list(result[1])
watt_list = [float(x) for x in watt_list]
print(watt_list)
watt_lists = [np.mean(watt_list[:5]), np.mean(watt_list[5:])]
print(watt_list)
predict = {
    'socket' : str(socket),
	'first_ave' : str(watt_lists[0]),
	'second_ave' : str(watt_lists[1]),
    'values' : watt_list
}
client = boto3.client('lambda', 
                    region_name='us-east-1', 
                    aws_access_key_id='XXXXXX', 
                    aws_secret_access_key='XXXXXXXX')
response = client.invoke(
	FunctionName='arn:aws:lambda:us-east-1:497819500052:function:ml-powerboard-py27',
	InvocationType='RequestResponse',
	Payload=json.dumps(predict)
)

predictedlabel = json.loads(response['Payload'].read())['predictedOutput']

saveAppliance(conn, predictedlabel, socket)