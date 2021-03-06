"""
Defines the libmseed structures and blockettes.
Importing libmseed.dll

For libmseed structures lookup libmseed.h in libmseed source
from https://seiscode.iris.washington.edu/projects/libmseed/files
"""

import ctypes as C
import platform
import os
import numpy as np
import sys


#checking platform
if platform.system() in {'Windows'}:
    pass
else:
    raise NotImplementedError('Platform is not supported yet. Sorry...')

#shared library names depending on the platform
#Windows ones
mseedlibnamesWin={'win32':'libmseed32.dll',
                  'win64':'libmseed64.dll'};
#Linux ones goes here
mseedlibnamesLin={'Linux':'libmseed32.so'};
#define library path
libdir=os.path.dirname(__file__);# A directory of running headers.py
#choose proper library filename
mseedlibname = mseedlibnamesWin['win32'] if platform.architecture()[0] in {'32bit'} else mseedlibnamesWin['win32']
libpath=os.path.join(libdir, 'resources', mseedlibname); # library is always on /resources path
#Loading compiled shared library
try:
    clibmseed = C.CDLL(libpath)
except:
    raise ImportError('Error while initializing shared library', libpath, ': {0}'.format(sys.exc_info()[0]))
else:
    print('"libmseed" shared library sucessfully initialised' )

#TODO may cause some problems regard to system architecture. Need to be checked in runtime
#Check this in case of problems first
long_int = C.c_int64
#long_int = C.c_int32


# expected data types for libmseed id: (numpy, ctypes)
DATATYPES = {"a": C.c_char, "i": C.c_int32, "f": C.c_float, "d": C.c_double}
SAMPLESIZES = {'a':1, 'i':4, 'f':4, 'd':8}

# allowed encodings:
# SEED id: SEED name, SEED sampletype a, i, f or d, default numpy type)}
ENCODINGS = {0: ("ASCII", "a", np.dtype("|S1").type),
             1: ("INT16", "i", np.dtype("int16")),
             3: ("INT32", "i", np.dtype("int32")),
             4: ("FLOAT32", "f", np.dtype("float32")),
             5: ("FLOAT64", "d", np.dtype("float64")),
             10: ("STEIM1", "i", np.dtype("int32")),
             11: ("STEIM2", "i", np.dtype("int32"))}


# SEED binary time
class BTime(C.Structure):
    _fields_ = [
        ('year', C.c_ushort),
        ('day', C.c_ushort),
        ('hour', C.c_ubyte),
        ('min', C.c_ubyte),
        ('sec', C.c_ubyte),
        ('unused', C.c_ubyte),
        ('fract', C.c_ushort),
    ]


# Fixed section data of header
class fsdh_s(C.Structure):
    _fields_ = [
        ('sequence_number', C.c_char * 6),
        ('dataquality', C.c_char),
        ('reserved', C.c_char),
        ('station', C.c_char * 5),
        ('location', C.c_char * 2),
        ('channel', C.c_char * 3),
        ('network', C.c_char * 2),
        ('start_time', BTime),
        ('numsamples', C.c_ushort),
        ('samprate_fact', C.c_short),
        ('samprate_mult', C.c_short),
        ('act_flags', C.c_ubyte),
        ('io_flags', C.c_ubyte),
        ('dq_flags', C.c_ubyte),
        ('numblockettes', C.c_ubyte),
        ('time_correct', C.c_int),
        ('data_offset', C.c_ushort),
        ('blockette_offset', C.c_ushort),
    ]


# Blockette 100, Sample Rate (without header)
class blkt_100_s(C.Structure):
    _fields_ = [
        ('samprate', C.c_float),
        ('flags', C.c_byte),
        ('reserved', C.c_ubyte * 3),
    ]


