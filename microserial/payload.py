'''
Contains functions to create a serial payload for sending to the PSOC5.
'''
from enum import Enum
from microserial.constants import EOC


def create_payload(cmd, fn, dformat, data=None):
    '''
    Create payload to be written to the serial port.
    Order must be the same as in console.c, processCommand()

    payload - (optional) must be a string
    '''
    b = bytearray()
    b.append(cmd.value)
    b.append(fn.value)
    b.append(dformat.value)
    if data is not None:
        d = data.encode() #convert str to utf8 bytearray
        b.extend(d)
    b.append(ord(EOC))
    return b

def create_empty_payload():
    b = bytearray()
    b.append(ord(EOC))