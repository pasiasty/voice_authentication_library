__author__ = 'mariusz'

class U2Decoder:

    @classmethod
    def merge_bytes(cls, arr):
        bin_arr = [format(ord(el), '#010b')[2:] for el in arr]
        return ''.join(bin_arr)

    @classmethod
    def inverse(cls, arg):
        max = 2**len(arg)-1
        act = int('0b' + arg, 2)
        val = max - act
        formatter = '#0' + str(len(arg)+2) + 'b'
        return format(val, formatter)[2:]

    @classmethod
    def increment(cls, arg):
        val = int('0b' + arg, 2) + 1
        formatter = '#0' + str(len(arg)+3) + 'b'
        return format(val, formatter)[2:]

    @classmethod
    def is_negative(cls, arg):
        return arg[0] == '1'

    @classmethod
    def decode_u2(cls, arr):
        val = cls.merge_bytes(arr)
        sign = 1

        if cls.is_negative(val):
            val = cls.inverse(val)
            val = cls.increment(val)
            sign = -1

        return (int('0b' + val, 2) * sign)/65536.

