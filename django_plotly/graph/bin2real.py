from ctypes import create_string_buffer, cast, pointer, POINTER
from ctypes import LittleEndianStructure, c_uint8, c_uint16, c_uint32, c_uint64
from ctypes import sizeof

class CustomBinStruct:
    """
    This class helps use of binary data.
    Look at below C/C++ example code, it will make the binary data depicted in below data structure.

    <C/C++ example code>
    #pragma pack(push, 1)
    typedef struct {
        unsigned int use22bits : 22;
        unsigned int use10bits : 10;
        unsigned short : 7;
        unsigned short use2bits : 2;
        unsigned short : 4;
        unsigned short use3bits : 3;
    } BinStructure;
    #pragma pack(pop)

    <Data structure made by example code>
    |LSB                                                 MSB|
    |0      21|22     31|32    38|39    40|41    44|45    47|
    |use22bits|use10bits|not used|use2bits|not used|use3bits|
    """

    def __init__(self):
        self._fields = []
        self._fields_buf = []

    def clear_binfield(self):
        self._fields.clear()
        self._fields_buf.clear()

    def append_binfield(self, label, bits):
        self._fields_buf.append((label, bits))
        bits_sum = sum([field[1] for field in self._fields_buf])
        if bits_sum == 8:
            ctype = c_uint8
        elif bits_sum == 16:
            ctype = c_uint16
        elif bits_sum == 32:
            ctype = c_uint32
        elif bits_sum == 64:
            ctype = c_uint64
        else:
            ctype = None
        if ctype:
            for field in self._fields_buf:
                self._fields.append((field[0], ctype, field[1])) 
            self._fields_buf.clear()

    def make_binstruct(self):
        class BinStruct(LittleEndianStructure):
            _pack_ = 1
            _fields_ = self._fields
        self._bs = BinStruct()
        self._unit_size = sizeof(self._bs)
        self._ctype = type(self._bs)

    def read_bin_to_list(self, fpath):

        # Open file
        f = open(fpath, 'rb')
        buf = f.read()
        f.close()

        # Set output list(element: tuple of structure's field values)
        res = []
        count = int(len(buf) / self._unit_size)
        for i in range(0, count):
            str_buf = create_string_buffer(
                        buf[i * self._unit_size : i * self._unit_size + self._unit_size])
            st = cast(pointer(str_buf), POINTER(self._ctype)).contents
            tuple_of_fields = tuple(getattr(st, field[0]) for field in st._fields_)
            res.append(tuple_of_fields)
        return res

    def read_bin_to_dict(self, fpath):

        # Open file
        f = open(fpath, 'rb')
        buf = f.read()
        f.close()

        # Prepare return dictionary(key: field label, value: value list)
        res = {}
        for field in self._ctype._fields_:
            res[field[0]] = []

        # Set value list
        count = int(len(buf) / self._unit_size)
        for i in range(0, count):
            str_buf = create_string_buffer(
                        buf[i * self._unit_size : i * self._unit_size + self._unit_size])
            st = cast(pointer(str_buf), POINTER(self._ctype)).contents
            for field in st._fields_:
                res[field[0]].append(getattr(st, field[0]))

        return res
