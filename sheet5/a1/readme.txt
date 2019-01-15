CBC Malleability: 
The title of the task is very suggestive: Malleability is a property of
cryptographic algorithms: An algorithm is "malleable" if it is possible to
transform a ciphertext into another ciphertext which decrypts to a related
plaintext without necessarily knowing the variables(the key, for example) to
the ciphertext instance.

CBC (Cipher block chaining) are partly malleable: flipping a bit in a
ciphertext block will ruin the plaintext for this block, but will result in the
same bit being flipped on the next. This way, we can sacrifice a block the
next. And the format of the transactions in this task allows us to do so
because an entire block before the dest account block is "<reason>", which is
one of the most useless field and the server doesn't validate it.

This way, by flipping the bits that would turn #78384 into #31337 on the n-1
block will give us the desired effect, as the script does:

wUHhFdm5le/fLoF/G4U0u6FGSNVtkxFA3ZIEwYombzhGF2eYUCOusH3g2R56BtYlBd5FO/XlJkQ058Ev+8hTIA==

And the server accepts it as a valid transfer :)

Basic cryptography principle violated: Integrity -> It should be ensured that
the messages received by the receiver are not altered anywhere on the
communication path. In this case, (just because it was asked) the flaw on the
communication system was "me", who altered it.
