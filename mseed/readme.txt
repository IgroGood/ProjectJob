#-------------------------------------------------------------------
#  Filename: mseed.py
#   Purpose: Miniseed data processing package
#    Author: Yury A. Kolotovichev, based on Lion Krischer, Robert Barsch and Moritz Beyreuther code
#     Email: ykol@nposodis.ru
#
# Copyright (C) 2008-2010 Lion Krischer, Robert Barsch, Moritz Beyreuther
# Ported to Python 3 (>= 3.2) by Yury A. Kolotovichev (ykol@nposodis.ru)
#---------------------------------------------------------------------

"""
Public functions for processing miniseed data
USE:
import mseed.mseed as MSEED
#filename - string containing full path to processing file
filename="D:/Work/PythonExp/mseed/resources/testfiles/geosigtest.msd"

status=MSEED.isMSEED(filename)

data=MSEED.readMSEED(filename)

header=MSEED.readHeaderOnly(filename)

time=MSEED.getStartAndEndTime(filename)

MSEED.plotTraces(filename)
"""