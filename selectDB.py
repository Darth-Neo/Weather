#!/usr/bin/python

import sqlite3

def determineTables(conn):
    print("Tables...")

    # Determine Table Names
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    for x in cursor.fetchall():
        print("%s" % x) 

def printTemperatures(conn):

    ins = "select * from temperature_temperature"
    cursor = conn.execute(ins)
    
    for row in cursor:
       print("ID = %s\tReadingDateTime = %s\tTempC = %s\tTempf = %s\t Humidity = %s" % 
            (row[0], row[1], row[2], row[3], row[4])) 

def getID(conn):
    ins = "select max(id) from temperature_temperature"
    cursor = conn.execute(ins)

    #data = int(cursor.fetchone())
    #print ("%s" % data)

    for row in cursor:
	id = int(row[0])
        print ("%s" % row[0])
        break
    return id

def insertTemperature(conn):
    # 2015-02-07 22:15:01 22.20*C 71.96*f 50.80% (edit)

    id = getID(conn) + 1
    dtMessage = "2015-02-07 23:00:00" 
    temperature = "22.20*C"
    f = "71.96*f"
    humidity = "50.80%"

    qs = "insert into temperature_temperature (id, ReadingDateTime, TempC, TempF, Humidity) values (%d, '%s', '%s', '%s', '%s')" % (id, dtMessage, temperature, f, humidity)
    print qs

    cursor = conn.execute(qs)

    conn.commit()

if __name__ == "__main__":
    conn = sqlite3.connect('/home/pi/rpipy/src/Weather.db')

    print "Opened database successfully";

    getID(conn)

    #determineTables(conn)

    insertTemperature(conn)

    printTemperatures(conn)



