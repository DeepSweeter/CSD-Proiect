from key_scheduler import *
from functions import *
from rc6 import *



if __name__ == "__main__":
    key = b'\x01\x23\x45\x67\x89\xab\xcd\xef'
    key_schedule_result = key_schedule(key, w, r)
    print("Key Schedule:")
    for i, val in enumerate(key_schedule_result):
        print("S[{}]: {:08X}".format(i, val))