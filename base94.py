import string
import math

alphabet = string.ascii_letters + string.digits + string.punctuation
base = len(alphabet)

def encode(num):
    if not isinstance(num, int):
        raise TypeError("can only encode integers")
    if num < 0:
        raise ValueError("only positive numbers can be encoded")
    if num == 0: return alphabet[0]
    res = ''
    while num != 0:
        res = (alphabet[num%base])+res
        num = int(num/base)
    return res

def decode(st):

    if not isinstance(st, str):
        raise TypeError("can only decode strings")

    res = 0
    mult = 1

    for char in reversed(st):
        res += mult * alphabet.index(char)
        mult *= base
    return res
