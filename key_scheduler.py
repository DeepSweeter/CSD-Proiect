from functions import *


# TODO Check if this function works properly
def key_schedule(key):
    b = len(key)
    c = b // 4
    t = 2 * r + 4

    L = [0] * c
    S = [0] * t

    user_key = [b for b in key]
    for i in range(b - 1, -1, -1):
        L[i // 4] = (L[i // 4] << 8) + user_key[i]
    
    S[0] = P32
    for i in range(1, t):
        S[i] = (S[i - 1] + Q32) % MOD32#& FF32

    A = B = i = j = 0

    v = (3 * max(c, t))

    for s in range(v):
        A = S[i] = leftRotate((((S[i] + A) % MOD32) + B) % MOD32, 3)
        B = L[j] = leftRotate((((L[j] + A) % MOD32) + B) % MOD32, (A + B) % MOD32)
        i = (i + 1) % t
        j = (j + 1) % c
    
    return S

