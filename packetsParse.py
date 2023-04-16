#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# autor jakub komárek

import scapy.all as sc
from os.path import exists
from pathlib import Path
import re


class neighbor:
    """
    struktura pro ukládání sousedů
    """
    ip=None
    port=None
    nodeId=None
    order=0
    fileHash=None
    connNum=0
    sendedPices=0
    sendedData=0
    recvData=0
    recvPices=0
    
    def __init__(self, ip,port,nodeId,order,fileHash):
        self.ip=ip
        self.port=port
        self.nodeId=nodeId
        self.order=order
        self.fileHash=fileHash
        
    def __repr__(self):
        return "neighbor()"
    
    def __str__(self):
        return "%4d# %16s:%5s, InfoHash: %s Dwn/Up:%8d/%8d B, Ratio: %0.3f, Pieces Send/recv %4d/%4d, Connections: %2s"%(self.order,self.ip,self.port,self.nodeId.hex(),
            self.recvData,self.sendedData, self.sendedData/self.recvData if self.recvData!=0 else 1 , self.recvPices,self.sendedPices ,self.connNum )
    
    def incConnNum(self):
        self.connNum+=1
    
    def incData(self,sendedData):
        self.sendedData+=sendedData
        self.sendedPices+=1
        
    def incsendData(self,size):
        self.recvPices+=1
        self.recvData+=size
        
class fileStat:
    """
    struktura obsahující záznamy o stahovaném souboru
    """
    contributors=[]
    sha1=None
    pieceSize=-1
    recvPieces=0
    recvData=0

    def __repr__(self):
        return "fileStat()"
    
    def __str__(self):
        return "Info_hash %s \n\tTotaly sended pieces %d ,Totaly sended %d B, Maximal Piece Size %d B"%(self.sha1.hex(),self.recvPieces,self.recvData,self.pieceSize)

    def __init__(self,sha1,srcIp ):
        self.sha1=sha1
        self.srcIp=srcIp
    
    def addContributor(self,ip,port):
        if ip==self.srcIp:
            return
        ID=ip+":"+str(port)
        if not(ID in self.contributors ):
            self.contributors.append(ID)
            
    def setPieceSize(self,new):
        if self.pieceSize<new:
            self.pieceSize=new
            
    def incSize(self,size):
        self.recvPieces+=1
        self.recvData+=size
            
    def getSha(self):
        return self.sha1
    
    def getContributors(self):
        return self.contributors
    
    def getInitCont(self):
        return self.srcIp
            
