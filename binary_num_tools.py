'''
https://realpython.com/python-bitwise-operators/
https://gist.github.com/cincodenada/6557582
https://www.falatic.com/index.php/108/python-and-bitwise-rotation
'''


def bnot(val, len=8):
    ''' Run Binary NOT on byte value '''
    return ~val & 2**len

def bshl(val, num, len=8):
    return val << num & 2**len-1

def bshr(val, num, len=8):
    return val >> num & 2**len-1

def brol(val, num, len=8):
    return (val << num % len) & (2**len-1) | \
        ((val & (2**len-1)) >> (len-(num % len)))

def bror(val, num, len=8):
    return ((val & (2**len-1)) >> num % len) | \
        (val << (len-(num % len)) & (2**len-1))

def binary(num, length=8):
    ''' Print Binary string withe leading zeros '''
    return format(num, '#0{}b'.format(length + 2))

def get_bit(value, bit_index):
    return value & (1 << bit_index)

def clear_bit(value, bit_index):
    return value & ~(1 << bit_index)

def toggle_bit(value, bit_index):
    return value ^ (1 << bit_index)