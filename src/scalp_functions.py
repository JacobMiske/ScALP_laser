# Legacy code
import time

def bitstring_to_bytes(s):
  v = int(s, 2)
  b = bytearray()
  while v:
    b.append(v & 0xFF)
    v >>= 8
    return bytes(b[::-1])


def set_int_to_DAC():
    
  for i in range(17, 4000, 1):
    val = int(i) + 4096
    binary_val = f'{val:016b}'
    # hex_val = binToHexa(binary_val)
    res = bitstring_to_bytes(binary_val)
    hex1 = hex(int(binary_val[0:8], 2))
    print(hex1)
    print(type(hex1))
    hex2 = hex(int(binary_val[8:16], 2))
    print(type(int(hex2, 16)))
    print(type(0x30))
    hex1 = int(hex1, 16)
    hex2 = int(hex2, 16)
    spi1.writebytes([hex1, hex2])
    spi2.writebytes([hex1, hex2])
    time.sleep(0.005)
  
  for i in range(1000, 17, -1):
    val = int(i) + 12288
    binary_val = f'{val:016b}'
    # hex_val = binToHexa(binary_val)
    res = bitstring_to_bytes(binary_val)
    hex1 = hex(int(binary_val[0:8], 2))
    print(hex1)
    hex2 = hex(int(binary_val[8:16], 2))
    print(hex2)
    #spi1.writebytes([hex1, hex2])
    time.sleep(0.005)