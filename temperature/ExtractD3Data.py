#!/usr/bin/env python
""""
Generate D3 Data as needed
"""
# __author__ = 'james.morris'
#
import os
import operator
from pymongo import *
from datetime import datetime

# import os.path

from Logger import *
logger = setupLogging("ExtractD3Data")
logger.setLevel(INFO)


class ExtractD3Data(object):
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

        self.project = "Weather"
        self.data_file = "data.tsv.run"

        self.client = MongoClient('mongodb://localhost:27017/')
        self.db = self.client["local"]
        self.collection = self.db['Weather']
        self.months = ["Skip", "Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

    def _find_month_index(self, m):
        for n, x in enumerate(self.months):
            if x == m:
                return n
        return None

    def query_aprs(self):
        client = MongoClient('mongodb://localhost:27017/')
        db = client["local"]
        collection = db['Weather']

        c = self.collection.find({'Temperature': {'$exists': 'true'}})

        for x in c:
            try:
                rdt = x['ReadingDateTime'][0:6]
                check_rdt = rdt[:3]
                check_day = rdt[4:6]

                m = self._find_month_index(check_rdt)
                d = check_day

                if m > 2:
                    rd = "2017{:02}{}".format(m, d)
                else:
                    rd = "2018{:02}{}".format(m, d)

                ymd = rd
                temperature = x['Temperature']
                humidity = x['Humidity']

                thn = list([float(temperature), float(humidity), 0])

            except KeyError, msg:
                logger.warn("Key Error: {}".format(msg))
                continue
            except TypeError, msg:
                logger.warn("Type Error: {}".format(msg))
                continue

            if ymd in self.dl:
                self.dl[ymd].append(thn)
            else:
                self.dl[ymd] = list([thn, ])

            logger.info("RDT: {}\t Temperature: {}\t humidity: {}".format(ymd, temperature, humidity))

        self._computeValues()

        self._saveDataTSV()

        pass

    @staticmethod
    def _existsFile(file_path):
        """
        Check if File exists
        :param file_path:
        :return boolean:
        """
        logger.debug("CWD : %s" % os.getcwd())

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
        with open(self.data_file, "w") as f:
            f.write("date\tTemperature-H\tHumidity-H\tTemperature-L\tHumidity-L%s" % os.linesep)

            for k, v in sorted_adt:
                logger.debug("key[%s] = %s" % (k, v))
                v2 = ExtractD3Data._fixReading(v[2])

                vRow = "%s\t%3.2f\t%3.2f\t%3.2f\t%3.2f%s" % (k, v[0], v[1], v2, v[3], os.linesep)

                f.write(vRow)
                logger.debug("vRow : %s" % vRow)

    def _computeValues(self):
        """
        Compute values for the day
        """

        for k, v in self.dl.items():

            minF = 1000.0
            minH = 1000.0

            maxF = 0.0
            maxH = 0.0

            for f, h, b in v:
                try:
                    ff = float(f)
                    fh = float(h)
                    fb = float(b)

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

                    logger.debug("-->%s Max \t%3.2f\t%3.2f" % (k, maxF, maxH))
                    logger.debug("            Min \t%3.2f\t%3.2f" % (minF, minH))

                except Exception, msg:
                    logger.warn("%s" % msg)

            logger.debug("===%s Max \t%3.2f\t%3.2f" % (k, maxF, maxH))
            logger.debug("            Min \t%3.2f\t%3.2f" % (minF, minH))

            nl = list()
            nl.append(maxF)
            nl.append(maxH)
            nl.append(minF)
            nl.append(minH)
            self.adt[k] = nl

    def generateD3Data(self):
        """
        Generate D3 Data
        :return:
        """
        strDT = None

        sel1 = "select ReadingDateTime, TempF, Humidity, Barometer from temperature_temperature "
        sel2 = " order by id desc"
        sel = sel1 + sel2

        cursor = self._conn.execute(sel)

        n = 0
        for row in cursor:

            if row[0][-1:] == os.linesep:
                strDT = row[0][0:-1]
            else:
                strDT = row[0]

            logger.info(".%s." % strDT[0:9])
            if strDT[0:9] == "2016 2015":
                p1 = strDT[0:4]
                p2 = strDT[10:]
                strDT = p1 + " " + p2

            p3 = strDT[-3:]
            if p3[0] != " ":
                p4 = strDT[-2:]
                strDT = strDT[:-2] + " " + p4

            try:
                dt = datetime.strptime(strDT, u'%Y %b %d  %I:%M %p')

                y = dt.year
                m = dt.month
                d = dt.day

                if m < 10:
                    m = "0%s" % m

                if d < 10:
                    d = "0%s" % d

                strDate = "%4s%2s%2s" % (y, m, d)

                logger.debug("%s" % strDate)

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
                logger.warn("%s" % msg)

        self._computeValues()

        self._saveDataTSV()

        logger.warn("Errors : %d" % n)


if __name__ == "__main__":
    gd3d = ExtractD3Data()
    gd3d.query_values()

