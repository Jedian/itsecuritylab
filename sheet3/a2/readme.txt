Sandbox:
In this task, I wrote a mini-library with wrappers around commonly used
functions to interact with files:
    - open, fopen
    - read, fread
    - write, fwrite

Running an application/program that uses one of this functions while the
LD_PRELOAD env variable is setted up causes the program to use our wrappers
instead of the original functions, giving us the power to debug an unknown and
suspicious application.

For this, a pair of whitelists is used to manually set which files the
sandboxed application can access/modify.
    -> whitelistread.txt keeps track of the absolute pathname of a file which
    is allowed to be read inside the sandbox
    -> whitelistwrite.txt keeps track of the absolute pathname of a file which
    is allowed to be modified inside the sandbox

With the motivation to try to keep the sandboxed application to run the longest
as possible without "realizing" it is inside a sandbox, when it tries to opens
a file without permission, it gets access to stdin/stdout instead of raising an
error.

To compile the library:
gcc -shared -fPIC sandbox.c -o sandbox.so -ldl

To run a program inside it:
LD_PRELOAD=$PWD/sandbox.so a.out

#WAYS HOW TO BREAK OUT THIS SANDBOX

1 -> Static compiling: If we static compile an application, it won't try to
load any library. Therefore, the versions of the functions it had while
compiling will be the ones actually called.

2 -> Demand your application to be owned by root, using setuid/setgit: By
default, linux prevents attaching to a setuid/setgit process.

3 -> Making syscalls directly, without using the wrappers available in the
loadable libraries. Maybe writing your own safe wrappers.
