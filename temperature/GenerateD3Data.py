#!/usr/bin/env python
""""
Generate D3 Data as needed
"""
# __author__ = 'james.morris'
#
import os
import os.path
import sqlite3
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
                print(u"File not found - %s" % dbFileInput)
                raise IOError
        else:
            if self._existsFile(fileInput):
                self._conn = sqlite3.connect(fileInput)
            else:
                print(u"File not found - %s" % fileInput)
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
                f.write("%s\t%3.2f\t%3.2f\t%3.2f\t%3.2f\t%3.2f\t%3.2f%s" % (k, v[0], v[1], v[2]/10.00,
                                                                          v[3], v[4], v[5]/10.00, os.linesep))

    def _computeValues(self):
        """
        Compute values for the day
        """

        for k, v in self.dl.items():

            minF = 1000
            minH = 1000
            minB = 1000

            maxF = 0
            maxH = 0
            maxB = 0

            for f, h, b in v:
                try:
                    ff = float(f)
                    fh = float(h)
                    if b is None:
                        b = 0.0
                    fb = float(b)

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

        sel1 = u"select ReadingDateTime, TempF, Humidity, Barometer from temperature_temperature "
        sel2 = u" order by ReadingDateTime desc"
        sel = sel1 + sel2

        cursor = self._conn.execute(sel)

        for row in cursor:
            strDT = row[0].rstrip()

            dlp = strDT.split()
            month = dlp[0]
            day = dlp[1]

            strDT = month + u" " + day + u" 2015 " + strDT[7:]

            try:
                dt = datetime.strptime(strDT, u'%b %d %Y %I:%M %p')
            except Exception, msg:
                logger.warn(u"%s" % msg)
                try:
                    dt = datetime.strptime(strDT, u'%b %d %Y %I:%M%p')
                except Exception, msg:
                    logger.warn(u"%s" % msg)
                    try:
                        dt = datetime.strptime(strDT, u'%Y-%m-%d %I:%M:%S')
                    except Exception, msg:
                        logger.error(u"%s" % msg)
                        continue

            y = dt.year
            m = dt.month

            if m < 10:
                m = u"0%s" % m

            d = dt.day
            if d < 10:
                d = u"0%s" % d

            strDate = u"%4s%2s%2s" % (y, m, d)

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

        self._computeValues()

        self._saveDataTSV()


if __name__ == u"__main__":
    gd3d = GenerateD3Data()

    gd3d.generateD3Data()
