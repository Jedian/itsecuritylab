import os, sys, socket, struct, select, time, string, argparse

class Icmpclient:
    def __init__(self, ID=None, dest=None):
        self.id = ID
        self.dest = dest
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.getprotobyname("icmp"))

    def checksum(self, source_string):
        sum = 0
        countTo = (len(source_string)/2)*2
        count = 0
        while count<countTo:
            thisVal = ord(source_string[count + 1])*256 + ord(source_string[count])
            sum = sum + thisVal
            sum = sum & 0xffffffff
            count = count + 2
        if countTo<len(source_string):
            sum = sum + ord(source_string[len(source_string) - 1])
            sum = sum & 0xffffffff
        sum = (sum >> 16)  +  (sum & 0xffff)
        sum = sum + (sum >> 16)
        answer = ~sum
        answer = answer & 0xffff
        return answer

    def send(self, message):
        pkg = struct.pack("bbHHh", 0, 0, 0, self.id, 1) + message
        checks = self.checksum(pkg)
        pkg = struct.pack("bbHHh", 0, 0, checks, self.id, 1) + message
        self.socket.sendto(pkg, (self.dest, 1))

    def recv(self, timeout):
        timeleft = timeout
        while True:
            if timeleft <= 0:
                return "N0TH1NG"
            starttimes = time.time()
            stat = select.select([self.socket], [], [], timeleft)
            howlong = time.time() - starttimes
            if stat[0] == []:
                timeleft = timeleft - howlong
                continue

            pkg, addr = self.socket.recvfrom(10240)
            header = pkg[20:28]
            data = pkg[28:]
            type, code, checksum, packetID, sequence = struct.unpack("bbHHh", header)

            if "Login" in data:
                self.dest = addr[0]
                self.id = packetID
                return data
            else:
                if self.id != None:
                    return data

            timeleft = timeleft - howlong

