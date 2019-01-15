import sys
import binascii
from Crypto.PublicKey import RSA
from base64 import b64decode

def chinese_remainder(n, a):
    sum = 0
    prod = reduce(lambda a, b: a*b, n)
 
    for n_i, a_i in zip(n, a):
        p = prod / n_i
        sum += a_i * mul_inv(p, n_i) * p
    return sum % prod
 
def mul_inv(a, b):
    b0 = b
    x0, x1 = 0, 1
    if b == 1: return 1
    while a > 1:
        q = a / b
        a, b = b, a%b
        x0, x1 = x1 - q * x0, x0
    if x1 < 0: x1 += b0
    return x1

def find_invpow(x,n):
    high = 1
    while high ** n < x:
        high *= 2
    low = high/2
    while low < high:
        mid = (low + high) // 2
        if low < mid and mid**n < x:
            low = mid
        elif high > mid and mid**n > x:
            high = mid
        else:
            return mid
    return mid + 1

e = 3

with open(sys.argv[1], 'r') as fl:
    n0 = long(RSA.importKey("".join(fl.read()).strip()).__getattr__('n'))

with open(sys.argv[2], 'r') as fl:
    n1 = long(RSA.importKey("".join(fl.read()).strip()).__getattr__('n'))

with open(sys.argv[3], 'r') as fl:
    n2 = long(RSA.importKey("".join(fl.read()).strip()).__getattr__('n'))

with open(sys.argv[4], 'rb') as fl:
    c0 = long(binascii.hexlify(fl.read()), 16)

with open(sys.argv[5], 'rb') as fl:
    c1 = long(binascii.hexlify(fl.read()), 16)

with open(sys.argv[6], 'rb') as fl:
    c2 = long(binascii.hexlify(fl.read()), 16)

n = [n0,n1,n2]
a = [c0,c1,c2]

result = (chinese_remainder(n, a))
resultHex = str(hex(find_invpow(result,3)))[2:-1]
print resultHex.decode('hex')