class PacketParse:
    """
    hlavní třída nástroje 
    - ukládá v sobě potřebná data pro analýzu
    """
    bootStrapDns ={}
    bootStrapPorts ={}
    bootStrapGetPeers =[]
    bootStrapResponse=[]
    
    peers={}
    peersCnt=0
    
    idsToSha={} #pomocná hasmapa mapující ip na info hash souboru
    files={}
    
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
        """Funkce podle typu paketu vybere způsob parsování
        Args:
            packet: vstupní paket
        """
        try:
            if packet.haslayer(sc.UDP):    
                if packet.haslayer(sc.DNS):
                    self.dnsParsing(packet)
                else :
                    payload=packet[sc.Raw].load
                                        
                    if payload[0]==0x64: #d
                        if payload[1]==0x31 or payload[1]==0x32:
                            self.dhtParsing(packet,payload)           
            elif  packet.haslayer(sc.TCP):
                payload=packet[sc.Raw].load
                self.bittorentParsing(packet,payload)      
                                           
        except Exception as ex:
            ...
            #print("exeption: ",ex) 

    def dnsParsing(self,packet):        
        if packet[sc.DNS].qr == 1:
            domain_name = packet[sc.DNSQR].qname.decode('utf-8')
            ip_address = packet[sc.DNSRR].rdata
            if self.is_valid_ip(ip_address):
                self.bootStrapDns[ip_address]=domain_name

        
    def bittorentParsing(self,packet,packetPayload):
        if packetPayload[0]==0x13 and packetPayload[1:20]==b'BitTorrent protocol': #handshake
            sha1=packetPayload[28:48]
            peerId=packetPayload[48:68]
            
            ip=packet[sc.IP].dst
            port=packet[sc.TCP].dport
            
            ipSrc=packet[sc.IP].src
 
            if (self.mode==1  or self.mode==2):
                if not(ip in self.peers.keys()):
                    self.peers[ip]=neighbor(ip,port,peerId,self.peersCnt,sha1)
                    self.peersCnt+=1
                if  ipSrc in self.peers.keys():                     
                    self.peers[ip].incConnNum()
                if not(sha1 in self.files.keys() ):
                    self.files[sha1]=fileStat(sha1,ipSrc)
                self.idsToSha[ip]=sha1
                self.files[sha1].addContributor(ip,port)
        else:            
            shift=0
            while True:  
                if shift+4>=len(packetPayload):   
                    break     
                lenght=int.from_bytes(packetPayload[shift:shift+4], "big") +4
                
                if lenght+shift>len(packetPayload):
                    payload=packetPayload[shift:]
                else:
                    payload=packetPayload[shift:shift+lenght]
                
                
                if payload[4]==0x07:
                    ip=packet[sc.IP].src
                    ipDst=packet[sc.IP].dst
                    port=packet[sc.TCP].sport
                    
                    size=int.from_bytes(payload[0:4], "big")-9
                    
                    if(size>262144):
                        return                   
                    if not(ip in self.peers.keys()):
                        self.peers[ip]=neighbor(ip,port,peerId,self.peersCnt,b"")
                    self.peers[ip].incData(size)   
                    self.peers[ipDst].incsendData(size)
                    if not(ip in self.idsToSha.keys()):
                        return
                    sha=self.idsToSha[ip]                    
                    self.files[sha].setPieceSize(size)
                    self.files[sha].incSize(size)  
                    self.files[sha].addContributor(ip,port) 
                """
                elif payload[4]==0x05:
                    print("bitField")
                elif payload[0]==0x14:
                    print("extended")
                    print(packet)
                elif payload[0]==0x02:
                    print("interested")
                    print(packet)
                elif payload[0]==0x06:
                    print("reguest")
                    print(packet)
                elif payload[0]==0x01:
                    print("unchoke")
                    print(packet)
                elif payload[0]==0x00:
                    print("choke")
                    print(packet)
                elif payload[0]==0x04:
                    print("have piece")
                    print(packet)
                """
                shift+=lenght
                if shift>=len(packetPayload):
                    break
            
                
    def dhtParsing(self,packet,payload):            
        strList=payload.split(b':')
        
        if(self.mode==0):
            if b"y1" in strList and b"re" in strList :
                self.bootStrapResponse.append(packet[sc.IP].src)
                self.bootStrapPorts[packet[sc.IP].src]=packet[sc.UDP].sport
            elif  b"get_peers1" in strList:
                self.bootStrapGetPeers.append(packet[sc.IP].dst)
                self.bootStrapPorts[packet[sc.IP].dst]=packet[sc.UDP].dport
    
    def printResults(self):
        if self.mode==0:
            print("Bootstraps servers:")
            for key, value in self.bootStrapDns.items():
                if key in self.bootStrapResponse or key in self.bootStrapGetPeers:
                    port=self.bootStrapPorts[key]
                    print(key,":",port," (",value,")",sep="")
        elif self.mode==1:
            print("Active peers:")
            for key, value in self.peers.items():
                print(value)
        elif self.mode==2:
            print("Files:")
            for key, value in self.files.items():
                print(value)
                init=value.getInitCont()
                print("\tDownload begined by:\n\t",self.peers[init])
                
                contributors=value.getContributors()
                print("\tPeers:")
                for cont in contributors:
                    id=cont.split(":")[0]
                    if(id in self.peers):
                        print("\t",self.peers[id])
                    else:
                        print("\t",cont)
+