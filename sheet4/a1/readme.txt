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

The repacked app with all the tests passed is on this folder with "signed.apk" as name.
You can see what was changed more easily by looking at the patchfile.

(In the patchfile there could still be the weird error I mentioned in the
 forum, that I could solve by copying an "attr" line from
 h4ckPr0/res/values/public.xml and moving it to the start of the file)
