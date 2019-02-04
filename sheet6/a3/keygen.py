#!/usr/bin/python
import sys

lic = "AAAAA-AAAAA-AAAAA-AAAAA-AAAAX"

sigma = range(ord("A"), ord("Z")+1)
keys_1 = []
keys_2 = []

def first_five(n):
    for i in sigma:
        keys_1.append(chr(i)*5)
    for i in sigma:
        for j in range(i+1, ord("Z")+1):
            keys_1.append(chr(i) + chr(i) + "A" + chr(j) + chr(j))
            keys_1.append(chr(i) + chr(j) + "A" + chr(i) + chr(j))
            keys_1.append(chr(i) + chr(j) + "A" + chr(j) + chr(i))
            keys_1.append((chr(i) + chr(i) + "A" + chr(j) + chr(j))[::-1])
            keys_1.append((chr(i) + chr(j) + "A" + chr(i) + chr(j))[::-1])
            if len(keys_1) >= n:
                return

def first_ten(n):
    for i in keys_1:
        i += "-"
        for j in sigma:
            for k in range(j+1, ord("Z")+1):
                for l in sigma:
                    keys_2.append(i + chr(j)*2 + chr(k) + chr(l) + chr(k))
                    keys_2.append(i + chr(j) + chr(k) + chr(j) + chr(l) + chr(k))
                    keys_2.append(i + chr(k) + chr(j)*2 + chr(l) + chr(k))
                    keys_2.append(i + chr(k)*2 + chr(j) + chr(l) + chr(j))
                    keys_2.append(i + chr(k) + chr(j) + chr(k) + chr(l) + chr(j))
                    keys_2.append(i + chr(j) + chr(k)*2 + chr(l) + chr(j))
                    if len(keys_2) >= n:
                        return

try:
    n = int(sys.argv[1])
    first_five(n)
    first_ten(n)
    for i in range(n):
        print keys_2[i] + "-AAAAA-AMALA-ABBAX"
except Exception as e:
    print "Usage: ./keygen.py <amount_of_keys>"
    print str(e)
