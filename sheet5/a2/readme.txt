HMAC Length Extension Attack:

This attack works because most of the hashing algorithms have in it's output
all the information of the state the algorithm was when hashing it. So, we can
make it "keep hashing" with appended new data.  Actually we also need to know
the size of what has been hashed until now. We have the length of the message,
but not of the key, that is why we should try brute-forcing the length of the
key.

For the first trial, I searched for key lengths between 1 and 1337. It happened
that the actual key length is only 20, so it was really fast to get it.

There is also a step in the hashing algorithms that appends a padding to the
string to be hashed, until it's length in bytes is congruent to 56 (mod 64).
After this, in the last 8 bytes (to complete 64) there is the size of the whole
original message in bits (8*(20 + 373) = 3144), which, in hexadecimal, is
"c48". And 48 is the ASCII code for "H". That is why there is always a "H" on
the message.
There could also be more weird characters, but as the task mentions: the server
ignores non-ASCII characters.

P.S.: To test it, you should remove the signature in the first line of the
file.  And some text editors (vim, for example), by default, add a EOL at the
end of the file. This will make it stop working. An easy workaround for vim is
executing ":set binary" and ":set noeol" before saving.
