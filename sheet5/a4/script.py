#!/usr/bin/python
import ecdsa

def log_pow(a, p, m):
    if p==0:
        return 1
    elif p==1:
        return a
    else:
        r = log_pow(a, p/2, m) % m
        if p%2==0:
            return r*r % m
        else:
            return r*r*a % m

def moddivide(a, b, m): #a/b % m
    #inv = inverse_mod(b, m)
    inv = log_pow(b, m-2, m) % m
    return (inv*a) % m


n = 0xffffffff00000000ffffffffffffffffbce6faada7179e84f3b9cac2fc632551L
Ln = 256
r1 = 0x00bfe855905780e8470494024e6bf8e5fe7fe32bf812dcbbd16993b1ea465a2874L
s1 = 0x615b3b0d09a5b0d2f79571392a7278bb7bb58542c5ba0d6b71a934bc17a65c4eL
r2 = 0x00bfe855905780e8470494024e6bf8e5fe7fe32bf812dcbbd16993b1ea465a2874L
s2 = 0x63089fbaccdc2c5c8aa9583a7627b79f25c0d1188a94b569b5d90f317c4faf65L
e1 = 0xdfcaf5e269a530c571d856783ed1b15647a54625L
e2 = 0x4b6d51036ccc95cb6f97f08deb36fdf0f564b412L
z1 = int(bin(e1)[2:][:Ln], 2)
z2 = int(bin(e2)[2:][:Ln], 2)

k = moddivide((z1 - z2)%n, (s1 - s2)%n, n)
dA = moddivide(((s1*k)%n - z1)%n, r1%n, n)

hkey = hex(dA)[2:len(hex(dA))-1]
print "Private key calculated: " + hkey
pkey = hkey.decode('hex')

sk = ecdsa.SigningKey.from_string(pkey, curve=ecdsa.NIST256p)
print "Signing new message with the private key..."
msg = 'int getRandomNumber(){ return -1 }'
sig1 = sk.sign(msg)

vk = ecdsa.VerifyingKey.from_pem(open("vk.pem").read())

print "Verifying message with public key..."
try:
    print vk.verify(sig1, msg)
    print "Success! Writing private key to sk.pem..."
    with open('sk.pem', 'w') as f:
        f.write(sk.to_pem())
except Exception as e:
    print "Error! " + str(e)
