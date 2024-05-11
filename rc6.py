from key_scheduler import *
from functions import *

class rc6:

    def __init__(self, key):
        self.key = key
        self.A = 0
        self.B = 0
        self.C = 0
        self.D = 0
        self.t = 0
        self.u = 0


    def encrypt(self, plain_text):
        S = key_schedule(self.key)
        self.A, self.B, self.C, self.D = split_in_4registers(plain_text)

        self.B = (self.B + S[0]) % MOD32
        self.D = (self.D + S[1]) % MOD32

        for i in range(1, r+1):
            self.t = leftRotate(((self.B * (2 * self.B + 1)) % MOD32), LOG32)
            self.u = leftRotate(((self.D * (2 * self.D + 1)) % MOD32), LOG32)
            self.A = (leftRotate((self.A ^ self.t), self.u) + S[2 * i]) % MOD32
            self.C = (leftRotate((self.C ^ self.u), self.t) + S[2 * i + 1]) % MOD32
            self.A, self.B, self.C, self.D = self.B, self.C, self.D, self.A
        
        self.A = (self.A + S[42]) % MOD32
        self.C = (self.C + S[43]) % MOD32
                           
        return struct.pack('I', self.A) + struct.pack('I', self.B) + struct.pack('I', self.C) + struct.pack('I', self.D)
                 

    def decrypt(self,ctext):
        S = key_schedule(self.key)
        self.A, self.B, self.C, self.D = split_in_4registers(ctext)

        self.C = (self.C - S[2*r + 3]) % MOD32
        self.A = (self.A - S[2*r + 2]) % MOD32

        for i in range(r, 0, -1):
            self.A, self.B, self.C, self.D = self.D, self.A, self.B, self.C
            self.u = leftRotate((self.D * ((2*self.D+1) % MOD32)) % MOD32, LOG32)
            self.t = leftRotate((self.B * ((2*self.B+1) % MOD32)) % MOD32, LOG32)
            self.C = rightRotate((self.C - S[2*i+1]) % MOD32, self.t) ^ self.u
            self.A = rightRotate((self.A - S[2*i]) % MOD32, self.u) ^ self.t

        self.D = (self.D - S[1]) % MOD32
        self.B = (self.B - S[0]) % MOD32

        return struct.pack('I', self.A) + struct.pack('I', self.B) + struct.pack('I', self.C) + struct.pack('I', self.D)

def encrypt_variable_length(plain_text, key):
    plain_text, nr0 = pad_to_128_bits(plain_text)
    obj = rc6(key)
    fragment = [plain_text[k:k + 16] for k in range(0, len(plain_text), 16)]
    encrypted_fragments = []
    for i in range(len(fragment)):
        if i != 0:
            fragment[i] = xor_bytes(fragment[i], encrypted_fragments[i - 1])
        encrypted_fragments.append(obj.encrypt(fragment[i]))
    return b''.join(encrypted_fragments), nr0


def decrypt_variable_length(cipher_text, key, nr0):
    obj = rc6(key)
    fragment = [cipher_text[k:k + 16] for k in range(0, len(cipher_text), 16)]
    decrypted_fragments = []
    for i in range(len(fragment)):
        print(str(fragment[i]) + " : " + str(len(fragment[i])))
        decrypted_block = obj.decrypt(fragment[i])
        if i != 0:
            decrypted_block = xor_bytes(decrypted_block, fragment[i - 1])
        decrypted_fragments.append(decrypted_block)

    if nr0 == 0:
        return b''.join(decrypted_fragments)

    return b''.join(decrypted_fragments)[:-nr0]