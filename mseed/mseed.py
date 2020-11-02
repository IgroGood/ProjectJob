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

from mseed.libmseed import LibMSEED
import matplotlib.pyplot as plt
import numpy as np

def isMSEED(filename):
    '''Check whether filename is a valid miniseed file'''
    __libmseed__=LibMSEED()
    return __libmseed__.isMSEED(filename)

def readMSEED(filename):
    '''Reads traces from a filename
    returns list of lists containing header dictionary and ndarray of samples
    for each trace in a file
    '''
    __libmseed__=LibMSEED()
    return __libmseed__.readMSTraces(filename)

def readHeaderOnly(filename):
    '''Reads headers only without reading data samples'''
    __libmseed__=LibMSEED()
    return __libmseed__.readMSHeader(filename)

def getStartAndEndTime(filename):
    '''Returns record's start and end time as instances of UTCDateTime class'''
    __libmseed__=LibMSEED()
    return __libmseed__.getStartAndEndTime(filename)

def plotTraces(filename):
    '''Plots all traces in a filename'''
    if isMSEED(filename):
        traces=readMSEED(filename)
        StartTime=getStartAndEndTime(filename)[0]

        timeAndDataArray=[{'time': np.arange(0,len(data))*1/(header['samprate']), #Time vector
                           'samples' : data,                                      #Data samples
                           'header' : header}                                     #Header dictionary
                           for [header,data] in traces]


        for channel in timeAndDataArray:
            plt.plot(channel['time'],channel['samples'],alpha = 0.9,label=channel['header']['channel'].decode())

        plt.title(filename)
        plt.xlabel('Seconds from %s' % StartTime) #Time vector is relative, so add start time mark
        plt.ylabel('Samples')

        plt.gcf().autofmt_xdate()
        plt.gcf().canvas.set_window_title('Miniseed traces plot')

        plt.grid(True)
        plt.tight_layout()
        plt.legend()
        plt.show()