# Blockette 200, Generic Event Detection (without header)
class blkt_200_s(C.Structure):
    _fields_ = [
        ('amplitude', C.c_float),
        ('period', C.c_float),
        ('background_estimate', C.c_float),
        ('flags', C.c_ubyte),
        ('reserved', C.c_ubyte),
        ('time', BTime),
        ('detector', C.c_char * 24),
    ]


#Blockette 201, Murdock Event Detection (without header)
class blkt_201_s(C.Structure):
    _fields_ = [
        ('amplitude', C.c_float),
        ('period', C.c_float),
        ('background_estimate', C.c_float),
        ('flags', C.c_ubyte),
        ('reserved', C.c_ubyte),
        ('time', BTime),
        ('snr_values', C.c_ubyte * 6),
        ('loopback', C.c_ubyte),
        ('pick_algorithm', C.c_ubyte),
        ('detector', C.c_char * 24),
    ]


#Blockette 300, Step Calibration (without header)
class blkt_300_s(C.Structure):
    _fields_ = [
        ('time', BTime),
        ('numcalibrations', C.c_ubyte),
        ('flags', C.c_ubyte),
        ('step_duration', C.c_uint),
        ('interval_duration', C.c_uint),
        ('amplitude', C.c_float),
        ('input_channel', C.c_char * 3),
        ('reserved', C.c_ubyte),
        ('reference_amplitude', C.c_uint),
        ('coupling', C.c_char * 12),
        ('rolloff', C.c_char * 12),
    ]


# Blockette 310, Sine Calibration (without header)
class blkt_310_s(C.Structure):
    _fields_ = [
        ('time', BTime),
        ('reserved1', C.c_ubyte),
        ('flags', C.c_ubyte),
        ('duration', C.c_uint),
        ('period', C.c_float),
        ('amplitude', C.c_float),
        ('input_channel', C.c_char * 3),
        ('reserved2', C.c_ubyte),
        ('reference_amplitude', C.c_uint),
        ('coupling', C.c_char * 12),
        ('rolloff', C.c_char * 12),
    ]


#Blockette 320, Pseudo-random Calibration (without header)
class blkt_320_s(C.Structure):
    _fields_ = [
        ('time', BTime),
        ('reserved1', C.c_ubyte),
        ('flags', C.c_ubyte),
        ('duration', C.c_uint),
        ('ptp_amplitude', C.c_float),
        ('input_channel', C.c_char * 3),
        ('reserved2', C.c_ubyte),
        ('reference_amplitude', C.c_uint),
        ('coupling', C.c_char * 12),
        ('rolloff', C.c_char * 12),
        ('noise_type', C.c_char * 8),
    ]


#Blockette 390, Generic Calibration (without header)
class blkt_390_s(C.Structure):
    _fields_ = [
        ('time', BTime),
        ('reserved1', C.c_ubyte),
        ('flags', C.c_ubyte),
        ('duration', C.c_uint),
        ('amplitude', C.c_float),
        ('input_channel', C.c_char * 3),
        ('reserved2', C.c_ubyte),
    ]


#Blockette 395, Calibration Abort (without header)
class blkt_395_s(C.Structure):
    _fields_ = [
        ('time', BTime),
        ('reserved', C.c_ubyte * 2),
    ]


#Blockette 400, Beam (without header)
class blkt_400_s(C.Structure):
    _fields_ = [
        ('azimuth', C.c_float),
        ('slowness', C.c_float),
        ('configuration', C.c_ushort),
        ('reserved', C.c_ubyte * 2),
    ]


#Blockette 405, Beam Delay (without header)
class blkt_405_s(C.Structure):
    _fields_ = [
        ('delay_values', C.c_ushort * 1),
    ]


#Blockette 500, Timing (without header)
class blkt_500_s(C.Structure):
    _fields_ = [
        ('vco_correction', C.c_float),
        ('time', BTime),
        ('usec', C.c_byte),
        ('reception_qual', C.c_ubyte),
        ('exception_count', C.c_uint),
        ('exception_type', C.c_char * 16),
        ('clock_model', C.c_char * 32),
        ('clock_status', C.c_char * 128),
    ]


