# Monitoring of BitTorrent Traffic in LAN
# PDS project
# Academic year 2022/2023
# autor: Bc. Jakub Komárek

inicializace:
  make 
  - pro incializaci venv a stažení knihoven, tento krok bude chvíli trvat

spuštení:
    - virtuální prostředí venv
    make run ARGS="-pcap <file.pcap>  [-init | -peers | -download] | -packetLim  | -h"
    nebo 
    - spuštění bez venv - musí se dostahovat knihovny
    python3 bt-monitor -pcap <file.pcap> [-init | -peers | -download] | -packetLim  | -h

Argumenty: 
<file.pcap>: vstupní PCAP soubor
-init: vrací seznam bootstrap uzlů (IP, port)
-peers: vrací seznam aktivních uzlů - probíhal mezi nimi užitečný provoz (IP, port, node ID, # of conn)
-download: vrací podrobnosti o stahovaném souboru info_hash, size, chunks, contributes (IP+port)
-packetLim: horní limit zpracovaných paketů - volitelný argument
-h: help

vyžadované knihovny: 
    - pokud použijete příkaz make, dostahuje se automaticky - je za potřebí mít podporu virtuálních prostředí venv
    - instalace venv: sudo apt install python3.8-venv
    - jinak dostahujte požadované knihovny ručně

    scapy>= 2.5.0


ukázky spuštění:

make run ARGS="-pcap logs/downloadOnly.pcapng  -init -packetLim 25000"
venv/bin/python3 main.py -pcap logs/downloadOnly.pcapng  -init -packetLim 25000
Bootstraps servers:
185.157.221.247:25401 (dht.libtorrent.org.)
67.215.246.10:6881 (router.bittorrent.com.)
82.221.103.244:6881 (router.utorrent.com.)
185.125.190.59:6926 (torrent.ubuntu.com.)


make run ARGS="-pcap logs/downloadOnly.pcapng  -peers -packetLim 40000"
venv/bin/python3 main.py -pcap logs/downloadOnly.pcapng  -peers -packetLim 40000
Active peers:
   0#   185.125.190.59: 6926, InfoHash: 2d7142343532302d577232304937794a626c2146 Dwn/Up:       0/   81920 B, Ratio: 1.000, Pieces Send/recv    0/   5, Connections:  0
   1#  192.168.226.128:57799, InfoHash: 543033492d2d3031302e6863576a6c6743563567 Dwn/Up:  540672/       0 B, Ratio: 0.000, Pieces Send/recv   33/   0, Connections:  5
   2#    89.134.88.185: 9916, InfoHash: 2d7142343532302d6d73314a5846463046546733 Dwn/Up:       0/  344064 B, Ratio: 1.000, Pieces Send/recv    0/  21, Connections:  1
   3#       5.79.77.54:55686, InfoHash: 2d7142343532302d287043497374623075502831 Dwn/Up:       0/   98304 B, Ratio: 1.000, Pieces Send/recv    0/   6, Connections:  1
   4#    66.63.167.116:60243, InfoHash: 2d7142343532302d456d457a722e37312d493348 Dwn/Up:       0/   16384 B, Ratio: 1.000, Pieces Send/recv    0/   1, Connections:  1
   5#    165.22.47.211:63793, InfoHash: 2d7142343532302d2d4363422a677a3770364c4c Dwn/Up:       0/       0 B, Ratio: 1.000, Pieces Send/recv    0/   0, Connections:  1
   6#  123.129.130.103:10086, InfoHash: 2d7142343532302d4d5845686937725643777e32 Dwn/Up:       0/       0 B, Ratio: 1.000, Pieces Send/recv    0/   0, Connections:  1


/mnt/c/workSpace/PDS# make run ARGS="-pcap logs/downloadOnly.pcapng  -download -packetLim 40000"
venv/bin/python3 main.py -pcap logs/downloadOnly.pcapng  -download -packetLim 40000
Files:
Info_hash 99c82bb73505a3c0b453f9fa0e881d6e5a32a0c1
Totaly sended pieces 33 ,Totaly sended 540672 B, Maximal Piece Size 16384 B
Download begined by:
    1#  192.168.226.128:57799, InfoHash: 543033492d2d3031302e6863576a6c6743563567 Dwn/Up:  540672/       0 B, Ratio: 0.000, Pieces Send/recv   33/   0, Connections:  5
Peers:
   0#   185.125.190.59: 6926, InfoHash: 2d7142343532302d577232304937794a626c2146 Dwn/Up:       0/   81920 B, Ratio: 1.000, Pieces Send/recv    0/   5, Connections:  0
   2#    89.134.88.185: 9916, InfoHash: 2d7142343532302d6d73314a5846463046546733 Dwn/Up:       0/  344064 B, Ratio: 1.000, Pieces Send/recv    0/  21, Connections:  1
   3#       5.79.77.54:55686, InfoHash: 2d7142343532302d287043497374623075502831 Dwn/Up:       0/   98304 B, Ratio: 1.000, Pieces Send/recv    0/   6, Connections:  1
   4#    66.63.167.116:60243, InfoHash: 2d7142343532302d456d457a722e37312d493348 Dwn/Up:       0/   16384 B, Ratio: 1.000, Pieces Send/recv    0/   1, Connections:  1
   5#    165.22.47.211:63793, InfoHash: 2d7142343532302d2d4363422a677a3770364c4c Dwn/Up:       0/       0 B, Ratio: 1.000, Pieces Send/recv    0/   0, Connections:  1
   6#  123.129.130.103:10086, InfoHash: 2d7142343532302d4d5845686937725643777e32 Dwn/Up:       0/       0 B, Ratio: 1.000, Pieces Send/recv    0/   0, Connections:  1