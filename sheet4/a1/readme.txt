H4ckpr0:

Hard-coded Credentials:
private static final String[] DUMMY_CREDENTIALS = new String[]{"YmFiYnlzQGZpcnN0LnJlOnBhY2thZ2VkLmFwcA=="};

DbgAnal.class: It tries to detect debugging by gathering two informations: the
application uid, and it's flags. If the uid is 42 or 1337, it immediately
returns false. Otherwise, it gets the flags and check if the FLAG_DEBUGGABLE (0x2) flag is
on, but return true even if it is not.

EmAnal.class: It searchs for string "sdk" in the field FINGERPRINT of the
Build. "sdk" is short for "Software Development Kit" and if it is inside the
fingerprint, it means it is an emulator.

InAnal.class: It tries to detect repackaging by comparing the hard-coded
certificate (probably the one used to sign the apk) with the certificate used
to sign the apk. If it is different, then it was repackaged.

DyAnal.class: It gets four system's properties that inform whether the secure
usb debugging is available/active or not. This way, it is able to confirm if it
is inside an analysis environment.


I had a lot of problems trying to repack this app :(
(I tried even without changing anything, even just
    $ apktool d h4ckpro.apk; 
    $ ./apkBuildersh.sec h4ckpro;
would fail :( )
So I tried to create a patch, showing which and how to modify the routines so
they won't detect anything at all. It is at a1.patch.
