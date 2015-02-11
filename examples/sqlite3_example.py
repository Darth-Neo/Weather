#!/usr/bin/python

import sqlite3

def determineTables(conn):
    # Determine Table Names
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    print(cursor.fetchall())

def printTemperatures(conn):

    ins = "select * from temperature_temperature"
    cursor = conn.execute(ins)
    
    for row in cursor:
       print("ID = %s\tReadingDateTime = %s\tTempC = %s\tTempf = %s\t Humidity = %s" % 
            (row[0], row[1], row[2], row[3], row[4])) 
if __name__ == "__main__":
    conn = sqlite3.connect('../Weather.db')

    print "Opened database successfully";

    printTemperatures(conn)



