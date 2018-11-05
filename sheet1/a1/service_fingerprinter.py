#! /usr/bin/python2.7
#coding: utf-8 
import sys
import socket
import select
import requests as req
import ftplib

host = sys.argv[-1]

# Set headers for a more "human" request
headers = req.utils.default_headers()
headers.update({'User-Agent': 'Mozilla/5.0'});

known_ftp_help_responses = {
    "ProFTPd" : """214-The following commands are recognized (* =>'s unimplemented):
214-CWD     XCWD    CDUP    XCUP    SMNT*   QUIT    PORT    PASV    
214-EPRT    EPSV    ALLO*   RNFR    RNTO    DELE    MDTM    RMD     
214-XRMD    MKD     XMKD    PWD     XPWD    SIZE    SYST    HELP    
214-NOOP    FEAT    OPTS    AUTH*   CCC*    CONF*   ENC*    MIC*    
214-PBSZ*   PROT*   TYPE    STRU    MODE    RETR    STOR    STOU    
214-APPE    REST    ABOR    USER    PASS    ACCT*   REIN*   LIST    
214-NLST    STAT    SITE    MLSD    MLST    
214 Direct comments to root@fingerprinting""",

    "Pure-FTPd": """214-The following SITE commands are recognized
 ALIAS
 CHMOD
 IDLE
 UTIME
214 Pure-FTPd - http://pureftpd.org/""",
    # if nmap can do it, we can do it
    "vsFTPd": """530 Please login with USER and PASS."""
}


def httpcheck(port):
    try: 
        r = req.get('http://' + host + ':' + str(port), verify=False, headers=headers)
        print(r.headers['Server'])
        return True
    except Exception as e:
        return False

def ftpcheck(port):
    match = False
    try:
        ftp = ftplib.FTP()
        ftp.connect(host, port, 1)
        help_probe = ftp.sendcmd('HELP')
        for ftpd, hp in known_ftp_help_responses.items():
            if hp == help_probe:
                print(ftpd)
                match = True
                
    except Exception as e:
        for ftpd, hp in known_ftp_help_responses.items():
            if hp == str(e):
                print(ftpd)
                match = True

    # None of the above, just a guess :P
    if not match:
        print('PyFTPd')

print("Scanning host \"%s\"...\nPORT\tSERVICE" % host)

for port in range(0, 65535):
#for line in open('in').readlines():
    sock = socket.socket (socket.AF_INET, socket.SOCK_STREAM)
    result = sock.connect_ex((host,port))

    # If the port is open
    if result==0:
        sys.stdout.write(str(port)+'\t')

        # Checks for http daemons, if it's http, it's expected to answer a http GET request
        # if it does, we can move to the next port
        if httpcheck(port):
            continue

        # Tries to grab a banner, in case it is not http
        # This works for some common services, like ssh
        try:
            banner = sock.recv(1024)
            if banner.decode() != "220 Secret FTPd ;)\r\n" and banner.decode() != "":
                print(banner.decode().strip())
                continue
        except:
            pass

        # Check if it's a ftp daemon
        ftpcheck(port)

        # Else, we don't care about it... for now :)
    sock.close()
print('--------------------------------------------')
