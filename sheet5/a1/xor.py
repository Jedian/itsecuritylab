#!/usr/bin/env python

# Format: TRANSFER AMOUNT $1000000 REASON Salary Jan. 2016 DEST #78384 END

from Crypto.Cipher import AES
import base64
import sys
import struct
import itertools

def xor(s, key):
    key = key * (len(s) / len(key) + 1)
    return ''.join(chr(ord(x) ^ ord(y)) for (x,y) in itertools.izip(s, key))

l = "wUHhFdm5le/fLoF/G4U0u6FGSNVtkxFA3ZIEwYombzhGF2eYUCOutHTg0h16BtYlBd5FO/XlJkQ058Ev+8hTIA=="
l = base64.b64decode(l)
valblocknminusone = l[32:48]
newblock = xor(xor(" DEST #78384 END", " DEST #31337 END"), valblocknminusone)
l = l[:32] + newblock + l[48:]
print base64.b64encode(l)
