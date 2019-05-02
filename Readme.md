# Introduction

Designed for communication with a microcontroller in mind, this package takes a leaf out of the REST API playbook, allowing commands to be sent in a similar fashion to a REST API.

**Quick start:**

Define an api.py file as follows:

```python
BASE_VAL = 0

class Cmd(Enum):
    READ = BASE_VAL
    WRITE = auto()

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
```

Then use your api and the microserial package to send commands and receive responses as follows:

```python
from microserial.microport import MicroPort
from api import Api

userial = MicroPort('COM14', Api)
cmd = userial.send_cmd('READ', 'ADC', 'D_NONE')
print(cmd)
resp = userial.read_chars()
print(resp)
```

For a complete example, see the examples directory.

# API structure

The api is defined in api.py.


# Payload structure

The payload is a byte array in the following format:

- Byte 0 = command
- Byte 1 = parameter
- Byte 2 = data type
- Bytes 3..n-1 = optional data bytes if data type is not D_NONE.
- Byte n = '\n'

Commands sent from the computer to the microcontroller are terminated with '\n'.

*Why use an EOT byte?*
This makes reading the response from the microcontroller easier if there are preceding messages terminated with '\n'.


# Response from microcontroller

Example microcontroller response
'Reading ADC\nValue: 1024\n111\nx04'
What does the API look like?

# Notes on the python serial package.

```Serial.readline()``` is slow and spends a lot of time waiting.
For this reason, microport.read_chars() uses Serial.read_all(), which immediately gets all characters that are in the buffer. As soon as the EOT byte has been detected, the response is processed.

See this ref: https://stackoverflow.com/questions/47235381/python-serial-read-is-extremely-slow-how-to-speed-up


