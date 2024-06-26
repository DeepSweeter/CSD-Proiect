import struct
import socket
#Constants
w = 32
r = 20

FF32 = 0xffffffff

MOD32 = 2 ** w

LOG32 = 5

#Maximum transmission unit
#TCP header 40-60 bytes. 
#Usual MTU for: 
#   Ethernet : 1500
#   WiFi : 1460
# 1376 => 86 blocks of 128 bits
MTU = 1376

#RC6 key schedule constants
P32 = 0xB7E15163
Q32 = 0x9E3779B9


#Diffie - Hellman key exchange variables
P = 0xfca682ce_8e12caba_26efccf7_110e526d_b078b05e_decbcd1e_b4a208f3_ae1617ae_01f35b91_a47e6df6_3413c5e1_2ed0899b_cd132acd_50d99151_bdc43ee7_37592e17
G = 0x678471b2_7a9cf44e_e91a49c5_147db1a9_aaf244f0_5a434d64_86931d2d_14271b9e_35030b71_fd73da17_9069b32e_2935630e_1c206235_4d0da20a_6c416e50_be794ca4


#Debugging

server_address = "127.0.0.5" #socket.gethostbyname()

#Functions

def leftRotate(n, d):
    d %= w
    return ((n << d)|(n >> (w - d))) % MOD32
 
def rightRotate(n, d):
    d %= w
    return ((n >> d)|(n << (w - d))) % MOD32

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


def xor_bytes(a, b):
    return bytes(x ^ y for x, y in zip(a, b))

def pad_to_128_bits(plain_text):
    cnt0 = 0
    while len(plain_text) % 16 != 0:
        plain_text += b'0'
        cnt0 += 1
    return plain_text, cnt0

def split_in_pack_1376B(cypher_text):
    return [cypher_text[k:k + 1376] for k in range(0, len(cypher_text), 1376)]

def get_local_ip():
    try:
        # Create a socket
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))  # Connect to a known external server
        local_ip = s.getsockname()[0]  # Get the local IP address
        s.close()
        return local_ip
    except Exception as e:
        print("Error:", e)
        return None