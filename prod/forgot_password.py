from external_db import db_connection as db
from datetime import datetime as dt
import time as tm

#function to return date Yesterday string
def timeNow():
    return str(dt.now().replace(microsecond=0))
def getForgotNow(db, now):
    cur = db.cursor()
    sql = "SELECT id FROM forgot_table WHERE time_expire='"+now+"'"
    cur.execute(sql)
    result = cur.fetchall()
    count = cur.rowcount
    cur.close()
    return (count, result)

def deleteForgot(db, id):
    cur = db.cursor()
    sql = "DELETE FROM forgot_table WHERE id="+ str(id)
    cur.execute(sql)
    db.commit()
    cur.close()

# START
while True:
    try:
        conn = db()
        now = timeNow()
        count, result = getForgotNow(conn, now)
        if count > 0:
            for row in result:
                deleteForgot(conn, row[0])
                print "deleted"
        else:
            print now
        conn.close()
        tm.sleep(1)
    except Exception as e:
        print e
        tm.sleep(1)

# END