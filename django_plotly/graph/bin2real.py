from ctypes import create_string_buffer, cast, pointer, POINTER

def to_structure_list(buf, unit_size, ctype):
    res = []
    count = int(len(buf) / unit_size)
    for i in range(0, count):
        str_buf = create_string_buffer(buf[i * unit_size : i * unit_size + unit_size])
        st = cast(pointer(str_buf), POINTER(ctype)).contents
        res.append(st)
    return res

def to_structure_dict(buf, unit_size, ctype):

    # Prepare return dictionary(key: field name, value: value list)
    res = {}
    for field in ctype._fields_:
        res[field[0]] = []
    
    # Set value list
    count = int(len(buf) / unit_size)
    for i in range(0, count):
        str_buf = create_string_buffer(buf[i * unit_size : i * unit_size + unit_size])
        st = cast(pointer(str_buf), POINTER(ctype)).contents
        for field in st._fields_:
            res[field[0]].append(getattr(st, field[0]))

    return res

def read_bin_list(fpath, unit_size, ctype):
    f = open(fpath, 'rb')
    bin_buf = f.read()
    f.close()
    return to_structure_list(bin_buf, unit_size, ctype)

def read_bin_dict(fpath, unit_size, ctype):
    f = open(fpath, 'rb')
    bin_buf = f.read()
    f.close()
    return to_structure_dict(bin_buf, unit_size, ctype)

# Test code
from ctypes import LittleEndianStructure, c_uint, c_ushort
class SampleBin(LittleEndianStructure):
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

if __name__ == '__main__':
    st_list = read_bin_list('sample.bin', 6, SampleBin)
    print(st_list)
    st_dict = read_bin_dict('sample.bin', 6, SampleBin)
    print(st_dict)
