Task 4 - Denial of Service
Language: Python 2.7
File: dos_attack.py
Usage: ./dos_attack.py <HOST> <PORT>

Dependencies:
  python2.7 - apt-get install python2.7-dev

This script opens a bunch of ssl connections with the target host and tries to
keep them open. It can be used for benchmarking purposes. For now it tries to
open 300 connections, but the assigned target host can only handle 150 of them.

It's a good way of attack, because it demands small processing power, and have
great attacking power, because a server needs much more effort to deal with a
connection than a client.

I could confirm the target server was down by trying to access it through a
browser and getting time out.
