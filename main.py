#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from scapy.all import *


def extract_dht_data(packet):
    try:
        if packet.haslayer(UDP):
            
            if packet.haslayer(DNS):
                dnsParsing(packet)
            else :
                print(packet)
                payload=packet[Raw].load
                print(payload)
                if payload[0:19]==b'.BitTorrentprotocol':
                    print("kek")
                    return
                
                dhsKek=payload[21]
                print(dhsKek=='\x00' or dhsKek=='\x01' or dhsKek=='\x0a' or dhsKek=='0x0b')
                """
                if(    "ping" (0x00)
                    "find_node" (0x01)
                    "get_peers" (0x0a)
                    "announce_peer" (0x0b))
                """
        elif False and packet.haslayer(TCP):
            #print(packet)
            payload=packet[Raw].load
            
            if payload[4]==0x04:
                print("have piece")
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
                
                
    except Exception as ex:
        ...
        #print("exeption: ",ex)
        

def dnsParsing(packet):
    ...
    
def bittorentParsing(packet):
    ...    

def dhtParsing(packet):
    ...
    
if __name__ == "__main__":
    # Open the pcap file
    pcap = rdpcap("logs/firstRun.pcapng",15000)

    # Loop through each packet and extract DHT data

    for packet in pcap:
        extract_dht_data(packet)