# Blockette 1000, Data Only SEED (without header)
class blkt_1000_s(C.Structure):
    _fields_ = [
        ('encoding', C.c_ubyte),
        ('byteorder', C.c_ubyte),
        ('reclen', C.c_ubyte),
        ('reserved', C.c_ubyte),
    ]

# Blockette 1001, Data Extension (without header)
class blkt_1001_s(C.Structure):
    _fields_ = [
        ('timing_qual', C.c_ubyte),
        ('usec', C.c_byte),
        ('reserved', C.c_ubyte),
        ('framecnt', C.c_ubyte),
    ]
blkt_1001 = blkt_1001_s


#Blockette 2000, Opaque Data (without header)
class blkt_2000_s(C.Structure):
    _fields_ = [
        ('length', C.c_ushort),
        ('data_offset', C.c_ushort),
        ('recnum', C.c_uint),
        ('byteorder', C.c_ubyte),
        ('flags', C.c_ubyte),
        ('numheaders', C.c_ubyte),
        ('payload', C.c_char * 1),
    ]


# Blockette chain link, generic linkable blockette index
class blkt_link_s(C.Structure):
    pass

# incomplete type has to be defined this way
blkt_link_s._fields_ = [
    ('blkt_type', C.c_ushort), # Blockette type
    ('next_blkt', C.c_ushort), # Offset to next blockette
    ('blktdata', C.POINTER(None)), # Blockette data
    ('blktdatalen', C.c_ushort), # Length of blockette data in bytes
    ('next', C.POINTER(blkt_link_s)),
]
BlktLink = blkt_link_s

class StreamState_s(C.Structure):
    _fields_ = [
        ('packedrecords', long_int), # Count of packed records
        ('packedsamples', long_int), # Count of packed samples
        ('lastintsample', C.c_int), # Value of last integer sample packed
        ('comphistory', C.c_byte), # Control use of lastintsample for compression history
    ]
StreamState = StreamState_s


class MSRecord_s(C.Structure):
    pass

MSRecord_s._fields_ = [
    ('record', C.POINTER(C.c_char)), # Mini-SEED record
    ('reclen', C.c_int), # Length of Mini-SEED record in bytes
    # Pointers to SEED data record structures
    ('fsdh', C.POINTER(fsdh_s)), # Fixed Section of Data Header
    ('blkts', C.POINTER(BlktLink)), # Root of blockette chain
    ('Blkt100', C.POINTER(blkt_100_s)), # Blockette 100, if present
    ('Blkt1000', C.POINTER(blkt_1000_s)), # Blockette 1000, if present
    ('Blkt1001', C.POINTER(blkt_1001_s)), # Blockette 1001, if present
    # Common header fields in accessible form
    ('sequence_number', C.c_int), # SEED record sequence number
    ('network', C.c_char * 11), # Network designation, NULL terminated
    ('station', C.c_char * 11), # Station designation, NULL terminated
    ('location', C.c_char * 11), # Location designation, NULL terminated
    ('channel', C.c_char * 11), # Channel designation, NULL terminated
    ('dataquality', C.c_char), # Data quality indicator
    ('starttime', C.c_longlong), # Record start time, corrected (first sample)
    ('samprate', C.c_double), # Nominal sample rate (Hz)
    ('samplecnt', long_int), # Number of samples in record
    ('encoding', C.c_byte), # Data encoding format
    ('byteorder', C.c_byte), # Byte order of record
    # Data sample fields
    ('datasamples', C.c_void_p), # Data samples, 'numsamples' of type 'sampletype'
    ('numsamples', long_int), # Number of data samples in datasamples
    ('sampletype', C.c_char), # Sample type code: a, i, f, d
    # Stream oriented state information
    ('ststate', C.POINTER(StreamState)), # Stream processing state information
]

