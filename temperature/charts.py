#!/usr/bin/env python
#
# __author__ = 'james.morris'
#
import os
import os.path
import time
import random
import sqlite3
from datetime import datetime, date, time, timedelta

import django

from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib.dates import DateFormatter

from Logger import *
logger = setupLogging(__file__)
logger.setLevel(DEBUG)


def existsFile(file_path):
    print(os.getcwd())

    if os.path.isfile(file_path):
        return True
    else:
        return False


def getReadings(con=None):

    if con is None:

        file_path = os.getcwd() + os.sep + u"Weather"

        if existsFile(file_path):
            con = sqlite3.connect(file_path)
        else:
            logger.error(u"File not found - %s" % file_path)

    sel = u"select ReadingDateTime, TempF, Humidity from temperature_temperature order by id desc"

    cursor = conn.execute(sel)

    listRows = list()
    for row in cursor:
        listRows.append([x for x in row])

    return listRows


def simple(request):

    response = None
    strDT = None
    w = list()
    x = list()
    y = list()
    z = list()

    now = datetime.now()

    lr = getReadings()

    for wl in lr:

        try:
            strDT = wl[0][:-1]
            strDT = strDT[0:6] + u" 2015" + strDT[7:]
            dt = datetime.strptime(strDT, u'%b %d %Y %I:%M %p')

        except Exception:
            try:
                # 2015-02-07 23:00:00
                dt = datetime.strptime(strDT, u'%Y-%b-%d %I:%M:%S')

            except Exception, msg:
                logger.error(u"Error %s" % msg)

        try:
            td = now - dt
            tdm = td.seconds / 60.0

            strTempF = wl[1][:-2]
            tf = float(strTempF)
            hm = wl[2][:-1]
            if wl[3] is None:
                br = 0
            elif isinstance(wl[3], str) or isinstance(wl[3], unicode):
                br = float(wl[3]) / 100.0

            # logger.info(u"%s\t%d\t%d\t%d" % (dt, tf, hm, br))
            logger.info(u"%s\t%d\t%d\t%d" % (dt, tf, hm))

            x.append(dt)
            y.append(tf)
            z.append(hm)
            # w.append(br)
        except Exception, msg:
            logger.debug(u"%s" % msg)

    try:
        fig = Figure()
        ax = fig.add_subplot(111)

        ax.plot(x, y, u"g^")
        ax.plot(x, z, u"ro")
        ax.plot(x, z, u"ro")
        # ax.plot(x, w, u"ro")
        ax.plot(x, w, u"ro")

        ax.xaxis.set_major_formatter(DateFormatter(u'%b %d %Y %I:%M %p'))
        fig.autofmt_xdate()

        canvas = FigureCanvas(fig)

        response = django.http.HttpResponse(content_type=u'image/png')

        canvas.print_png(response)

    except Exception, msg:
        logger.warn(u"%s" % msg)

    return response


if __name__ == "__main__":

    home = os.getcwd()

    conn_str = home + os.sep + "Weather.db"

    conn = sqlite3.connect(conn_str)
