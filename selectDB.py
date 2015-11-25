#!/usr/bin/env python
import os
import sqlite3
from Logger import *

logger = setupLogging(u"tft_ip")
logger.setLevel(DEBUG)


def determineTables(conn):
    print(u"Tables...")

    # Determine Table Names
    cursor = conn.cursor()
    cursor.execute(u"SELECT name FROM sqlite_master WHERE type='table';")
    for x in cursor.fetchall():
        print(u"%s" % x)


def fixReadings():
    """
    select ReadingDateTime, max(TempF) from temperature_temperature;
    select ReadingDateTime, min(TempF) from temperature_temperature;
    """

    conn_str1 = home + os.sep + u"Weather.db"
    conn1 = sqlite3.connect(conn_str1)

    conn_str2 = home + os.sep + u"Weather.db"
    conn2 = sqlite3.connect(conn_str2)

    cast1 = u"select TempF, cast(TempF as Real) from temperature_temperature where TempF like'2%';"
    cast2 = u"update temperature_temperature set TempF = cast(TempF as Real) * 1.8 + 32.0 where TempF like'2%';"

    del1 = u"delete from temperature_temperature where ReadingDateTime like '7%'"

    sel1 = u"select ReadingDateTime, TempF, Humidity, Barometer from temperature_temperature"
    sel2 = u"where ReadingDateTime like '7%'"

    qs1 = u"insert into temperature_temperature (ReadingDateTime, TempF, Humidity, Barometer) values "
    # qs2 = u"('%s', '%3.1f*F', '%0.2f%%', '%3.2f')" % (dtMessage, Tempf, humidity, barometer)

    cursor = conn.execute(sel1)

    for row in cursor:
        print(u"ReadingDateTime = %s\tTempf = %s\tHumidity = %s\tBarometer = %s" %
            (row[0], row[1], row[2], row[3]))


def printReadings(conn):
    sel = u"select ReadingDateTime, TempF, Humidity, Barometer from temperature_temperature order by id desc"

    cursor = conn.execute(sel)

    for row in cursor:
        print(u"ReadingDateTime = %s\tTempf = %s\tHumidity = %s\tBarometer = %s" %
              (row[0], row[1], row[2], row[3]))


if __name__ == u"__main__":

    home = os.getcwd()

    conn_str = home + os.sep + u"Weather.db"
    conn = sqlite3.connect(conn_str)

    print(u"Opened database successfully")

    # determineTables(conn)

    printReadings(conn)

