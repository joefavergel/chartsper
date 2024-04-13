def read_varlen(data):
    NEXTBYTE = 1
    value = 0
    while NEXTBYTE:
        chr = next(data)
        # is the hi-bit set?
        if not (chr & 0x80):
            # no next BYTE
            NEXTBYTE = 0
        # mask out the 8th bit
        chr = chr & 0x7f
        # shift last value up 7 bits
        value = value << 7
        # add new value
        value += chr
    return value

def write_varlen(value):
    res = bytes()
    while True:
        byte = value & 0x7F
        value >>= 7
        if value:
            byte |= 0x80
        res += bytes([byte])
        if not value:
            break
    return res
