from key_scheduler import *
import math

#TODO The encryption and decryption algorithm should be here

class rc6:

    def __init__(self,key):
        self.key = key
        self.A = 0
        self.B = 0
        self.C = 0
        self.D = 0
        self.t = 0
        self.u = 0


    def encrypt(self, plain_text):
        S = key_schedule(self.key)
        self.A,self.B,self.C,self.D = split_in_4registers(plain_text)

        self.B = add_modulo_2w(self.B, S[0])
        self.D = add_modulo_2w(self.D, S[1])

        for i in range(1,r+1):
            self.t = leftRotate(multiply_modulo_2w(self.B,2*self.B+1),LN)
            self.u = leftRotate(multiply_modulo_2w(self.D,2*self.D+1),LN)
            self.A = add_modulo_2w(leftRotate((xor(self.A,self.t)),self.u),S[2*i])
            self.C = add_modulo_2w(leftRotate((xor(self.C,self.u)),self.t),S[2*i + 1])
            self.A = self.B
            self.B = self.C
            self.C = self.D
            self.D = self.A
        
        self.A = add_modulo_2w(self.A,S[2*r + 2])
        self.C = add_modulo_2w(self.C,S[2*r + 3])
                           
        return struct.pack('I',self.A) + struct.pack('I',self.B) + struct.pack('I',self.C) + struct.pack('I',self.D)     
                 

    def decrypt(self,ctext):
        S = key_schedule(self.key)
        self.A,self.B,self.C,self.D = split_in_4registers(ctext)


        self.C = multiply_modulo_2w(self.C,-S[2*r + 3])
        self.A = multiply_modulo_2w(self.A,-S[2*r + 2])

        for i in range (r,0,-1):
            self.A = self.D
            self.D = self.C
            self.C = self.B
            self.D = self.C
            self.u = leftRotate(multiply_modulo_2w(self.D,2*self.D+1),LN)
            self.t = leftRotate(multiply_modulo_2w(self.B,2*self.B+1),LN)
            self.C = xor(rightRotate(add_modulo_2w(self.C,-S[2*i+1]),self.t),self.u)
            self.A = xor(rightRotate(add_modulo_2w(self.A,-S[2*i]),self.u),self.t)

        self.D = self.D - S[1]
        self.B = self.B - S[1]

        bA = self.A.to_bytes(4, 'big')
        bB = self.B.to_bytes(4, 'big')
        bC = self.C.to_bytes(4, 'big')
        bD = self.D.to_bytes(4, 'big')

        return bA + bB + bC + bD