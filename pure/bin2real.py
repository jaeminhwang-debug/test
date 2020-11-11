from ctypes import LittleEndianStructure, byref, sizeof, string_at
from ctypes import create_string_buffer, c_uint, c_ushort
from ctypes import cast, pointer, POINTER

class BinStructure(LittleEndianStructure):
    """
    Define your structure here
    """
    _fields_ = [
        ('use22bits', c_uint, 22),
        ('use10bits', c_uint, 10),

        ('', c_ushort, 7),
        ('use2bits', c_ushort, 2),
        ('', c_ushort, 4),
        ('use3bits', c_ushort, 3),
    ]

def to_structure(buf, unit_size, ctype):
    res = []
    count = int(len(buf) / unit_size)
    for i in range(0, count):
        str_buf = create_string_buffer(buf[i * unit_size : i * unit_size + unit_size])
        st = cast(pointer(str_buf), POINTER(ctype)).contents
        res.append(st)
    return res

# Test code
if __name__ == '__main__':

    # Read the sample file
    f = open('sample.bin', 'rb')
    bin_buf = f.read()
    f.close()

    # Convert binary to real value
    sts = to_structure(bin_buf, 6, BinStructure)
    for i, st in enumerate(sts):
        print('[%d] use22bits: %#x, use10bits: %#x, use2bits: %#x, use3bits: %#x' % (
            i, st.use22bits, st.use10bits, st.use2bits, st.use3bits))