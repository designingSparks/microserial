#Allow running this example directly from inside the examples directory.
import sys
sys.path.insert(0, '../')

from microserial.microport import MicroPort
from api import Api
# from microserial.payload import create_payload

PORT = 'COM14' #change this to suit your system

def example1(mserial):
    mserial.send_cmd('READ', 'ADC', 'D_NONE')
    resp = mserial.read_chars()
    print(resp)

if __name__ == '__main__':
    userial = MicroPort(PORT, Api)
    example1(userial)