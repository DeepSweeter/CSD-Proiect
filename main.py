from rc6 import *

#plaintext 02 13 24 35 46 57 68 79 8a 9b ac bd ce df e0 f1
#user key 01 23 45 67 89 ab cd ef 01 12 23 34 45 56 67 78
#ciphertext 52 4e 19 2f 47 15 c6 23 1f 51 f6 36 7e a4 3f 18

file_path = "Files/fisier_test.txt"

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
    #Test
    print("Test1 :#####################################################################################################\n")
    plain_text = "This is a test message. It is longer than 16 bytes."
    print("Plain text: ---------------------------------------------------------------------")
    print(plain_text)

    cipher_text, nr0 = encrypt_variable_length(plain_text.encode(), key)
    print("\n--------------- Nr de zerouri adaugate prin padding: {} ---------------".format(nr0))
    print("\nCypher text: --------------------------------------------------------------------")
    print(cipher_text)
    x = ' '.join([f'{i:02x}' for i in cipher_text])
    print("\nCypher text in hexazecimal: -----------------------------------------------------")
    print(x)

    decrypted_text = decrypt_variable_length(cipher_text, key, nr0)
    print("\nDecrypted text: -----------------------------------------------------------------")
    print(decrypted_text.decode())

    trustFlag = 1
    for i in range(len(plain_text)):
        if plain_text[i] != decrypted_text.decode()[i]:
            trustFlag = 0

    if trustFlag:
        print("\nCripatare si decriptare efectuate cu succes!!!\n")
    else:
        print("\nEroare la functiile de criptare si/sau decriptare!!!\n")

    print("Test2 :#####################################################################################################\n")
    print("Plain text: ---------------------------------------------------------------------\n")
    with open(file_path, 'r') as f:
        text = f.read()
    print(text)

    ctext, nr1 = encrypt_variable_length(text.encode(), key)
    print("\n--------------- Nr de zerouri adaugate prin padding: {} ---------------".format(nr1))
    dtext = decrypt_variable_length(ctext, key, nr1)
    print("\nCypher text: --------------------------------------------------------------------\n")
    print(ctext)
    print("\nDecrypted text: -----------------------------------------------------------------\n")
    print(dtext.decode())


    print("\n---------------------------------------- Fragments ----------------------------------------")
    fragments = []
    fragments = split_in_pack_1376B(dtext)
    for i in range(len(fragments)):
        print("----------pachet[{}]----------".format(i))
        print(fragments[i].decode())
        print("--------------- Dimensiune pachet : {} (octeti) ---------------\n".format(len(fragments[i])))
