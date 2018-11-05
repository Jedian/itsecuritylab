Task 2 - Sniffing
Language: Python 2.7
File: heartbleed.py
Usage: ./heartbleed.py <HOST> <PORT>

Dependencies:
  python2.7 - apt-get install python2.7-dev

This script exploits the Heartbleed Bug. This bug happens due to a
implementation fail when a server with the buggy code receive a heartbeat
request with a message on the payload. Then, the server is supposed to send the
same message back, but the buggy version does not check the size of the payload
is as it should be and ends up sending whatever is loaded in it's memory
together with the message received. The real risk right after a handshake
(opening process of a connection), when the server has just used it's private
key to decrypt it's content and the private key goes along with the message. An
attacker could use it to sniff encrypted packages it receives and gather secret
data like passwords.

I followed the guide on the assignment, implemented my version of the exploit
code, got the private key (that can be read in the file 'private_key.txt').
Then I decrypted the traffic pcap given using wireshark and could get the login
and password for the user in the email server. An interesting sent email can be
seen in the file 'email.txt'.

login_username: "d4rkh4xx0r"
secretkey: "Y0uW1llN3v3rG3tM3"
