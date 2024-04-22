from key_scheduler import *
from functions import *
from rc6 import *

#plaintext 02 13 24 35 46 57 68 79 8a 9b ac bd ce df e0 f1
#user key 01 23 45 67 89 ab cd ef 01 12 23 34 45 56 67 78
#ciphertext 52 4e 19 2f 47 15 c6 23 1f 51 f6 36 7e a4 3f 18
file_path = "Files/fisier_test.txt"


def pad_to_128_bits(plain_text):
    cnt0 = 0
    while len(plain_text) % 16 != 0:
        plain_text += b'0'
        cnt0 += 1
    return plain_text,cnt0

def encrypt_variable_length(plain_text, key):
    plain_text, nr0 = pad_to_128_bits(plain_text)
    obj = rc6(key)
    fragment = [plain_text[k:k+16] for k in range(0, len(plain_text), 16)]
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
        decrypted_block = obj.decrypt(fragment[i])
        if i != 0:
            decrypted_block = xor_bytes(decrypted_block, fragment[i - 1])
        decrypted_fragments.append(decrypted_block)
        
    if nr0 == 0:
        return b''.join(decrypted_fragments)
    
    return b''.join(decrypted_fragments)[:-(nr0+1)]

def split_in_pack_1376B(cypher_text):
    return [cypher_text[k:k+1376] for k in range(0, len(cypher_text),1376)]


if __name__ == "__main__":
    # key = b'\x01\x23\x45\x67\x89\xab\xcd\xef\x01\x12\x23\x34\x45\x56\x67\x78'
    # plaintext = b'\x02\x13\x24\x35\x46\x57\x68\x79\x8a\x9b\xac\xbd\xce\xdf\xe0\xf1'
    # key_schedule_result = key_schedule(key)
    # print("Key Schedule:")
    # for i, val in enumerate(key_schedule_result):
    #     print("S[{}]: {:08X}".format(i, val))
    #
    # rc6_class = rc6(key)
    # print("Plaintext = ", end=' ')
    # for byte in plaintext:
    #     print('{:02X}'.format(byte), end=' ')
    #
    # ctext = rc6_class.encrypt(plaintext)
    # print("\nCyphertext = ", end=' ')
    # for byte in ctext:
    #     print('{:02X}'.format(byte), end=' ')
    # print("\n")
    #
    # dtext= rc6_class.decrypt(ctext)
    # print("\nDecrypt Text = ", end=' ')
    # for byte in dtext:
    #     print('{:02X}'.format(byte), end=' ')
    # Exemplu de cheie și text clar
    key = b'1234567812345678'
    plain_text = b'This is a test message. It is longer than 16 bytes.'
    print("Plaint text: ", str(plain_text))

    cipher_text, nr0 = encrypt_variable_length(plain_text, key)
    #x = ' '.join([f'{i:02x}' for i in cipher_text])
    print('Text criptat:', cipher_text)

    decrypted_text = decrypt_variable_length(cipher_text, key,nr0)
    print('Text decriptat:', decrypted_text)

    #assert decrypted_text[:len(plain_text)] == plain_text, 'Decryption failed!'
    trustFlag = 1
    for i in range(len(plain_text)):
        if(str(plain_text)[i] != str(decrypted_text)[i]):
            trustFlag = 0

    print(trustFlag)

    print("Plain text: ---------------------------------------------------------------------")
    with open(file_path,'r') as f:
        text = f.read()
    print(text.encode())

    ctext,nr1 = encrypt_variable_length(text.encode(),key)
    dtext = decrypt_variable_length(ctext,key,nr1)
    print("Cypher text: --------------------------------------------------------------------")
    print(ctext)
    print("Decrypted text: -----------------------------------------------------------------")
    print(dtext)


    print("Fragments: -----------------------------------------------------------------")
    fragments = []
    fragments = split_in_pack_1376B(dtext)
    for i in range(len(fragments)):
        print("fragment["+str(i)+"]--------------------------------------------------\n")
        print(fragments[i])
        print(len(fragments[i]))
