#!/usr/bin/env python
import os
import datetime
import sqlite3
from Logger import *

logger = setupLogging(__file__)
logger.setLevel(INFO)

months = [u"Dec%", u"Nov%", u"Oct%", u"Sep%", u"Jul%",
          u"Jun%", u"May%", u"Apr%", u"Mar%", u"Feb%", u"Jan%",]

def countReadings(conn, tcy):
    global months

    c = conn.cursor()

    for n, month in enumerate(tcy):
        t = u"%d%%%s" % (month[0], month[1])
        cnt = u"select count(*) from temperature_temperature where ReadingDateTime like '%s'" % t

        c.execute(cnt)

        nt = u"%d %s" % (month[0], month[1])
        logger.info(u"%s\t%s" % (nt[:-1], c.fetchone()))

if __name__ == u"__main__":
    home = os.getcwd()

    logger.info(u"Current date and time: %s" % datetime.datetime.now())

    year = int(datetime.date.today().strftime(u"%Y"))
    month = int(datetime.date.today().strftime(u"%m"))

    logger.debug(u"Year : %d" % year)
    logger.debug(u"Month : %s" % months[month - 1][:-1])

    lm = list()

    # Go through current year
    ty = [ (year, x) for x in months[12 - month:]]
    cy = [ (year -1, x) for x in months[:12 - month]]
    tcy = ty + cy

    for n, s in enumerate(tcy):
        logger.debug(u"%d %d %s" % (n, s[0], s[1][:-1]))

    conn_str = u"Weather.db"
    conn = sqlite3.connect(conn_str)

    countReadings(conn, tcy)


