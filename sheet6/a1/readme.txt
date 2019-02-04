Basic Reverse Engineering:

1) The password really stands out after following the tip and using "strings".
Together with the other not built-in strings of the executable, like
"Congratulations", we see "p4ssw0rd". Testing it is easy and get us the success
message.

2) After some analyzing (I used another decompiler also: boomerang), I could
see that the second challenge was a number composed of 4 summed integers:

0x3e8 + 0x12c + 0x1e + 0x7 -> 1337

3) The third one has a more complex loop evaluating the answer. My first
approach was to rewrite the loop, it leaded me to the correct answer, but I
played with the debugger solution as well.
The answer is "zyvgjqpc"
