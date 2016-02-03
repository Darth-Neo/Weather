#!/usr/bin/env python
import os
import sqlite3
from Logger import *

logger = setupLogging(__file__)
logger.setLevel(DEBUG)

months = ["Jan%", "Feb%", "Mar%", "Apr%", "May%", "Jun%", "Jul%", "Aug%", "Sep%", "Oct%", "Nov%", "Dec%"]

def countReadings(conn):

    c = conn.cursor()
    n = 0

    for month in months:
        t = ("%s" % month, )
        cnt = "select count(*) from temperature_temperature where ReadingDateTime like ?"

        c.execute(cnt, t)

        logger.info("Month[%2d]: %s\t%s" % (n, month[:-1], c.fetchone()))
        n += 1


def trimReadings(conn, month):
    logger.info("Trim %s%s" % (month[:-1], os.linesep)

    c = conn.cursor()

    t = ("%s" % month, )

    trim = u"delete from temperature_temperature where ReadingDateTime like ?"

    c.execute(trim, t)

if __name__ == u"__main__":
    home = os.getcwd()

    conn_str = home + os.sep + u"Weather.db"
    conn = sqlite3.connect(conn_str)

    tm = months[9] 

    trimReadings(conn, tm)

    countReadings(conn)


