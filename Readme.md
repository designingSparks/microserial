# Introduction

Designed for communication with a microcontroller in mind, this package takes a leaf out of the REST API playbook, allowing commands to be sent in a similar fashion to a REST API.

Quick start:

```python
from microserial.microport import MicroPort
from microserial.api import Cmd, Param, DataType
from microserial.payload import create_payload

userial = MicroPort('COM14')
payload = create_payload(Cmd.READ, Param.ADC, DataType.D_NONE)
userial.write(payload)
resp = userial.read_chars()
print(resp)
```

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





# Example usage

# Notes on the serial port

```ser.readline()``` is slow.
It appears that it spends a lot of time waiting
See this ref: https://stackoverflow.com/questions/47235381/python-serial-read-is-extremely-slow-how-to-speed-up

