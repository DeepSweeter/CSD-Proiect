from key_scheduler import *
from functions import *
from rc6 import *
import struct

#plaintext 02 13 24 35 46 57 68 79 8a 9b ac bd ce df e0 f1
#user key 01 23 45 67 89 ab cd ef 01 12 23 34 45 56 67 78
#ciphertext 52 4e 19 2f 47 15 c6 23 1f 51 f6 36 7e a4 3f 18

if __name__ == "__main__":
    key = b'\x01\x23\x45\x67\x89\xab\xcd\xef\x01\x12\x23\x34\x45\x56\x67\x78'
    plaintext = b'\x02\x13\x24\x35\x46\x57\x68\x79\x8a\x9b\xac\xbd\xce\xdf\xe0\xf1'
    # key_schedule_result = key_schedule(key)
    # print("Key Schedule:")
    # for i, val in enumerate(key_schedule_result):
    #     print("S[{}]: {:08X}".format(i, val))

    rc6_class= rc6(key)
    print("Plaintext = ", end=' ')
    for byte in plaintext:
        print('{:02X}'.format(byte), end=' ')

    ctext = rc6_class.encrypt(plaintext)
    print("\nCyphertext = ", end=" ")
    for byte in ctext:
        print('{:02X}'.format(byte), end=' ')
    print("\n")

    dtext= rc6_class.decrypt(ctext)
    print("\nDecrypt Text = ", end=' ')
    for byte in dtext:
        print('{:02X}'.format(byte), end=' ')


