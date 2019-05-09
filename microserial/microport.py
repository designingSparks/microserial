# coding: utf8
'''
'''
import serial
import time

EOC = '\n' #end of command
EOT = b'\x04' #end of transmission


class MicroPort(serial.Serial):

    def __init__(self, port, api, baud=115200):
        self.api = api
        try:
            print('Connecting to serial port: {}'.format(port))
            super(MicroPort, self).__init__(port, baud, timeout=0.5,parity=serial.PARITY_NONE)
        except serial.serialutil.SerialException as err:
            print('Serial port error.')
            if "FileNotFoundError" in err.args[0]:
                print('{} does not exist.'.format(port))
            elif "PermissionError" in err.args[0]:
                print('{} currently in use.'.format(port))
        except Exception as ex: #Display information about other exceptions
            template = "An exception of type {0} occurred.  Details:\n{1!r}"
            message = template.format(type(ex).__name__, ex.args[0])
            print(message)
        self.reset_input_buffer()
        self.reset_output_buffer()
    

    def send_cmd(self, cmd_str, param_str, dformat_str, data_str=None):
        payload = self._create_payload(cmd_str, param_str, dformat_str, data_str)
        self.write(payload)
        return payload


    def _create_payload(self, cmd_str, param_str, dformat_str, data_str=None):
        '''
        Create payload to be written to the serial port.
        Order must be the same as in console.c, processCommand()

        data - (optional) must be a string
        '''
        #Get the actual Enum member from the strings
        cmd = self.api.cmd.__members__[cmd_str]
        param = self.api.param.__members__[param_str]
        dformat = self.api.datatype.__members__[dformat_str]

        b = bytearray()
        b.append(cmd.value)
        b.append(param.value)
        b.append(dformat.value)
        if data_str is not None:
            d = data_str.encode() #convert str to utf8 bytearray
            b.extend(d)
        b.append(ord(EOC))
        return b


    def read_nchars(self, min_chars, timeout=0.5):
        '''
        Read a specified number of characters from the serial port. 
        Useful if you know the number of characters to be received, e.g. When only receiving an ACK
        Param:
        min_chars - number of characters to read
        '''
        n = 0
        try:
            tic = time.time()
            while n < min_chars: #Min number of bytes in response
                n = self.inWaiting()
                if time.time() - tic > timeout:
                    print('Timeout in read_chars()')
                    break

            print('Read time: {}'.format(time.time() - tic))
            print('n = {}'.format(n))
            data = self.read(n)
            data = data.decode() #Convert to string, e.g. 'Reading ADC\n107\n020\n'
            print(data)
            data_list = data.split(EOC)

        except Exception as ex:
            template = "An exception of type {0} occurred.  Arguments:\n{1!r}"
            message = template.format(type(ex).__name__, ex.args)
            print(message)
            return None

        else:
            return data_list[:-1] #e.g. ['Reading ADC', '107', '020']


    def read_chars(self, timeout=0.5):
        '''
        Read characters from the serial port until the EOT byte is received.
        '''
        try:
            tstart = time.time()
            data = bytes()
            last_char = None
            while EOT not in data: 
                data += self.read_all()
                if time.time() - tstart > timeout:
                    print('Timeout in read_chars')
                    break

            # print('Read time: {}'.format(time.time() - tstart))
            data = data.decode() #Convert to string, e.g. '151\n\x04'
            data_list = data.split(EOC)

        except Exception as ex:
            template = "An exception of type {0} occurred.  Arguments:\n{1!r}"
            message = template.format(type(ex).__name__, ex.args)
            print(message)
            return None

        else: #no exception
            return data_list[:-1] #Return everything except for EOT


    def read_stream(self, n, timeout=2):
        '''
        After EOT has been received, read n '\n' terminated messages from the serial port.
        Param:
        n - number of samples to read.
        timeout - timeout after the last sample was read.
        '''
        tstart = time.time()
        try:
            tlast = time.time()
            data = bytes()
            num_rx = 0

            while num_rx < n*5:
                char = self.read() #read a single byte to allow testing
                if char != b'':
                    data += char
                    tlast = time.time()
                    num_rx += 1

                if data[-5:] == b'011\n\x04': #end of ACK sequence
                #TODO: Improve the logic
                    print('ACK sequence detected. Dicarding data:')
                    print(data)
                    num_rx = 0
                    data = bytes()
                    tlast = time.time()

                if time.time() - tlast > timeout:
                    print('Timeout in read_stream')
                    break

        except Exception as ex:
            template = "An exception of type {0} occurred.  Arguments:\n{1!r}"
            message = template.format(type(ex).__name__, ex.args)
            print(message)
            return None

        else: #no exception
            # data = data.decode() #Convert to string, e.g. '151\n\x04'
            # data_list = data.split(EOC)
            print(time.time() - tstart)
            return data

    def flush(self):
        '''
        TODO: Implement command to flush uC command buffer.
        '''
        print('Flushing microport input buffer')
        self.write(bytearray(EOT))
        self.reset_input_buffer()
