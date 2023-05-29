from Crypto.Util.number import bytes_to_long
from zlib import crc32, adler32

def checksum(value):
    return hex(crc32(value) & 0xffffffff)[2:]

def checksum_adler(value):
    # return hex(adler32(value) & 0xffffffff)[2:]
    return hex(adler32(value))[2:]

H_LEN = 8
ADLER_LEN = 4
CRC_LEN = 4

file1 = open('scrambled1.png','rb').read()
file2 = open('scrambled2.png','rb').read()

magic_chunk = file1[:8]

# IHDR
ihdr_chunk = file1[8:33]
# ihdr_length = ihdr_chunk[:4]
# print(ihdr_length.hex())
# print(ihdr)
# ihdr_crc = ihdr_chunk[-4:]
# print(ihdr_crc.hex())
# print(hex(crc32(ihdr_chunk[4:-4]) & 0xffffffff)[2:]) # chunk type + chunk data
# print(checksum(ihdr_chunk[4:-4])) # chunk type + chunk data

offset = 33
while b'IDAT' in file1[offset: offset+H_LEN]:
    idat_header = file1[offset : offset+H_LEN]
    print(idat_header)
    idat_length = bytes_to_long(idat_header[:4])
    # print(idat_length)
    idat_data = file1[offset+H_LEN : offset+H_LEN+idat_length] # raw data + adler32
    idat_crc32 = file1[offset+H_LEN+idat_length : offset+H_LEN+idat_length+CRC_LEN]
    # print(idat_data)
    deflate = idat_data[0]
    print(hex(deflate)[2:])
    idat_adler32 = idat_data[-ADLER_LEN:]
    print(idat_adler32.hex())
    print(idat_crc32.hex())
    my_adler32 = checksum_adler(idat_data[7:-ADLER_LEN])
    print(my_adler32)
    my_checksum = checksum(idat_data)
    print(my_checksum)

    offset += H_LEN + idat_length + CRC_LEN
    print()

print(file1[offset:offset+50])



iend_chunk = file1[-12:]
print(iend_chunk)

# data1 = file1[49:-12]
# data2 = file2[49:-12]

# combined = b''.join([(a ^ b).to_bytes(1, 'little') for a, b in zip(data1, data2)])
# # print(combined)

# new_picture = ihdr + idat_filter + combined + iend
# with open('flag.png','wb') as f:
#     f.write(new_picture)