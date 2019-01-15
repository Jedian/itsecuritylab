ECDSA Fixed K:
1) The parameters are:
ASN1 OID: prime256v1
NIST CURVE: P-256

These parameters refer to the curve used by the algorithm: it uses a prime
"0xFFFFFFFF00000000FFFFFFFFFFFFFFFFBCE6FAADA7179E84F3B9CAC2FC632551" and a
curve shape "y^2 = x^3 - 3x + b".

2) When hexdumping the signatures, we can see they have the same preffix (r);
this means they were both signed with the same argument k, which is really
unsafe and can lead us to get the original private key used to sign these
files. A different cryptographically secure random k is supposed to be used for
each signature.

3) To calculate the private key, it is possible to derivate the method from the
original algorithm, solving the inverted equations. Let's first gather all we
have:

Each signature is composed by a pair (r, s). We have two signatures sig1 and
sig2.

By hexdumping it's content ( $ xxd -p msg1.sig ), we get the following string:

3045022100bfe855905780e8470494024e6bf8e5fe7fe32bf812dcbbd169
93b1ea465a28740220615b3b0d09a5b0d2f79571392a7278bb7bb58542c5ba0d6b71a934bc17a65c4e

Reading:
30 45 -> Header + length (0x45 -> 69 bytes)
02 21 -> Mark + length of r (0x21 -> 33 bytes)
00bfe855905780e8470494024e6bf8e5fe7fe32bf812dcbbd16993b1ea465a2874 -> r1
02 20 -> Mark + length of s (0x20 -> 32 bytes)
615b3b0d09a5b0d2f79571392a7278bb7bb58542c5ba0d6b71a934bc17a65c4e   -> s1

This way we can also extract r2 ( r2 == r1 ) and s2.

Our next parameter is the hash function of the message, in this case, SHA1.
$ openssl sha1 msg1.txt
z1 = e1 = dfcaf5e269a530c571d856783ed1b15647a54625

The same operation is valid for msg2.txt, getting us z2.

We also need the integer order of the elliptic curve base point n. Most
libraries already have the recommended values codified. So I just copied it:
n = 0xffffffff00000000ffffffffffffffffbce6faada7179e84f3b9cac2fc632551

Now we can start to calculate:
First, we recover the random integer unsafely used twice: 
k = (((z1 - z2) % n) / ((s1 - s2) % n)) % n

An important remark is that, on modular arithmetics, for modular division, we
have to calculate the modular inverse:
a/b % m -> a*mod_inv(b, m) % m

By using Euler's theorem, we have that mod_inv(a, m) = a^(m-2). (This only is
valid because m is prime). This would take quite a bit to run, so I implemented
the power operation in O(log n).

Then, after we get k = 0x71a5280342079f0daec065f38a943520b71b36c8811630019ae78e483ebe952b
we can now calculate the private key 

d = (((s1*k - z1) % n) / r1) % n

Again, using the modular inverse for the division.

After this, we convert it to pem:

-----BEGIN EC PRIVATE KEY-----
MHcCAQEEIN3Kex8uJS7CrU+6WH30YS03et8nHNMys0u0mvX+dbZAoAoGCCqGSM49
AwEHoUQDQgAEHTGYikaCJAYeT9d7rZEIO2Ak3FRwf2wNeKpL7lpJsSny/BKtZFEd
V/Rynkqi9MVTREGsAijvqUCuST6UCosrGw==
-----END EC PRIVATE KEY-----

4) The script does that at the end.
