#!/usr/bin/python
import os.path
import sqlite3
from datetime import datetime


def createTable(conn=None):

    sql = u"CREATE TABLE 'temperature_barometer' \
    (`id` INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,\
        `ReadingDateTime` varchar(255) NOT NULL, \
        'TempF' varchar(255) NOT NULL, \
        'Barometer' varchar(255) NOT NULL\
        )"
    cursor = conn.execute(sql)


def existsFile(file_path):

    # print("CWD = %s" % os.getcwd())

    if os.path.isfile(file_path):
        return True
    else:
        return False


def getTemperatures(conn=None):

    if conn is None:
        file_path = u"/home/james.morris/PythonDev/pyrpi/Weather/Weather.db"
        if existsFile(file_path):
            conn = sqlite3.connect(file_path)
        else:
            print(u"File not found - %s" % file_path)

    sel = u"select ReadingDateTime, TempF, Humidity from temperature_temperature order by ReadingDateTime desc"
    cursor = conn.execute(sel)

    listRows = list()
    for row in cursor:

        # print("ID = %s\tReadingDateTime = %s\tTempC = %s\tTempf = %s\t Humidity = %s" %
        #     (row[0], row[1], row[2], row[3], row[4]))

        listRows.append([x for x in row])

    return listRows


def determineTables(conn):
    # Determine Table Names
    cursor = conn.cursor()
    cursor.execute(u"SELECT name FROM sqlite_master WHERE type='table';")
    # print(cursor.fetchall())


def printTemperatures(conn):

    ins = u"select ReadingDateTime, TempF, Humidity from temperature_temperature order by id desc"
    cursor = conn.execute(ins)
    
    for row in cursor:
        print(u"ReadingDateTime = %s\tTempf = %s\t Humidity = %s" %
            (row[0], row[1], row[2]))

if __name__ == u"__main__":
    conn = sqlite3.connect(u'../Weather.db')
    print u"Opened database successfully"

    now = datetime.now()
    print(u"Now: %s" % now)

    lr = getTemperatures()

    x = list()
    x.append(0.0)

    y = list()
    y.append(0.0)

    for wl in lr[0:20]:
        print (u"x : %s" % x)
        strDT = wl[0][:-1]
        print (u"    strDT : %s" % strDT)
        strDT = strDT[0:6] + u" 2015" + strDT[7:]
        dt = datetime.strptime(strDT, u'%b %d %Y %I:%M %p')
        print(u"    dt : %s" % dt)

        td = now - dt
        tdm = td.seconds / 60.0

        print(u"    tdm : %5.2f" % tdm)
        x.append(tdm)

        strTempF = wl[1][:-2]
        tf = float(strTempF)
        print(u"    tf : %3.2f" % tf)
        y.append(tf)

    print(u" %s" % x)
    print(u"  %s" % y)