MSRecord = MSRecord_s

class MSTrace_s(C.Structure):
    pass

MSTrace_s._fields_ = [
    ('network', C.c_char * 11), # Network designation, NULL terminated
    ('station', C.c_char * 11), # Station designation, NULL terminated
    ('location', C.c_char * 11), # Location designation, NULL terminated
    ('channel', C.c_char * 11), # Channel designation, NULL terminated
    ('dataquality', C.c_char), # Data quality indicator
    ('type', C.c_char), # MSTrace type code
    ('starttime', C.c_longlong), # Time of first sample
    ('endtime', C.c_longlong), # Time of last sample
    ('samprate', C.c_double), # Nominal sample rate (Hz)
    ('samplecnt', long_int), # Number of samples in trace coverage
    ('datasamples', C.c_void_p), # Data samples, 'numsamples' of type 'sampletype'
    ('numsamples', long_int), # Number of data samples in datasamples
    ('sampletype', C.c_char), # Sample type code: a, i, f, d
    ('prvtptr', C.c_void_p), # Private pointer for general use
    ('ststate', C.POINTER(StreamState)), # Stream processing state information
    ('next', C.POINTER(MSTrace_s)), # Pointer to next trace
]
MSTrace = MSTrace_s

class MSTraceGroup_s(C.Structure):
    pass

MSTraceGroup_s._fields_ = [
    ('numtraces', C.c_int), # Number of MSTraces in the trace chain
    ('traces', C.POINTER(MSTrace_s)), # Root of the trace chain
]
MSTraceGroup = MSTraceGroup_s


# Define the high precision time tick interval as 1/modulus seconds */
# Default modulus of 1000000 defines tick interval as a microsecond */
HPTMODULUS = 1000000.0

# Reading Mini-SEED records from files
class MSFileParam_s(C.Structure):
    pass

MSFileParam_s._fields_ = [
  ('fp', C.POINTER(long_int)),
  ('filename', C.c_char * 512),
  ('rawrec', C.c_char_p),
  ('readlen', C.c_int),
  ('readoffset', C.c_int),
  ('packtype', C.c_int),
  ('packhdroffset', C.c_long),
  ('filepos', C.c_long),
  ('filesize', C.c_long),
  ('recordcount', C.c_int),
]
MSFileParam = MSFileParam_s

class U_DIFF(C.Union):
    """
    Union for Steim objects.
    """
    _fields_ = [
        ("byte", C.c_int8 * 4), # 4 1-byte differences.
        ("hw", C.c_int16 * 2), # 2 halfword differences.
        ("fw", C.c_int32), # 1 fullword difference.
    ]

class FRAME(C.Structure):
    """
    Frame in a seed data record.
    """
    _fields_ = [
        ("ctrl", C.c_uint32), # control word for frame.
        ("w", U_DIFF * 14), # compressed data.
    ]


# Declare function of libmseed library, argument parsing
clibmseed.mst_init.argtypes = [C.POINTER(MSTrace)]
clibmseed.mst_init.restype = C.POINTER(MSTrace)

clibmseed.mst_free.argtypes = [C.POINTER(C.POINTER(MSTrace))]
clibmseed.mst_free.restype = C.c_void_p

clibmseed.mst_initgroup.argtypes = [C.POINTER(MSTraceGroup)]
clibmseed.mst_initgroup.restype = C.POINTER(MSTraceGroup)

clibmseed.mst_freegroup.argtypes = [C.POINTER(C.POINTER(MSTraceGroup))]
clibmseed.mst_freegroup.restype = C.c_void_p

clibmseed.msr_init.argtypes = [C.POINTER(MSRecord)]
clibmseed.msr_init.restype = C.POINTER(MSRecord)

clibmseed.ms_readmsr_r.argtypes = [
    C.POINTER(C.POINTER(MSFileParam)), C.POINTER(C.POINTER(MSRecord)),
    C.c_char_p, C.c_int, C.POINTER(long_int), C.POINTER(C.c_int), C.c_short,
    C.c_short, C.c_short]
