import struct
import math

#Constants
w = 32
r = 20

FF32 = 2 ** w

MOD32 = 0xffffffff

LN = int(math.log2(w))

#RC6 key schedule constants
P32 = 0xB7E15163
Q32 = 0x9E3779B9


#Functions

def leftRotate(n, d):
    d = d % w
    return ((n << d)|(n >> (w - d))) % FF32
 
def rightRotate(n, d):
    d = d % w
    return (n >> d)|(n << (w - d)) % FF32

#TODO Add the rest of the functions necessary for the algorithm

def add_modulo_2w(a, b):
    return (a + b) % FF32

def xor(a, b):
    return a ^ b

def multiply_modulo_2w(a, b):
    return (a * b) % FF32

def split_in_4registers(plain_text):

    #plain_bytes = plain_text.encode()
    A = struct.unpack('I', plain_text[:4])[0]
    print("\n\n A: ", A,end = "  ")
    B = struct.unpack('I', plain_text[4:8])[0]
    print("B: ", B,end = "  ")
    C = struct.unpack('I', plain_text[8:12])[0]
    print("C: ", C,end = "  ")
    D = struct.unpack('I', plain_text[12:])[0]
    print("D: ", D,end = "  ")
    print("\n")


    return A, B, C, D