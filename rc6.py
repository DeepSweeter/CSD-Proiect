from key_scheduler import *
import math

#TODO The encryption and decryption algorithm should be here

class rc6:

    def __init__(self,key,plain_text,t,u,A,B,C,D):
        self.key = key
        self.plain_text = plain_text
        self.A,self.B,self.C,self.D = split_in_4registers(plain_text)


    def encrypt(self):
        S = key_schedule(self.key)

        self.B = self.B + S[0]
        self.D = self.D + S[1]

        for i in range(1,r+1):
            self.t = leftRotate(multiply_modulo_2w(self.B,2*self.B+1),math.log2(w))
            self.u = leftRotate(multiply_modulo_2w(self.D,2*self.D+1),math.log2(w))
            self.A = add_modulo_2w(leftRotate((xor(self.A,self.t)),self.u),S[2*i])
            self.C = add_modulo_2w(leftRotate((xor(self.C,self.u)),self.t),S[2*i + 1])
            self.A = self.B
            self.B = self.C
            self.C = self.D
            self.D = self.A
        
        self.A = multiply_modulo_2w(self.A,S[t-2])
        self.C = multiply_modulo_2w(self.C,S[t-1])
                           
        return self.A+self.B+self.C+self.D     
                 

    def decrypt(self,ctext):
        S = key_schedule(self.key)

        self.C = multiply_modulo_2w(self.C,-S[self.t-1])
        self.A = multiply_modulo_2w(self.A,-S[self.t-2])

        for i in range (r,0,-1):
            self.A = self.D
            self.D = self.C
            self.C = self.B
            self.D = self.C
            self.u = leftRotate(multiply_modulo_2w(self.D,2*self.D+1),math.log2(w))
            self.t = leftRotate(multiply_modulo_2w(self.B,2*self.B+1),math.log2(w))
            self.C = xor(rightRotate(multiply_modulo_2w(self.C,-S[2*i+1]),self.t),self.u)
            self.A = xor(rightRotate(multiply_modulo_2w(self.A,-S[2*i]),self.u),self.t)

        self.D = self.D - S[1]
        self.B = self.B - S[1]

        return self.A+self.B+self.C+self.D