#!/usr/bin/env python
import os
import sqlite3
from Logger import *

logger = setupLogging(__file__)
logger.setLevel(DEBUG)


def determineTables(conn):
    logger.debug(u"Tables...")

    # Determine Table Names
    cursor = conn.cursor()
    cursor.execute(u"SELECT name FROM sqlite_master WHERE type='table';")
    for x in cursor.fetchall():
        logger.debug(u"%s" % x)


def fixReadings():
    """
    select ReadingDateTime, max(TempF) from temperature_temperature;
    select ReadingDateTime, min(TempF) from temperature_temperature;
    """

    conn_str1 = home + os.sep + u"Weather.db"
    conn1 = sqlite3.connect(conn_str1)

    conn_str2 = home + os.sep + u"Weather.db"
    conn2 = sqlite3.connect(conn_str2)

    # qs1 = u"insert into temperature_temperature (ReadingDateTime, TempF, Humidity, Barometer) values "
    # qs2 = u"('%s', '%3.1f*F', '%0.2f%%', '%3.2f')" % (dtMessage, Tempf, humidity, barometer)

    cast1 = u"select TempF, cast(TempF as Real) from temperature_temperature where TempF like'2%';"
    cast2 = u"update temperature_temperature set TempF = cast(TempF as Real) * 1.8 + 32.0 where TempF like'2%';"

    del1 = u"delete from temperature_temperature where ReadingDateTime like '7%'"

    sel1 = u"select ReadingDateTime, TempF, Humidity from temperature_temperature"

    upd1 = u"update temperature_temperature set ReadingDateTime = printf('2015 %s', ReadingDateTime);"
    upd2 = u"update temperature_temperature set ReadingDateTime = printf('2016 %s', ReadingDateTime)  where id > 49421;"

    if True:
        cursor = conn.execute(upd1)
        cursor = conn.execute(upd2)
        conn.commit()
    else:
        cursor = conn.execute(sel1)
        for row in cursor:
            if row[0][-1:] == os.linesep:
                row[0] = row[0][:-1]

            logger.debug(u"ReadingDateTime = %s\tTempf = %s\tHumidity = %s" %
                         (row[0], row[1], row[2]))


def printReadings(conn):
    sel = u"select ReadingDateTime, TempF, Humidity from temperature_temperature order by id desc limit 50"

    cursor = conn.execute(sel)

    for row in cursor:
        logger.debug(u"ReadingDateTime = %s\tTempf = %s\tHumidity = %s" %
                     (row[0], row[1], row[2]))


if __name__ == u"__main__":
    home = os.getcwd()

    conn_str = home + os.sep + u"Weather.db"
    conn = sqlite3.connect(conn_str)

    print(u"Opened database successfully")

    # determineTables(conn)
    printReadings(conn)
    # : fixReadings()

    conn.close()