clibmseed.ms_readmsr_r.restypes = C.c_int

clibmseed.ms_readtraces.argtypes = [
    C.POINTER(C.POINTER(MSTraceGroup)), C.c_char_p, C.c_int, C.c_double,
    C.c_double, C.c_short, C.c_short, C.c_short, C.c_short]
clibmseed.ms_readtraces.restype = C.c_int

clibmseed.ms_readtraces_timewin.argtypes = [
    C.POINTER(C.POINTER(MSTraceGroup)), C.c_char_p, C.c_int, C.c_double,
    C.c_double, long_int, long_int, C.c_short, C.c_short, C.c_short,
    C.c_short]
clibmseed.ms_readtraces_timewin.restype = C.c_int

clibmseed.msr_starttime.argtypes = [C.POINTER(MSRecord)]
clibmseed.msr_starttime.restype = long_int

clibmseed.msr_endtime.argtypes = [C.POINTER(MSRecord)]
clibmseed.msr_endtime.restype = long_int

clibmseed.ms_detect.argtypes = [C.c_char_p, C.c_int]
clibmseed.ms_detect.restype = C.c_int

clibmseed.msr_unpack_steim2.argtypes = [C.POINTER(FRAME), C.c_int,
        C.c_int, C.c_int,
        np.ctypeslib.ndpointer(dtype='int32', ndim=1, flags='C_CONTIGUOUS'),
        np.ctypeslib.ndpointer(dtype='int32', ndim=1, flags='C_CONTIGUOUS'),
        C.POINTER(C.c_int32), C.POINTER(C.c_int32), C.c_int, C.c_int]
clibmseed.msr_unpack_steim2.restype = C.c_int

clibmseed.msr_unpack_steim1.argtypes = [C.POINTER(FRAME), C.c_int,
        C.c_int, C.c_int,
        np.ctypeslib.ndpointer(dtype='int32', ndim=1, flags='C_CONTIGUOUS'),
        np.ctypeslib.ndpointer(dtype='int32', ndim=1, flags='C_CONTIGUOUS'),
        C.POINTER(C.c_int32), C.POINTER(C.c_int32), C.c_int, C.c_int]
clibmseed.msr_unpack_steim2.restype = C.c_int

# tricky, C.POINTER(C.c_char) is a pointer to single character fields
# this is completely differenct to C.c_char_p which is a string
clibmseed.mst_packgroup.argtypes = [ C.POINTER(MSTraceGroup),
    C.CFUNCTYPE(C.c_void_p, C.POINTER(C.c_char), C.c_int, C.c_void_p),
    C.c_void_p, C.c_int, C.c_short, C.c_short, C.POINTER(C.c_int),
    C.c_short, C.c_short, C.POINTER(MSRecord)]
clibmseed.mst_packgroup.restype = C.c_int

clibmseed.msr_addblockette.argtypes = [C.POINTER(MSRecord), C.POINTER(C.c_char),
                                       C.c_int, C.c_int, C.c_int]
clibmseed.msr_addblockette.restype = C.POINTER(BlktLink)

clibmseed.msr_parse.argtypes = [C.POINTER(C.c_char), C.c_int,
                                C.POINTER(C.POINTER(MSRecord)),
                                C.c_int, C.c_int, C.c_int]
clibmseed.msr_parse.restype = C.c_int


PyFile_FromFile = C.pythonapi.PyFile_FromFd
PyFile_FromFile.argtypes = [
    long_int, C.c_char_p, C.c_char_p, C.CFUNCTYPE(C.c_int, long_int)]
PyFile_FromFile.restype = C.py_object


# Python callback functions for C
def __PyFile_callback(f):
    return 1
_PyFile_callback = C.CFUNCTYPE(C.c_int, long_int)(__PyFile_callback)