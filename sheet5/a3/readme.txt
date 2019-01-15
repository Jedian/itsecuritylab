RSA Small Exponent:
By examining the public keys, I could see they all had the same small exponent:
3. A small value for this is useful to avoid the calculation time during
encryption or signature-verification. By increasing the exponent, you increase
the amount of messages one has to gather to read your message.

But this is not the flaw exploited here. The problem that happened here is that
the attacker(us) could get multiple copies of the same message encrypted. If
each message was different, we could not attack this way.
Also, some kinds of paddings(non-linear) could avoid it.

This attack is called "Coppersmith's Attack" (more specifically: Hastad's
broadcast attack) and is based on the pure mathematical definitions of how RSA
works and is implemented. 

The message is:
The answer to life the universe and everything = 42

To run:

$  python script.py pk1.pem pk2.pem pk3.pem msg1.bin msg2.bin msg3.bin
