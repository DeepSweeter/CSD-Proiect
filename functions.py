#Constants
w = 32
r = 20

FF32 = 0xffffffff

#RC6 key schedule constants
P32 = 0xB7E15163
Q32 = 0x9E3779B9


#Functions

def leftRotate(n, d):
    d = d % w
    return ((n << d)|(n >> (w - d))) & FF32
 
def rightRotate(n, d):
    return (n >> d)|(n << (w - d)) & FF32

#TODO Add the rest of the functions necessary for the algorithm

def add_modulo_2w(a, b):
    return (a + b) & FF32

def xor(a, b):
    return a ^ b

def multiply_modulo_2w(a, b):
    return (a * b) & FF32

def split_in_4registers(plain_text):

    plain_bytes = plain_text.encode()

    while len(plain_bytes) % (4 * w // 8) != 0:
        plain_bytes += b'\x00'

    A = int.from_bytes(plain_bytes[0:(w // 8)], byteorder='big')
    B = int.from_bytes(plain_bytes[(w // 8):(2 * w // 8)], byteorder='big')
    C = int.from_bytes(plain_bytes[(2 * w // 8):(3 * w // 8)], byteorder='big')
    D = int.from_bytes(plain_bytes[(3 * w // 8):(4 * w // 8)], byteorder='big')

    return A, B, C, D