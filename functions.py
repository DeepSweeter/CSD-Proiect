import struct
import math

#Constants
w = 32
r = 20

FF32 = 0xffffffff

MOD32 = 2 ** w

LOG32 = 5

#RC6 key schedule constants
P32 = 0xB7E15163
Q32 = 0x9E3779B9


#Functions

def leftRotate(n, d):
    d %= w
    return ((n << d)|(n >> (w - d))) % MOD32
 
def rightRotate(n, d):
    d %= w
    return ((n >> d)|(n << (w - d))) % MOD32

#TODO Add the rest of the functions necessary for the algorithm

def xor(a, b):
    return a ^ b

def split_in_4registers(plain_text):

    #plain_bytes = plain_text.encode()
    A = struct.unpack('<I', plain_text[:4])[0]
    #print("\n", A)
    B = struct.unpack('<I', plain_text[4:8])[0]
    #print(B)
    C = struct.unpack('<I', plain_text[8:12])[0]
    #print(C)
    D = struct.unpack('<I', plain_text[12:])[0]
    #print(D)


    return A, B, C, D