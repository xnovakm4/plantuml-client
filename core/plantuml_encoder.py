import zlib

def encode6bit(b: int) -> str:
    if b < 10:
        return chr(48 + b)
    b -= 10
    if b < 26:
        return chr(65 + b)
    b -= 26
    if b < 26:
        return chr(97 + b)
    b -= 26
    if b == 0:
        return '-'
    if b == 1:
        return '_'
    return '?'

def append3bytes(b1: int, b2: int, b3: int) -> str:
    c1 = b1 >> 2
    c2 = ((b1 & 0x3) << 4) | (b2 >> 4)
    c3 = ((b2 & 0xF) << 2) | (b3 >> 6)
    c4 = b3 & 0x3F
    return encode6bit(c1 & 0x3F) + encode6bit(c2 & 0x3F) + encode6bit(c3 & 0x3F) + encode6bit(c4 & 0x3F)

def encode64(data: bytes) -> str:
    res = ""
    i = 0
    length = len(data)
    while i < length - 2:
        res += append3bytes(data[i], data[i+1], data[i+2])
        i += 3
    if i == length - 2:
        res += append3bytes(data[i], data[i+1], 0)
        res = res[:-1]
    elif i == length - 1:
        res += append3bytes(data[i], 0, 0)
        res = res[:-2]
    return res

def encode_plantuml(text: str) -> str:
    """
    Encodes PlantUML text using zlib deflate and custom base64-like encoding.
    """
    zlibobj = zlib.compressobj(9, zlib.DEFLATED, -zlib.MAX_WBITS)
    compressed = zlibobj.compress(text.encode('utf-8')) + zlibobj.flush()
    return encode64(compressed)
