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