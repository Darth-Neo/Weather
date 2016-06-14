#!/usr/bin/env python
import os
import sqlite3

from Logger import *
logger = setupLogging(__file__)
logger.setLevel(DEBUG)

months = [u"Jan%", u"Feb%", u"Mar%", u"Apr%", u"May%", u"Jun%", u"Jul%", u"Aug%", u"Sep%", u"Oct%", u"Nov%", u"Dec%"]


def countReadings(conn):

    c = conn.cursor()
    n = 0

    for month in months:
        t = (u"%s" % month, )
        cnt = u"select count(*) from temperature_temperature where ReadingDateTime like ?"

        c.execute(cnt, t)

        logger.info(u"Month[%2d]: %s\t%s" % (n, month[:-1], c.fetchone()))
        n += 1


def trimReadings(conn, month):
    logger.info(u"Trim %s%s" % (month[:-1], os.linesep))

    c = conn.cursor()

    t = (u"%s" % month, )

    trim = u"delete from temperature_temperature where ReadingDateTime like ?"

    c.execute(trim, t)

if __name__ == u"__main__":

    conn_str = u".%sWeather.db" % os.sep

    logger.info(u"Using : %s" % conn_str)
    tm = months[9] 

    with sqlite3.connect(conn_str) as conn:
        # trimReadings(conn, tm)
        countReadings(conn)
    


