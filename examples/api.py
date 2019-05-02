'''
Setting '0' as the base makes debugging with a console easier, since it is easier to read alphanumeric chars.
'''
from enum import Enum, auto
BASE_VAL = ord('0') #ascii 48

#These definitions must also be in console.h
class Cmd(Enum):
    READ = BASE_VAL
    WRITE = auto()
    CALIBRATE = auto()

class Param(Enum):
    DAC1 = BASE_VAL
    ADC = auto()

class DataType(Enum):
    D_NONE = BASE_VAL
    D_INT32 = auto()
    D_STR = auto()


class Api():
    cmd = Cmd
    param = Param
    datatype = DataType
