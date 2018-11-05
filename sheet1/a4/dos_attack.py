#! /usr/bin/python2.7
#coding: utf-8 
import socket
import threading
import ssl
import resource
import time
import sys
from multiprocessing import Process, RawValue, Lock

resource.setrlimit(resource.RLIMIT_NOFILE, (65536, 65536))

class Counter(object):
    def __init__(self, value=0):
        self.val = RawValue('i', value)
        self.lock = Lock()

    def increment(self):
        with self.lock:
            self.val.value += 1

    def decrement(self):
        with self.lock:
            self.val.value -= 1

    def value(self):
        with self.lock:
            return self.val.value

co = Counter()

class conn(threading.Thread):
    def __init__(self, nconn, host, port):
        threading.Thread.__init__(self)
        self.nconn = nconn
        self.socket = False
        self.host = host
        self.port = port
        
    def connect(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(10)
        s = ssl.wrap_socket(s, ssl_version=ssl.PROTOCOL_TLSv1)
        try:
            s.connect((self.host, self.port))
            self.socket = s
            co.increment()
            return True
        except:
            return False
            

    def run(self):
        if self.connect():
            while True:
                if self.socket:
                    try:
                        self.socket.send('nothing'.encode())
                        time.sleep(1)
                    except:
                        co.decrement()
                        return
                else:
                    return

threads = []

def flood(number_of_connections, host, port):
    for i in range(0, number_of_connections):
        threadx = conn(i, host, port)
        threadx.daemon=True
        threads.append(threadx)
        threadx.start()

host = sys.argv[-2]
port = int(sys.argv[-1])

start_val = 300
flood(start_val, host, port)

while True:
    time.sleep(1)
    print("Total threads the server supported: " + str(co.value()))
    print("Total threads with connection not accepted yet: " + str(start_val - co.value()))
