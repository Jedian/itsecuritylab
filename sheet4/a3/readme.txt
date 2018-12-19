Flappy hacks:

Anti-emulation routines:

There are a lot of anti emulation routines: some of them are very similar to
those present in the previous tasks.

Class /com/prosper/ts/hapra/b/b:
    * The code tries to get the address of the default bluetooth adapter, which
    causes an exception on most emulators and exits the program.

    * The code compare the build fingerprint with a lot of strings that would
    be present in emulators build fingerprints, exiting the program in case it
    finds any of them. (There seems also to be a trap for if you modify this
    function: if the same string-comparing function is called with "fish", and
    return false, the program exits)

Class /com/prosper/ts/hapra/b/a:
    * This code implements a function very similar to the string-comparing
    function on previous class b/b, but this time the "exit" call is inside it.
    (It makes it easier to make it emulable.)

Class /com/prosper/ts/hapra/GameActivity:
    * Here we have some tests about battery level and status: if it is exactly
    50% loaded (some emulators seems to implement it to be on 50% by default)
    or if there is no information about it, it is likely running inside an
    emulator.

    * And we have again a string-comparing function similar to the others, but
    printing a message saying you was caught by trying to use emulators.

I could get rid of them and the apk here can run on an emulator without major
problems.

Cheats: There are three cheats:

    1) The first one does nothing besides making a toast appear with the
    message "Success". It is stored in the apk md5 hashed, so it would be
    really hard to find out, but the answer is in those online databases of
    hashes and the answer is "HaPra".

    2) The second cheat is harder, because it is sha256 hashed and the answer
    is not on those online databases. I could not find the actual string that
    has this hash, but I could replace it with a hash I knew the string it was
    from to simulate the cheatcode and see it's effect. It makes some toasts
    appear with hints to find the next cheat, using the answer to this one, so
    not helpful at all for me :(

    3) The same as the previous, it is sha256 hashed, and I had to simulate
    another cheatcode in the same way. This adds a multiplier of 1000 for every
    point. Making it really easy to surpass uncheaters scores within a few flaps.


Verification routine:
    on class /com/prosper/ts/hapra/b/b there is a function a() that receives 2
    strings as parameters: it is called throughout the code with str1 being the
    one you write on field cheat of the app and str2 being the hashed version
    of the cheat the code is trying to check.

    This function calls another function a() from class /com/prosper/ts/hapra/a
    with a lot of parameters, which itself is quite naughty: 
        -> It load up every image (asset) on assets/gfx/game/ and xor decrypt
        (key: filename) it into a temporary file. Then it tries to load it as a
        class.
        -> If it works, then it invokes a method specified by the parameters
        from inside the just loaded secret class and return its value.

    So, inside this secret class, there is a method(V.v()) that hashes str1 with md5
    and sha256 and compares it with str2. Returning true if they are equal. And
    this is the method called by the first function here mentionated (a()).

    When the md5 or sha256 hash of str1 is equal to str2, the corresponding
    cheat is activated.

    There are some other labirinth and maze-like routines involved, but this is
    the main and probably the trickiest one.
