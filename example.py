from microserial.microport import MicroPort
from microserial.api import Cmd, Param, DataType
from microserial.payload import create_payload

PORT = 'COM14' #change this to suit your system

def example1(userial):
    payload = create_payload(Cmd.READ, Param.ADC, DataType.D_NONE)
    userial.write(payload)
    resp = userial.read_chars()
    print(resp)

if __name__ == '__main__':
    userial = MicroPort(PORT)
    example1(userial)