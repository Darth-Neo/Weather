#! /bin/python
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


def existsFile(file_path):
    print os.getcwd()

    if os.path.isfile(file_path):
        return True
    else:
        return False


def getTemperatures(conn=None):

    if conn == None:

        file_path = "/home/james.morris/rpi/Weather/Weather.db"

        if existsFile(file_path):
            conn = sqlite3.connect(file_path)
        else:
            print("File not found - %s" % file_path)

    sel = "select ReadingDateTime, TempF, Humidity from temperature_temperature order by ReadingDateTime desc"
    cursor = conn.execute(sel)

    listRows = list()
    for row in cursor:
        listRows.append([x for x in row])

    return listRows

def simple(request):

    x = list()
    y = list()
    z = list()

    now = datetime.now()

    lr = getTemperatures()

    for wl in lr:

        try:
            strDT = wl[0][:-1]
            strDT = strDT[0:6] + " 2015" + strDT[7:]
            dt = datetime.strptime(strDT, '%b %d %Y %I:%M %p')
        except:
            try:
                #2015-02-07 23:00:00
                dt = datetime.strptime(strDT, '%Y-%b-%d %I:%M:%S')
            except:
                continue

        td = now - dt
        tdm = td.seconds / 60.0

        strTempF = wl[1][:-2]
        tf = float(strTempF)

        hm = wl[2][:-1]

        x.append(dt)
        y.append(tf)
        z.append(hm)

    fig = Figure()
    ax = fig.add_subplot(111)

    ax.plot(x, y, "g^")
    ax.plot(x, z, "ro")

    ax.xaxis.set_major_formatter(DateFormatter('%b %d %Y %I:%M %p'))
    fig.autofmt_xdate()

    canvas = FigureCanvas(fig)

    response = django.http.HttpResponse(content_type='image/png')

    canvas.print_png(response)

    return response