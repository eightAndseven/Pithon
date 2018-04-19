import MySQLdb as mysql

def db_connection():
    db = mysql.connect(host="localhost", user="root", passwd="", db="powerboard")
    return db