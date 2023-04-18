#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# autor jakub komárek

from scapy.all import *
from os.path import exists
from pathlib import Path
from packetsParse import PacketParse
    
if __name__ == "__main__":
    args=sys.argv
    mode=-1
    path=" "
    packetLim=-1
    try: 
        i=1     
        while i< len(args):
            arg=args[i]
            if arg== "-h" or arg=="--help":
                print(
"""Nástroj pro analýzu bittorent provozu z pcap soubori
Použití: bt-monitor -pcap <file.pcap> -init | -peers | -download
<file.pcap>: vstupní PCAP soubor
-init: vrací seznam bootstrap uzlů (IP, port)
-peers: vrací seznam aktivních uzlů - probíhal mezi nimi užitečný provoz (IP, port, node ID, # of conn)
-download: vrací podrobnosti o stahovaném souboru info_hash, size, chunks, contributes (IP+port)
-packetLim: horní limit zpracovaných paketů - volitelný argument
""")
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
                elif arg=="packetLim":
                    i+=1
                    if(i>= len(args)):
                        raise Exception("Chyba v parametrech, zkuste -h")
                    packetLim=args[i]
                else:
                    raise Exception("Chyba v parametrech, zkuste -h")
            i+=1                  
        if  path==None:
            raise Exception("Nazadal jste soubor,zkuste -h")
        elif  not(exists(Path(path)) ):
            raise Exception("Soubor neexistuje")
        elif  mode==-1:
            raise Exception("Chyba v parametrech, zkuste -h")

    except Exception as ex:
        print("Chyba:",ex)
        exit(-1)
    
    
    pcap = rdpcap(path,int(packetLim))
    packetParser=PacketParse(mode)

    for packet in pcap:
        packetParser.parsePacket(packet)

    packetParser.printResults()