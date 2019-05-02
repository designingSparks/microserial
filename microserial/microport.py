# coding: utf8
'''
'''
import serial
import time

EOC = '\n' #end of command
EOT = b'\x04' #end of transmission


class MicroPort(serial.Serial):

    def __init__(self, port, baud=115200):
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
        Reads the serial port until the EOT byte is received.
        '''
        try:
            tstart = time.time()
            data = bytes()
            last_char = None
            while EOT not in data: 
                data += self.read_all()
                if time.time() - tstart > timeout:
                    print('Timeout in read_chars_eot')
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


    def flush(self):
        '''
        TODO: Implement command to flush uC command buffer.
        '''
        pass
