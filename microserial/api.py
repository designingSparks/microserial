'''
Setting '0' as the base makes debugging with a console easier, since it is easier to read alphanumeric chars.
'''
from enum import Enum, auto
BASE_VAL = ord('0') 

#These definitions must also be in console.h
class Cmd(Enum):
    READ = BASE_VAL
    WRITE = auto()
    CALIBRATE = auto()

class Param(Enum):
    DAC1 = BASE_VAL
    DAC2 = auto()
    DAC1_MSD = auto()
    DAC1_LSD = auto()
    ADC = auto()
    PWM_DAC = auto()
    DAC2_MSD = auto()

class DataType(Enum):
    D_NONE = BASE_VAL
    D_INT32 = auto()
    D_STR = auto()