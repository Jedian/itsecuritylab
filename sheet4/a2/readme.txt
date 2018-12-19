ThankYou behavior:

The app "disguise" itself as a word cloud generator that uses as input data
your sms text, your contacts'names and your calendar events.

There is a class com.fau.i1.hapra.thankyou.b that is focused on anti-emulation:
    -> It checks for existence of a shared folder (??? windows ???)
    -> It checks for existence of a bluetooth adapter and it's address
    -> It checks if it's running on bluestacks (emulator of apps)
    -> It checks in the architecture of the system

There is another class com.fau.i1.hapra.thankyou.a that seems naughty:
It opens a socket to "10.20.5.98" port 13337 and listen for incomming messages:

    If the message is "c2VuZFNNUw==" (base64 encode for "sendSMS"):
        Then the class sends a SMS to "01234561" (could be the attacker phone
        number) with the message "Hello Premiumnumber".

    If the message is "Z2V0U01T" (base64 encode for "getSMS"):
        Then the class sends a message through the socket with all the SMS
        stored in the victim's phone.

    If the message is "Z2V0TnI=" (base64 encode for "getNr"):
        Then the class sends a message through the socket with all the contacts
        stored in the victim's phone.

    Otherwise, it executes "/system/bin/sh -c " + content of the message,
    likely a command. And then sends the output to the socket. Just like a
    remote shell.

After given the permissions 
    * The app will query every contact, getting it's name and number, filling
    in the data to send when asked for "getNr" and storing it base64 encoded
    into a file "contacts.txt" and then deleting the contact.

    * Add a daily alert with the following message 'Pay ransom 1 BTC to
    BTC:XXXXXXXX to retrieve your contacts information!'

    * Will query the SMS data to fill the data to send when asked for "getSMS". 


How to improve the malware:
I believe a simple and easy improvement could be choose the message to be sent
by sms with the "remote shell", for example.
