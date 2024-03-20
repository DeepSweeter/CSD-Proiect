from functions import *


#TODO Check if this function works properly
def key_schedule(key, w, r):
    c = len(key) // (w // 8)
    rounds = 2 * (r + 1)
    L = [0] * rounds

    #Initialize L
    for i in range(c):
        L[i] = int.from_bytes(key[i * (w // 8) : (i + 1) * (w // 8)])
    
    S = [0] * (2 * r + 4)
    S[0] = P32
    for i in range(1, 2 * r + 3):
        S[i] = (S[i - 1] + Q32) & FF32

    A = B = i = j = 0

    v = 3 * max(c, 2 * r + 4)

    for s in range(v):
        A = S[i] = leftRotate((S[i] + A + B) & FF32, 3)
        B = L[j] = leftRotate((L[j] + A + B) & FF32, (A + B))
        i = (i + 1) % (2 * r +4)
        j = (j + 1) % c
    
    return S

