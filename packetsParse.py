#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# autor jakub komárek

import scapy.all as sc
import re

class neighbor:
    """
    struktura pro ukládání sousedů
    """
    ip=None
    port=None
    
    nodeId=None
    fileHash=None
    connNum=1
    
    sendedPices=0
    sendedData=0
    recvData=0
    recvPices=0
    
    def __init__(self, ip,port,nodeId,fileHash):
        self.ip=ip
        self.port=port
        self.nodeId=nodeId
        self.fileHash=fileHash
        
    def __repr__(self):
        return "neighbor()"
    
    def __str__(self):
        if self.sendedData==0:
            ratio="0.000"
        elif  self.recvData!=0:
            ratio="%0.3f"%(self.recvData/self.sendedData)
        else:
            ratio="inf. "
        return "%-22s, NodeId: %s, Dwn/Up:%10d/%10d B, Ratio: %s, Pieces Send/recv %4d/%-4d, Connections: %2s"%(self.ip + ":" +str(self.port),self.nodeId.hex(),
            self.recvData,self.sendedData,ratio , self.recvPices,self.sendedPices ,self.connNum )
    def incUpload(self,size):
        self.sendedPices+=1
        self.sendedData+=size
    def incDownload(self,size):
            
        self.recvPices+=1
        self.recvData+=size
    def incConnections(self):
        self.connNum+=1
        
