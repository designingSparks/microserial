def print_array(a):
    '''Prints a byte array'''
    output = [hex(byte) for byte in a]  #creates a list
    print(output)

def b_to_list(a):
    '''Convert byte array to list to make printing easier'''
    output = [hex(byte) for byte in a]  #creates a list
    return output

def create_bytearray_str(b):
    '''Converts a bytearray into a string of ints. Elements are space delimited
    '''
    if b is None:
        return None
    s = ''
    for item in b:
        # s += format(item, "02x")
        # s += hex(int(item))
        s += str(int(item))
        s += ' '
        
    return s[:-1]