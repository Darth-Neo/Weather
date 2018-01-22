#!/usr/bin/env python
import os
import datetime
import sqlite3

from Logger import *

logger = setupLogging(__file__)
logger.setLevel(INFO)

months = [u"Dec", u"Jan", u"Feb", u"Mar", u"Apr", u"May", u"Jun", u"Jul",
          u"Aug", u"Sep", u"Oct", u"Nov", u"Dec", u"Jan"]


def trimReadings(conn, id):

    logger.info(u"id : {}".format(id))

    trim = u"delete from temperature_temperature where id < ?"
    logger.info(u"trim  : {}".format(trim))

    c = conn.cursor()
    c.execute(trim, (id,))
    c.close()


def check_effect(conn):

    query = u"select min(id) from temperature_temperature"
    logger.info(u"query : {}".format(query))

    c = conn.cursor()
    c.execute(query)
    id = c.fetchone()[0]
    c.close()

    get_fields(conn, id)


def get_fields(conn, id):

    query = u"select * from temperature_temperature where id=?"
    logger.debug(u"query : {}".format(query))

    c = conn.cursor()
    c.execute(query, (id, ))
    fields = c.fetchone()
    c.close()

    for n, x in enumerate(fields):
        logger.info(u"  {} : {}".format(n, x))


def get_id(conn, year, month):
    y = year - 1
    m = months[month]

    query = u"select min(id) from temperature_temperature where ReadingDateTime like '{} {}%'".format(y, m)

    logger.debug(u"query : {}".format(query))

    c = conn.cursor()
    c.execute(query)
    id = c.fetchone()[0]
    c.close()

    return id


if __name__ == u"__main__":
    home = os.getcwd()

    logger.info(u"Current date and time: %s" % datetime.datetime.now())

    year = int(datetime.date.today().strftime(u"%Y"))
    month = int(datetime.date.today().strftime(u"%m"))

    logger.info(u"Year  : %d" % year)
    logger.info(u"Month : %s" % months[month])

    conn_str = u".%sWeather.db" % os.sep
    with sqlite3.connect(conn_str) as conn:

        # Get ID
        #
        nid = int(get_id(conn, year, month))
        logger.info(u"nid   : {}".format(nid))

        # Get Fields
        #
        get_fields(conn, nid)

        # Trim Database
        #
        trimReadings(conn, nid)


    with sqlite3.connect(conn_str) as conn:

        # Check that it worked!
        #
        check_effect(conn)



