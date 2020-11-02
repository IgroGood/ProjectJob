from functions import *
import obspy.core.inventory
from obspy.io.xseed import Parser

fileBh = '20201023_0207_AA.UBL.D0.20.BH'
fileSeed = 'DATALESS.D0_UBL.SEED'


dataSeed = Parser(fileSeed)
dataBh = obspy.read(fileBh)

for dataBh_item in dataBh:
    for dataSeed_item in dataSeed.stations[0]:
        #if (dataSeed_item.station_call_letters == dataBh_item.stats['station']):
        changeArrayValues(dataBh_item, 1)
dataBh.plot()