class fileStat:
    """
    struktura obsahující záznamy o stahovaném souboru
    """
    sha1=None
    maximalPieceIdex=0
    maximalPiceLen=0
    bitmapLen=0

    def __repr__(self):
        return "fileStat()"
    
    def __str__(self):
        try:
            piceNum= int(self.bitmapLen*8* (self.maximalPieceIdex/self.maximalPiceLen))
        except:
            piceNum=-1
        return "Info_hash %s, PiceSize %dB ,PiceCount %d, ChuncksCount  %d, ChunckLen  %d, Filesize %dB"% (self.sha1.hex(),self.maximalPiceLen, piceNum,self.bitmapLen*8,self.maximalPieceIdex+self.maximalPiceLen,self.bitmapLen*8* (self.maximalPieceIdex+self.maximalPiceLen ) )

    def __init__(self,srcIp,sha1 ):
        self.sha1=sha1
        self.srcIp=srcIp
                
    def setSize(self,size,offset):
        if self.maximalPiceLen<size:
            self.maximalPiceLen=size
        if self.maximalPieceIdex<offset:
            self.maximalPieceIdex=offset
    def setBitmapSize(self,size):
        self.bitmapLen=size
            
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
    peersRecv=[]
    nodesRecv=[]
    files={}
    cotributorsToFiles={}
    filesToContributors={}
    
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
            if not packet.haslayer(sc.IP):
                return
            
            ipSource=packet[sc.IP].src
            ipDest=packet[sc.IP].dst

            if packet.haslayer(sc.UDP):                 
                if packet.haslayer(sc.DNS) and packet.haslayer(sc.DNSQR) and packet.haslayer(sc.DNSRR):
                    self.dnsParsing(packet)
                else :
                    portSource=packet[sc.UDP].sport
                    portDest=packet[sc.UDP].dport
                    if not packet.haslayer(sc.Raw):
                        return
                    payload=packet[sc.Raw].load
                                        
                    if payload[0]==0x64: #d
                        if payload[1]==0x31 or payload[1]==0x32:
                            self.dhtParsing(packet,payload)   
                    elif self.mode==1 or self.mode==2:
                        self.bittorentParsing(ipSource,ipDest,portSource,portDest,payload[20:])
            elif (self.mode==1 or self.mode==2 ) and packet.haslayer(sc.TCP):
                if not packet.haslayer(sc.Raw):
                    return
                portSource=packet[sc.TCP].sport
                portDest=packet[sc.TCP].dport
                payload=packet[sc.Raw].load
                
                self.bittorentParsing(ipSource,ipDest,portSource,portDest,payload)      
                                           
        except Exception as ex:
            #print("exeption: ",ex) 
            ...

    def dnsParsing(self,packet):
        try:               
            if packet[sc.DNS].qr == 1:
                domain_name = packet[sc.DNSQR].qname.decode('utf-8')
                ip_address = packet[sc.DNSRR].rdata
                if self.is_valid_ip(ip_address):
                    self.bootStrapDns[ip_address]=domain_name
        except:
            ...

        
    def bittorentParsing(self,ipSource,ipDest,portSource,portDest,packetPayload):
        
        if packetPayload[0]==0x13 and packetPayload[1:20]==b'BitTorrent protocol': #handshake
            sha1=packetPayload[28:48]
            peerId=packetPayload[48:68]
            
            if ipSource in self.peers.keys():
                self.peers[ipSource].incConnections()
            else:
                self.peers[ipSource]=neighbor(ipSource,portSource,peerId,sha1)
             
            if not (sha1 in self.files.keys()):
                self.files[sha1]=fileStat(ipSource,sha1)


            if not (ipSource in self.cotributorsToFiles.keys()):
                self.cotributorsToFiles[ipSource]=sha1
            if not (sha1 in self.filesToContributors.keys()):   
                self.filesToContributors[sha1]=[ipSource]
            else:
                if not (ipSource in self.filesToContributors[sha1]):
                    self.filesToContributors[sha1].append(ipSource)
            
        elif ipSource in self.peers.keys():     
            shift=0
            while True:  
                if shift+4>=len(packetPayload):   
                    break                  
                lenght=int.from_bytes(packetPayload[shift:shift+4], "big") +4
                
                nokFlag=False
                if lenght+shift>len(packetPayload):
                    payload=packetPayload[shift:]
                    nokFlag=True
                else:
                    payload=packetPayload[shift:shift+lenght]
                
                
                if payload[4]==0x07:
                    size=int.from_bytes(payload[0:4], "big")
                    offset=int.from_bytes(payload[9:13], "big")
                    if size>64000: #maximální velikost je to pravděpodobně špatně
                        return
                    sha=self.cotributorsToFiles[ipSource]
                    self.files[sha].setSize(size,offset)
                                            
                    self.peers[ipSource].incUpload(size)
                    self.peers[ipDest].incDownload(size)
                elif nokFlag:
                    return
                elif payload[4]==0x05:
                    sha=self.cotributorsToFiles[ipSource]
                    size=int.from_bytes(payload[0:4], "big")-1
                    self.files[sha].setBitmapSize(size)
                """
                elif payload[4]==0x14:
                    print("extended",end=" ")                   
                elif payload[4]==0x02:
                    print("interested",end=" ")
                elif payload[4]==0x06:
                    print("reguest",end=" ")
                elif payload[4]==0x01:
                    print("unchoke",end=" ")
                elif payload[4]==0x00:
                    print("choke",end=" ")
                elif payload[4]==0x04:
                    #print("have piece",end=" ")
                    ...
                """
                shift+=lenght
                if shift>=len(packetPayload):
                    break
                
    def dhtParsing(self,packet,payload):            
        strList=payload.split(b':')
        if self.mode==0:
            if b"y1" in strList and b"re" in strList :
                self.bootStrapResponse.append(packet[sc.IP].src)
                self.bootStrapPorts[packet[sc.IP].src]=packet[sc.UDP].sport
            elif  b"get_peers1" in strList:
                self.bootStrapGetPeers.append(packet[sc.IP].dst)
                self.bootStrapPorts[packet[sc.IP].dst]=packet[sc.UDP].dport
        else:
            mesPeers=payload.split(b'6:')[1:]
            for i in mesPeers:
                ip_string = '.'.join(str(byte) for byte in i[0:4])
                port=int.from_bytes(i[4:6], "big")
                adr=ip_string+":"+str(port)
                if not(adr in self.peersRecv):
                    self.peersRecv.append(adr)
                    
            mesNodes=payload.split(b':nodes',1)[1]
            if mesNodes[0:4]==b"208:":
                nodes=8
            elif mesNodes[0:4]==b"416:":
                nodes=16
            else:
                return
            mesNodes=mesNodes[4:]
            
            i=0
            for j in range(0,nodes):                       
                if i+26>len(mesNodes):
                    break
                id=mesNodes[i+0:i+20]
                ip_string = '.'.join(str(byte) for byte in mesNodes[i+20:i+24])
                port=int.from_bytes(mesNodes[i+24:i+26], "big")
                string=("%-22s (%s)"%(ip_string+":"+str(port),id.hex()))
                if not(string in self.nodesRecv):
                    self.nodesRecv.append(string)
                i+=26    
    
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
                                    
            print("\nAll received peers:")
            
            inp="Y"
            if len( self.peersRecv   )>30:
                inp=input("Je zde %d položek, opravdu je chcete vypsat? [Y/N]"% len(self.peersRecv)  )
            if inp=="Y" or inp=="y":
                for i in self.peersRecv:
                    print(i)
                    
            print("\nAll received noodes:")
            inp="Y"
            if len( self.nodesRecv   )>30:
                inp=input("Je zde %d položek, opravdu je chcete vypsat? [Y/N]"% len(self.nodesRecv)  )
            if inp=="Y" or inp=="y":
                for i in self.nodesRecv:
                    print(i)
                
        elif self.mode==2:
            print("Files:")
            for key,file in self.files.items():
                print(file) 
                print("Contributors:")
                for value in self.filesToContributors[key]:
                    print(self.peers[value])


