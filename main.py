#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from scapy.all import *
from os.path import exists
from pathlib import Path
from packetsParse import PacketParse
    
if __name__ == "__main__":
    # Open the pcap file
    args=sys.argv
    mode=-1
    path=None
    try: 
        i=1
        
        while i< len(args):
            arg=args[i]
            
            if arg== "-h" or arg=="--help":
                print(
"""Použití: bt-monitor -pcap <file.pcap>|-csv <file.csv> -init | -peers | -download
<file.pcap>: input PCAP file or <file.csv> input CSV file
-init: returns a list of detected bootstrap nodes (IP, port)
-peers: returns a list of detected neighbors (IP, port, node ID, # of conn)
-download: returns file info_hash, size, chunks, contributes (IP+port) """
                )
                exit(0)
            else:
                strList=arg.split('-')
                if len(strList)<2:
                    raise Exception("Chyba v parametrech, zkuste -h")
                
                arg=strList[1]
                if arg=="pcap":
                    i+=1
                    if(i>= len(args)):
                        raise Exception("Chyba v parametrech, zkuste -h")
                    path=args[i]
                elif arg=="init":
                    if mode!=-1:
                        raise Exception("Vyberete právě jeden mód běhu, zkuste -h")
                    mode=0
                    
                elif arg=="peers":
                    if mode!=-1:
                        raise Exception("Vyberete právě jeden mód běhu, zkuste -h")
                    mode=1
                elif arg=="download":
                    if mode!=-1:
                        raise Exception("Vyberete právě jeden mód běhu, zkuste -h")
                    mode=2
                        
                else:
                    raise Exception("Chyba v parametrech, zkuste -h")
            i+=1
                       
        if  path==None:
            raise Exception("Nazadal jste soubor")
        elif  not(exists(Path(path)) ):
            raise Exception("Soubor neexistuje")

    except Exception as ex:
        print("Error:",ex)
        exit(-1)
    
    
    pcap = rdpcap(path,15000)
    packetParser=PacketParse(mode)


    # Loop through each packet and extract DHT data

    for packet in pcap:
        packetParser.parsePacket(packet)

    packetParser.printResults()