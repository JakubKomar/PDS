#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import scapy.all as sc
from os.path import exists
from pathlib import Path
import re

class PacketParse:
    bootStrapDns ={}
    bootStrapGetPeers =[]
    bootStrapResponse=[]
    
    def __init__(self, mode):
        self.mode=mode
    
    def is_valid_ip(self,address):
        ipv4_regex = r"^(\d{1,3}\.){3}\d{1,3}$"
        ipv6_regex = r"^([\da-fA-F]{1,4}:){7}([\da-fA-F]{1,4})$"
        if re.match(ipv4_regex, address):
            return True
        elif re.match(ipv6_regex, address):
            return True
        return False



    def parsePacket(self,packet):
        try:
            if packet.haslayer(sc.UDP):
                
                if packet.haslayer(sc.DNS):
                    self.dnsParsing(packet)
                else :
                    payload=packet[sc.Raw].load
                                        
                    if len(payload)>20 and payload[0:19]==b'.BitTorrentprotocol':
                        print("handshake")
                    elif payload[0]==0x64: #d
                        if payload[1]==0x31 or payload[1]==0x32:
                            self.dhtParsing(packet,payload)
                    
                    
            elif False and packet.haslayer(sc.TCP):
                #print(packet)
                payload=packet[Raw].load
                self.bittorentParsing(packet,payload)
                    
                    
        except Exception as ex:
            ...
            print("exeption: ",ex)
            

    def dnsParsing(self,packet):
            
        if packet[sc.DNS].qr == 1:
            # extract the domain name from the response
            domain_name = packet[sc.DNSQR].qname.decode('utf-8')
            # extract the IP address from the response
            ip_address = packet[sc.DNSRR].rdata
            # print the domain name and IP address
            #print("Domain Name: ", domain_name)
            #print("IP Address: ", ip_address)
            if self.is_valid_ip(ip_address):
                self.bootStrapDns[ip_address]=domain_name

        
    def bittorentParsing(self,packet,payload):
        if payload[4]==0x04:
            print("have piece")
            print(packet)
        elif payload[4]==0x07:
            print("piece")
            print(packet)
        elif payload[4]==0x14:
            print("extended")
            print(packet)
        elif payload[4]==0x02:
            print("interested")
            print(packet)
        elif payload[4]==0x06:
            print("reguest")
            print(packet)
        elif payload[4]==0x01:
            print("unchoke")
            print(packet)
        elif payload[4]==0x00:
            print("choke")
            print(packet)
        elif payload[0]==0x13 and payload[1:20]==b'BitTorrent protocol':
            print("handshake")
            print(packet)    


    def dhtParsingPayload(self,payload):
        keyVals={}
        lastIndex=0
        for i in range(0, payload):
            if payload[i]==ord(':'):
                keyVals.append()

    def dhtParsing(self,packet,payload):
        
        if payload[1]==0x31:
            clientPacket=True
        elif payload[1]==0x32:
            clientPacket=False
            
        strList=payload.split(b':')
        
        if(self.mode==0):
            if b"y1" in strList and b"re" in strList :
                self.bootStrapResponse.append(packet[sc.IP].src)
            elif  b"get_peers1" in strList:
                self.bootStrapGetPeers.append(packet[sc.IP].dst)
    
    def printResults(self):

        if self.mode==0:
            print("Bootstraps servers:")
            for key, value in self.bootStrapDns.items():
                if key in self.bootStrapResponse or key in self.bootStrapGetPeers:
                    print(key," (",value,")",sep="")