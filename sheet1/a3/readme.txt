Task 3 - Spoofing
Language: Python 2.7
File: ntpspoof.py
Usage: ./ntpspoof.py <TARGETHOST> <GATEWAYHOST>

Dependencies:
  python2.7 - apt-get install python2.7-dev
  netfilterqueue - apt-get install libnetfilter-queue-dev
  scapy - pip install scapy

This script performs a man-in-the-middle attack, spoofing packets from the
gateway to the target. If these packets are not encrypted, it's easy to read
their content and even to change it. The Network Time Protocol (NTP) is
vulnerable to this kind of attack, because the ntp packets are not encrypted.

This protocol is used for clock synchronization between systems.

To get the packets from a target before the target itself, we can spoof the arp
table on the local network, making the gateway believe we are the target, and
then forwarding the packets, modified or not, to the target, so it cannot
realise it is under attack.

In this script, we change the packets so the target believe the actual year is
2035, possibly synchronizing it's own clock to this date.
