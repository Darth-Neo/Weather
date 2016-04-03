#!/usr/bin/env python
""""
Generate D3 Data as needed
"""
# __author__ = 'james.morris'
#
import os
import os.path
import sqlite3
import time
from datetime import datetime
import operator
from Logger import *

logger = setupLogging(u"GenerateD3Data")
logger.setLevel(INFO)


class GenerateD3Data(object):
    """
    Generate D3 Data via Javascript
    """

    conn = None
    listRows = None
    file_path = None
    dl = None

    def __init__(self, pathDir=None, fileInput=None, fileOutput=None):

        self.listRows = list()
        self.adt = dict()
        self.dl = dict()

        if pathDir is None:
            pathDir = u"/home/james.morris/PythonDev/Django/Weather"

        db_file = u"Weather.db"
        data_file = u"data.tsv.run"

        if fileInput is None:

            dbFileInput = pathDir + os.sep + db_file

            if self._existsFile(dbFileInput):
                self._conn = sqlite3.connect(dbFileInput)
            else:
                logger.error(u"File not found - %s" % dbFileInput)
                raise IOError
        else:
            if self._existsFile(fileInput):
                self._conn = sqlite3.connect(fileInput)
            else:
                logger.error(u"File not found - %s" % fileInput)
                raise IOError

        if fileOutput is None:
            self.dataFileOutput = pathDir + os.sep + u"Weather" + os.sep + u"static" + os.sep + data_file
        else:
            self.dataFileOutput = fileOutput

    @staticmethod
    def _existsFile(file_path):
        """
        Check if File exists
        :param file_path:
        :return boolean:
        """
        logger.debug(u"CWD : %s" % os.getcwd())

        if os.path.isfile(file_path):
            return True
        else:
            return False

    @staticmethod
    def _fixReading(v):
        newV = 0

        if v < 1.0:
            newV = v * 100.0
        elif v < 10.0:
            newV = v * 10.0
        elif v < 100.0:
            newV = v
        elif v < 1000.0:
            newV = v / 10.0

        return newV

    def _saveDataTSV(self):
        """
        Save Data to load into D3
        """

        sorted_adt = sorted(self.adt.items(), key=operator.itemgetter(0))

        # ----- Note: Must be lower case or javascript will fail ------
        with open(self.dataFileOutput, u"w") as f:
            f.write("date\tTemperature-H\tHumidity-H\tBarometer-H\tTemperature-L\tHumidity-L\tBarometer-L%s"
                    % os.linesep)

            for k, v in sorted_adt:
                v2 = GenerateD3Data._fixReading(v[2])
                v5 = GenerateD3Data._fixReading(v[5])

                vRow = "%s\t%3.2f\t%3.2f\t%3.2f\t%3.2f\t%3.2f\t%3.2f%s" % (k, v[0], v[1], v2,
                                                                           v[3], v[4], v5, os.linesep)

                f.write(vRow)
                logger.debug(u"vRow : %s" % vRow)

    def _computeValues(self):
        """
        Compute values for the day
        """

        for k, v in self.dl.items():

            minF = 1000.0
            minH = 1000.0
            minB = 1000.0

            maxF = 0.0
            maxH = 0.0
            maxB = 0.0

            for f, h, b in v:
                try:
                    ff = float(f); fh = float(h); fb = float(b)

                    if fh < 1.00:
                        continue

                    if b is None:
                        b = 0.0

                    if ff > maxF:
                        maxF = ff
                    if ff < minF:
                        minF = ff

                    if fh > maxH:
                        maxH = fh
                    if fh < minH:
                        minH = fh

                    if fb > maxB:
                        maxB = fb
                    if fb < minB:
                        minB = fb

                    logger.debug(u"-->%s Max \t%3.2f\t%3.2f\t%3.2f" % (k, maxF, maxH, maxB))
                    logger.debug(u"            Min \t%3.2f\t%3.2f\t%3.2f" % (minF, minH, minB))

                except Exception:
                    logger.warn(u"%s" % (Exception.message))

            logger.debug(u"===%s Max \t%3.2f\t%3.2f\t%3.2f" % (k, maxF, maxH, maxB))
            logger.debug(u"            Min \t%3.2f\t%3.2f\t%3.2f" % (minF, minH, minB))

            nl = list()
            nl.append(maxF)
            nl.append(maxH)
            nl.append(maxB)
            nl.append(minF)
            nl.append(minH)
            nl.append(minB)
            self.adt[k] = nl

    def generateD3Data(self):
        """
        Generate D3 Data
        :return:
        """
        strDT = None

        sel1 = u"select ReadingDateTime, TempF, Humidity, Barometer from temperature_temperature "
        sel2 = u" order by id desc"
        sel = sel1 + sel2

        cursor = self._conn.execute(sel)

        n = 0
        for row in cursor:

            if row[0][-1:] == os.linesep:
                strDT = row[0][0:-1]
            else:
                strDT = row[0]

            logger.info(u".%s." % strDT[0:9])
            if strDT[0:9] == u"2016 2015":
                p1 = strDT[0:4]
                p2 = strDT[10:]
                strDT = p1 + u" " + p2

            p3 = strDT[-3:]
            if p3[0] != u" ":
                p4 = strDT[-2:]
                strDT = strDT[:-2] + u" " + p4

            try:
                dt = datetime.strptime(strDT, u'%Y %b %d  %I:%M %p')

                y = dt.year
                m = dt.month
                d = dt.day

                if m < 10:
                    m = u"0%s" % m

                if d < 10:
                    d = u"0%s" % d

                strDate = u"%4s%2s%2s" % (y, m, d)

                logger.debug(u"%s" % strDate)

                strTempF = row[1][:-2]
                strHumidity = row[2][:-2]

                if row[3] is None:
                    strBarometer = 0.0
                else:
                    strBarometer = row[3]

                ct = list()
                ct.append(strTempF)
                ct.append(strHumidity)
                ct.append(strBarometer)

                if strDate in self.dl:
                    self.dl[strDate].append(ct)
                else:
                    nl = list()
                    nl.append(ct)
                    self.dl[strDate] = nl

            except Exception, msg:
                n += 1
                logger.warn(u"%s" % msg)

        self._computeValues()

        self._saveDataTSV()

        logger.warn(u"Errors : %d" % n)

if __name__ == u"__main__":
    gd3d = GenerateD3Data()

    gd3d.generateD3Data()
