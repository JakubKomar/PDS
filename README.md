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
    python3 main.py -pcap <file.pcap> [-init | -peers | -download] | -packetLim  | -h

Argumenty: 
-pcap <file.pcap>: vstupní PCAP soubor
-init: vrací seznam bootstrap uzlů (IP, port)
-peers: vrací seznam aktivních uzlů - probíhal mezi nimi užitečný provoz (IP, port, node ID, # of conn), následně všechny nazbírané noodes a peers
-download: vrací podrobnosti o stahovaném souboru info_hash, size, chunks, contributes (IP+port)
-packetLim: horní limit zpracovaných paketů - volitelný argument
-h: help

vyžadované knihovny: 
    - pokud použijete příkaz make, dostahuje se automaticky - je za potřebí mít podporu virtuálních prostředí venv
    - instalace venv: sudo apt install python3.8-venv
    - jinak dostahujte požadované knihovny ručně

    scapy>= 2.5.0

všechny testovací pcapy:
https://owncloud.cesnet.cz/index.php/s/1UmBhvoEB5rUlWv


ukázky spuštění:

# make run ARGS="-pcap logs/firstRun.pcapng  -init -packetLim 25000"
185.157.221.247:25401 (dht.libtorrent.org.)
67.215.246.10:6881 (router.bittorrent.com.)
82.221.103.244:6881 (router.utorrent.com.)
185.125.190.59:6926 (torrent.ubuntu.com.)

# make run ARGS=" -pcap logs/downloadSmall.pcapng  -peers"
Active peers:
192.168.226.128:40985 , NodeId: 2d7142343532302d5129504a6162747862294b61, Dwn/Up:    196716/         0 B, Ratio: 0.000, Pieces Send/recv   12/0   , Connections:  1
90.64.243.162:33232   , NodeId: 2d7142343530302d374a6a545072415972625439, Dwn/Up:         0/    196716 B, Ratio: inf. , Pieces Send/recv    0/12  , Connections:  1

All received peers:
147.229.196.19:63309
118.97.108.117:25971
31.30.172.6:26431
90.64.243.162:33232
31.30.167.111:15772
90.180.146.238:51679
93.91.246.175:15997
78.99.92.144:54321
178.255.168.212:28962
31.30.172.6:1
90.64.243.162:1
110.111.115.101:25956

All received noodes:
Je zde 293 položek, opravdu je chcete vypsat? [Y/N]y
49.164.195.61:61244    (734e160222efd5923f7b0670b505eebce00f1f2e)
211.58.127.63:59170    (7221c6711e541eb878ef897250cf0aacd05abd3d)
49.167.15.86:40718     (712fb1fb892aee1e009d3ff86f8bf1ae6e0b66a8)
72.34.105.232:54321    (700f37dc794bbb45c53b53801b861cd40b485873)
78.190.148.140:54030   (773fd3b2f48a551b6174c50c3907cf60bae3a9f9)
                            ...

# make run ARGS="-pcap logs/downloadSmall.pcapng  -download"
Files:
Info_hash 99c82bb73505a3c0b453f9fa0e881d6e5a32a0c1, PiceSize 16393B , PiceCount 232912, Filesize 4072809008B
Contributors:
 192.168.226.128:40985, NodeId: 2d7142343532302d704d6f636f287e5a34723570, Dwn/Up:12713297/       0 B, Ratio: 0.000, Pieces Send/recv  776/   0, Connections: 143
   90.120.136.31:13866, NodeId: 2d7142343235302d5a2e4c6d616d744b476f472e, Dwn/Up:       0/   16393 B, Ratio: inf. , Pieces Send/recv    0/   1, Connections:  1
    85.140.32.57:50505, NodeId: 2d5554333630572d92b6e35f095dfe8de0ccdab4, Dwn/Up:       0/   65572 B, Ratio: inf. , Pieces Send/recv    0/   4, Connections:  1
 184.145.159.241:39150, NodeId: 2d5554333630572d92b6ee559cb08b35f64c4c6b, Dwn/Up:       0/  131144 B, Ratio: inf. , Pieces Send/recv    0/   8, Connections:  1
  80.109.142.237:48714, NodeId: 2d7142343532302d5f30302e34357e5547575555, Dwn/Up:       0/   65572 B, Ratio: inf. , Pieces Send/recv    0/   4, Connections:  1
  23.114.235.154:16572, NodeId: 2d4c54313042302d2a535a676379482e4a6a774a, Dwn/Up:       0/   49179 B, Ratio: inf. , Pieces Send/recv    0/   3, Connections:  1
   194.26.196.92:25871, NodeId: 2d7142343531302d66564c2e394c2a6279653143, Dwn/Up:       0/  213109 B, Ratio: inf. , Pieces Send/recv    0/  13, Connections:  1
   93.103.164.98:62349, NodeId: 2d5554333630572d92b6d7e62cc0435461cd8be3, Dwn/Up:       0/  147537 B, Ratio: inf. , Pieces Send/recv    0/   9, Connections:  1
  177.37.193.185:44206, NodeId: 2d55573133304b2d5f6f4641455f2e337321502e, Dwn/Up:       0/   49179 B, Ratio: inf. , Pieces Send/recv    0/   3, Connections:  1
    37.187.20.70:31673, NodeId: 2d5554333330422d06774eee56ef4be9a8bf5cec, Dwn/Up:       0/   65572 B, Ratio: inf. , Pieces Send/recv    0/   4, Connections:  1
    78.133.78.75: 6881, NodeId: 2d55573133304b2d6245305f6d5357524d725135, Dwn/Up:       0/   49179 B, Ratio: inf. , Pieces Send/recv    0/   3, Connections:  1
   139.64.134.10:58620, NodeId: 2d7142343431302d396244305f4b456274667e30, Dwn/Up:       0/   81965 B, Ratio: inf. , Pieces Send/recv    0/   5, Connections:  1
  179.61.197.192:44209, NodeId: 2d4445323131732d214878514c59627e732e5244, Dwn/Up:       0/   32786 B, Ratio: inf. , Pieces Send/recv    0/   2, Connections:  1
  185.125.190.59: 6926, NodeId: 543033492d2d3031302e6863576a6c6743563567, Dwn/Up:       0/  901615 B, Ratio: inf. , Pieces Send/recv    0/  55, Connections:  1
  81.170.154.139:60012, NodeId: 2d7142343532302d414853726262357250764269, Dwn/Up:       0/   81965 B, Ratio: inf. , Pieces Send/recv    0/   5, Connections:  1
      79.26.3.66:59006, NodeId: 2d4445323033732d34587a6671726d705a335831, Dwn/Up:       0/   65572 B, Ratio: inf. , Pieces Send/recv    0/   4, Connections:  1
    5.18.171.250: 3084, NodeId: 2d4254376230572d5bb616aec858ce5afadd09ea, Dwn/Up:       0/  114751 B, Ratio: inf. , Pieces Send/recv    0/   7, Connections:  1
 186.249.201.167: 6881, NodeId: 2d55573133304b2d39672865434a775221772e2e, Dwn/Up:       0/   16393 B, Ratio: inf. , Pieces Send/recv    0/   1, Connections:  1
   89.134.88.185: 9916, NodeId: 2d5554333630572d92b69ca877bc82ada8c12e7b, Dwn/Up:       0/  360646 B, Ratio: inf. , Pieces Send/recv    0/  22, Connections:  1
   216.16.84.237:33839, NodeId: 2d5554333630572d92b66eef7ed8751495d8a993, Dwn/Up:       0/   81965 B, Ratio: inf. , Pieces Send/recv    0/   5, Connections:  1
    37.113.3.220:59847, NodeId: 2d4445323033732d55737053464e41662a357937, Dwn/Up:       0/  147537 B, Ratio: inf. , Pieces Send/recv    0/   9, Connections:  1
   47.207.36.155: 9288, NodeId: 2d7142343530302d6a772e5a4e6b687e305a2e5f, Dwn/Up:       0/   65572 B, Ratio: inf. , Pieces Send/recv    0/   4, Connections:  1
 176.176.153.143:42767, NodeId: 2d7142343339302d4d6c50566d79626a74634e29, Dwn/Up:       0/       0 B, Ratio: 0.000, Pieces Send/recv    0/   0, Connections:  1
   179.109.45.56:17461, NodeId: 2d55573133304b2d21295672626f39655f63314b, Dwn/Up:       0/   81965 B, Ratio: inf. , Pieces Send/recv    0/   5, Connections:  1
      5.79.77.54:55686, NodeId: 2d4445313346302d724358427144514a56762d38, Dwn/Up:       0/  107080 B, Ratio: inf. , Pieces Send/recv    0/   7, Connections:  1
     37.17.234.6:19005, NodeId: 2d7142343433312d4c706145334a427271472a75, Dwn/Up:       0/   49179 B, Ratio: inf. , Pieces Send/recv    0/   3, Connections:  1
  178.167.12.145:38462, NodeId: 2d7142343435302d632d3021356f38554836294e, Dwn/Up:       0/  114751 B, Ratio: inf. , Pieces Send/recv    0/   7, Connections:  1
   66.63.167.116:60243, NodeId: 2d7142343532302d584c4e4b78743435444d4d5a, Dwn/Up:       0/   32786 B, Ratio: inf. , Pieces Send/recv    0/   2, Connections:  1
     68.57.15.89:15546, NodeId: 2d5554333630572d7cb6209b3944a9149d203577, Dwn/Up:       0/  147537 B, Ratio: inf. , Pieces Send/recv    0/   9, Connections:  1
   165.22.47.211:63793, NodeId: 2d4445323131732d61482e504646736579397e30, Dwn/Up:       0/  360646 B, Ratio: inf. , Pieces Send/recv    0/  22, Connections:  1
  67.149.146.103: 1797, NodeId: 2d7142343532302d6a73344e56615a7866654b31, Dwn/Up:       0/  262288 B, Ratio: inf. , Pieces Send/recv    0/  16, Connections:  1
   91.148.94.123:65061, NodeId: 2d7142343532302d496f76486349674b21394566, Dwn/Up:       0/  229502 B, Ratio: inf. , Pieces Send/recv    0/  14, Connections:  1
  181.41.202.214:31798, NodeId: 2d4445323131732d5a714b78546336594870684e, Dwn/Up:       0/   98358 B, Ratio: inf. , Pieces Send/recv    0/   6, Connections:  1
      5.147.49.5:47470, NodeId: 2d7142343532302d7a554b6e635a5a364f526958, Dwn/Up:       0/  278681 B, Ratio: inf. , Pieces Send/recv    0/  17, Connections:  1
  188.17.116.156:43849, NodeId: 2d5554333535572d44b440fa5e01a60d4f9bdc76, Dwn/Up:       0/  180323 B, Ratio: inf. , Pieces Send/recv    0/  11, Connections:  1
   173.30.203.73: 6881, NodeId: 2d7142343532302d79672d6152312d284a315f65, Dwn/Up:       0/   81965 B, Ratio: inf. , Pieces Send/recv    0/   5, Connections:  2
    5.196.74.194:51102, NodeId: 2d6c74304438302d22b69d1e2b1916a4bd2b89cc, Dwn/Up:       0/   49179 B, Ratio: inf. , Pieces Send/recv    0/   3, Connections:  1
   145.236.6.116: 6881, NodeId: 2d42573133304b2d647e63675877523078377458, Dwn/Up:       0/   65572 B, Ratio: inf. , Pieces Send/recv    0/   4, Connections:  1
   80.229.30.166:53979, NodeId: 2d4445323035732d71624678304d7a3272683641, Dwn/Up:       0/   16393 B, Ratio: inf. , Pieces Send/recv    0/   1, Connections:  1
   91.236.156.69:44743, NodeId: 2d7142343531302d506759425453377452546d51, Dwn/Up:       0/   98358 B, Ratio: inf. , Pieces Send/recv    0/   6, Connections:  1
  109.195.51.115:45184, NodeId: 2d7142343435302d5773454c6250754f3772484d, Dwn/Up:       0/   16393 B, Ratio: inf. , Pieces Send/recv    0/   1, Connections:  2
  89.250.167.234: 7177, NodeId: 2d55573133304b2d7a72343828574659484e6245, Dwn/Up:       0/  114751 B, Ratio: inf. , Pieces Send/recv    0/   7, Connections:  1
  89.212.207.169:36217, NodeId: 2d7142343531302d322d7e6947504e38656d3138, Dwn/Up:       0/  295074 B, Ratio: inf. , Pieces Send/recv    0/  18, Connections:  1
 217.107.124.170: 1795, NodeId: 2d7142343333302d62314b546556305f4a327337, Dwn/Up:       0/   16393 B, Ratio: inf. , Pieces Send/recv    0/   1, Connections:  1
    77.139.16.17:10292, NodeId: 2d5554333535572d06b2ee48f39bc87bced13bbc, Dwn/Up:       0/   81965 B, Ratio: inf. , Pieces Send/recv    0/   5, Connections:  1
  45.152.182.136:32802, NodeId: 2d7142343532302d754c674b394c2d2865386973, Dwn/Up:       0/   32786 B, Ratio: inf. , Pieces Send/recv    0/   2, Connections:  1
   83.149.84.133:15167, NodeId: 2d4445323033732d687e576744486d3531563177, Dwn/Up:       0/  147537 B, Ratio: inf. , Pieces Send/recv    0/   9, Connections:  1
   136.35.138.88:38355, NodeId: 2d7142343531302d29435966314f4d3348564d64, Dwn/Up:       0/   16393 B, Ratio: inf. , Pieces Send/recv    0/   1, Connections:  1
 190.131.210.202:25346, NodeId: 2d4c54313030302d5447216f302e574759677454, Dwn/Up:       0/   32786 B, Ratio: inf. , Pieces Send/recv    0/   2, Connections:  1
     86.60.208.2: 7760, NodeId: 2d7142343532302d4c746657574277526338336f, Dwn/Up:       0/  360646 B, Ratio: inf. , Pieces Send/recv    0/  22, Connections:  1
   32.220.98.185:51438, NodeId: 2d6c74304438302de24701be6434288b93d5140e, Dwn/Up:       0/   32786 B, Ratio: inf. , Pieces Send/recv    0/   2, Connections:  1
  174.29.180.130: 6881, NodeId: 2d4c54304748302d736c754b776a2d7843747953, Dwn/Up:       0/   16393 B, Ratio: inf. , Pieces Send/recv    0/   1, Connections:  1
     68.104.20.8:22771, NodeId: 2d7142343435302d584870626e7e6347484c2e46, Dwn/Up:       0/   32786 B, Ratio: inf. , Pieces Send/recv    0/   2, Connections:  1
 178.174.148.253:22988, NodeId: 2d7142343532302d4677783531436b724954547e, Dwn/Up:       0/   32786 B, Ratio: inf. , Pieces Send/recv    0/   2, Connections:  1
    154.61.57.50:50449, NodeId: 2d7142343530302d69763376575f324e43475653, Dwn/Up:       0/  508183 B, Ratio: inf. , Pieces Send/recv    0/  31, Connections:  1
    50.67.58.116:49442, NodeId: 2d4254376230572d5bb66b7d0bbdc669b5b899b7, Dwn/Up:       0/   32786 B, Ratio: inf. , Pieces Send/recv    0/   2, Connections:  1
  27.125.183.241:49384, NodeId: 2d4445323131732d6b644479392e527558706c58, Dwn/Up:       0/       0 B, Ratio: 0.000, Pieces Send/recv    0/   0, Connections:  1
  107.189.14.246: 4533, NodeId: 2d7142343532302d6b2d35526b6931536158516c, Dwn/Up:       0/   49179 B, Ratio: inf. , Pieces Send/recv    0/   3, Connections:  2
     82.66.19.76: 7134, NodeId: 2d4658303230302d4ba1e46e3dd6289002d337a0, Dwn/Up:       0/  901615 B, Ratio: inf. , Pieces Send/recv    0/  55, Connections:  1
    92.52.202.51:53721, NodeId: 2d7142343530302d486855774d315f2870666e67, Dwn/Up:       0/   32786 B, Ratio: inf. , Pieces Send/recv    0/   2, Connections:  1
 185.195.233.144:56730, NodeId: 2d7142343531302d79436e305429374b42503461, Dwn/Up:       0/   65572 B, Ratio: inf. , Pieces Send/recv    0/   4, Connections:  1
    107.4.110.17: 3854, NodeId: 2d5554323231302d1662145c2dfe7421eb1a3ec0, Dwn/Up:       0/  180323 B, Ratio: inf. , Pieces Send/recv    0/  11, Connections:  1
 184.147.189.195:41739, NodeId: 2d7142343532302d58794c71735968486e726746, Dwn/Up:       0/   81965 B, Ratio: inf. , Pieces Send/recv    0/   5, Connections:  1
     79.47.60.82:26282, NodeId: 2d4c54313242302d58303167554830662175636c, Dwn/Up:       0/  540969 B, Ratio: inf. , Pieces Send/recv    0/  33, Connections:  1
    68.235.43.12:13283, NodeId: 2d7142343435302d436229352d545f316c537148, Dwn/Up:       0/   16393 B, Ratio: inf. , Pieces Send/recv    0/   1, Connections:  1
  163.172.50.202:49152, NodeId: 2d4445323131732d75462a585529384a74614638, Dwn/Up:       0/  295074 B, Ratio: inf. , Pieces Send/recv    0/  18, Connections:  1
  184.68.216.134:30097, NodeId: 2d7142343532302d4865446921444c7e456d2d79, Dwn/Up:       0/   65572 B, Ratio: inf. , Pieces Send/recv    0/   4, Connections:  1
    185.9.19.107:51037, NodeId: 2d7142343532302d6f3228323679355932286528, Dwn/Up:       0/  245895 B, Ratio: inf. , Pieces Send/recv    0/  15, Connections:  1
    86.49.242.71:61211, NodeId: 2d4c54313242302d32482d6539345950506e2a77, Dwn/Up:       0/   32786 B, Ratio: inf. , Pieces Send/recv    0/   2, Connections:  1
   95.181.238.55:47205, NodeId: 544958303331312d693465326934623567356236, Dwn/Up:       0/   49179 B, Ratio: inf. , Pieces Send/recv    0/   3, Connections:  1
 188.130.149.176:41388, NodeId: 2d5554323030302d784707881e938a10abecf6ce, Dwn/Up:       0/   98358 B, Ratio: inf. , Pieces Send/recv    0/   6, Connections:  1
    70.66.209.41:22333, NodeId: 2d7142343530302d2a504a342d2e304573773536, Dwn/Up:       0/  180323 B, Ratio: inf. , Pieces Send/recv    0/  11, Connections:  1
    59.66.203.65:28898, NodeId: 2d7142343532302d314a30654d59304735547e32, Dwn/Up:       0/   32786 B, Ratio: inf. , Pieces Send/recv    0/   2, Connections:  1
   89.35.141.253: 4672, NodeId: 2d7142343532302d394e6a69525a7735427e5577, Dwn/Up:       0/       0 B, Ratio: 0.000, Pieces Send/recv    0/   0, Connections:  1
  156.146.62.209:37981, NodeId: 2d4445323131732d446b643569537079362e7669, Dwn/Up:       0/   32786 B, Ratio: inf. , Pieces Send/recv    0/   2, Connections:  1
 109.201.152.162:55272, NodeId: 2d7142343532302d66596f697a773259454c6361, Dwn/Up:       0/   81965 B, Ratio: inf. , Pieces Send/recv    0/   5, Connections:  1
  45.152.182.230:65260, NodeId: 2d7142343433312d664c744a47507554762d7845, Dwn/Up:       0/   98358 B, Ratio: inf. , Pieces Send/recv    0/   6, Connections:  1
 111.237.115.101:47372, NodeId: 2d7142343530412d4c665664704e6f7e792e6347, Dwn/Up:       0/   65572 B, Ratio: inf. , Pieces Send/recv    0/   4, Connections:  1
  121.62.175.134:39889, NodeId: 2d7142343332302d6d715469416d77612e364d4d, Dwn/Up:       0/   32786 B, Ratio: inf. , Pieces Send/recv    0/   2, Connections:  1
   173.76.190.86:19650, NodeId: 2d7142343431302d477e365a496e74696c317a6b, Dwn/Up:       0/   32786 B, Ratio: inf. , Pieces Send/recv    0/   2, Connections:  1
     87.176.1.96:48403, NodeId: 2d7142343530302d4c354d78344162432a425670, Dwn/Up:       0/  180323 B, Ratio: inf. , Pieces Send/recv    0/  11, Connections:  1
  213.48.243.211:24171, NodeId: 2d7142343532302d504644393169796f707a4e28, Dwn/Up:       0/  213109 B, Ratio: inf. , Pieces Send/recv    0/  13, Connections:  1
   37.21.225.219:59980, NodeId: 2d7142343532302d675a644b6b214f3644743943, Dwn/Up:       0/       0 B, Ratio: 0.000, Pieces Send/recv    0/   0, Connections:  1
   185.37.58.171:20981, NodeId: 2d7142343532302d704b4c527165545929334734, Dwn/Up:       0/   32786 B, Ratio: inf. , Pieces Send/recv    0/   2, Connections:  1
  24.194.181.159: 6881, NodeId: 2d4257313130512d49484f21547674657a324967, Dwn/Up:       0/   49179 B, Ratio: inf. , Pieces Send/recv    0/   3, Connections:  1
   72.212.32.122:22222, NodeId: 2d7142343532302d554a5a3569627a34776a7e69, Dwn/Up:       0/   32786 B, Ratio: inf. , Pieces Send/recv    0/   2, Connections:  1
  109.202.200.73:58945, NodeId: 2d7142343532302d30476334644d5a774a5f6658, Dwn/Up:       0/   32786 B, Ratio: inf. , Pieces Send/recv    0/   2, Connections:  1
  109.60.232.157:21483, NodeId: 2d7142343432302d55364b723569296d75722e4e, Dwn/Up:       0/   32786 B, Ratio: inf. , Pieces Send/recv    0/   2, Connections:  1
   178.137.50.28:22010, NodeId: 2d5554333535532dceb54c7e4a0dd8b7615bd1de, Dwn/Up:       0/   49179 B, Ratio: inf. , Pieces Send/recv    0/   3, Connections:  1
   38.240.226.19:49544, NodeId: 2d7142343339302d287145295741645842456458, Dwn/Up:       0/   32786 B, Ratio: inf. , Pieces Send/recv    0/   2, Connections:  1
   35.197.15.172: 6881, NodeId: 2d7142343530302d7074215a634a4d3338635767, Dwn/Up:       0/   65572 B, Ratio: inf. , Pieces Send/recv    0/   4, Connections:  1
     223.64.65.1: 7492, NodeId: 2d7142343135302d5f515763374c66615478477e, Dwn/Up:       0/   16393 B, Ratio: inf. , Pieces Send/recv    0/   1, Connections:  1
 188.156.194.186:64029, NodeId: 2d5554333630572d92b63d65b4a6e0471cf79ed2, Dwn/Up:       0/   32786 B, Ratio: inf. , Pieces Send/recv    0/   2, Connections:  1
 185.213.155.192:59998, NodeId: 2d7142343532302d6655294f7461467537754673, Dwn/Up:       0/   16393 B, Ratio: inf. , Pieces Send/recv    0/   1, Connections:  1
 181.214.206.233:41629, NodeId: 2d7142343532302d436e6b6d422e4d637845454f, Dwn/Up:       0/   16393 B, Ratio: inf. , Pieces Send/recv    0/   1, Connections:  1
   91.207.249.40:17582, NodeId: 2d7142343532302d374974386c3170447932774c, Dwn/Up:       0/  360646 B, Ratio: inf. , Pieces Send/recv    0/  22, Connections:  1
    61.140.44.27:21394, NodeId: 2d7142343532412d5149347771746a6271483967, Dwn/Up:       0/   16393 B, Ratio: inf. , Pieces Send/recv    0/   1, Connections:  1
  91.170.227.161: 7735, NodeId: 2d4658303230302d4dcecd590a4cc618f843a262, Dwn/Up:       0/  442611 B, Ratio: inf. , Pieces Send/recv    0/  27, Connections:  1
  158.174.111.90:63311, NodeId: 2d4249333330302d4f656961464f534f497a6d37, Dwn/Up:       0/       0 B, Ratio: 0.000, Pieces Send/recv    0/   0, Connections:  1
   146.70.134.87:56419, NodeId: 2d7142343431302d7a5154764e64562e576c316a, Dwn/Up:       0/   65572 B, Ratio: inf. , Pieces Send/recv    0/   4, Connections:  1
     84.17.42.26: 6881, NodeId: 2d7142343531302d7a3776396f6971656f547966, Dwn/Up:       0/  114751 B, Ratio: inf. , Pieces Send/recv    0/   7, Connections:  1
  59.172.119.217:24917, NodeId: 2d7142343532412d702a304a4c75586472433858, Dwn/Up:       0/  114751 B, Ratio: inf. , Pieces Send/recv    0/   7, Connections:  1
    98.33.196.50: 6881, NodeId: 2d55573133304b2d485951453335662a5a4f7768, Dwn/Up:       0/       0 B, Ratio: 0.000, Pieces Send/recv    0/   0, Connections:  1
  107.181.189.57:32444, NodeId: 2d7142343532302d4942616432215365434f5050, Dwn/Up:       0/   32786 B, Ratio: inf. , Pieces Send/recv    0/   2, Connections:  1
   149.28.46.217:63552, NodeId: 2d7142343235302d525975387e614f4b354c384b, Dwn/Up:       0/   16393 B, Ratio: inf. , Pieces Send/recv    0/   1, Connections:  1
  146.59.157.102: 1688, NodeId: 2d4445313346302d417177757472647e7442455f, Dwn/Up:       0/   16393 B, Ratio: inf. , Pieces Send/recv    0/   1, Connections:  1
 176.124.204.176:17694, NodeId: 2d7142343532302d5369397335582d70714a4167, Dwn/Up:       0/  245895 B, Ratio: inf. , Pieces Send/recv    0/  15, Connections:  1
    212.7.200.12:54768, NodeId: 2d4445323131732d727177734f3063726b477078, Dwn/Up:       0/  180323 B, Ratio: inf. , Pieces Send/recv    0/  11, Connections:  1
     5.13.71.211:31067, NodeId: 2d7142343435302d796d31437832375058637a6a, Dwn/Up:       0/   49179 B, Ratio: inf. , Pieces Send/recv    0/   3, Connections:  1
   62.219.164.15:58462, NodeId: 2d7142343431302d71566d655543793379297842, Dwn/Up:       0/   32786 B, Ratio: inf. , Pieces Send/recv    0/   2, Connections:  1
  170.133.11.210:56475, NodeId: 2d7142343532302d4f56474261325270442d434f, Dwn/Up:       0/   49179 B, Ratio: inf. , Pieces Send/recv    0/   3, Connections:  1
  168.91.247.225:63885, NodeId: 2d7142343435302d4f32323872327a2e297e2133, Dwn/Up:       0/   16393 B, Ratio: inf. , Pieces Send/recv    0/   1, Connections:  1
 180.157.169.134:55556, NodeId: 2d7142343532302d6352475946625a393821794f, Dwn/Up:       0/   32786 B, Ratio: inf. , Pieces Send/recv    0/   2, Connections:  1
    79.142.79.40:39584, NodeId: 2d7142343338302d42497057562a74376a716274, Dwn/Up:       0/   16393 B, Ratio: inf. , Pieces Send/recv    0/   1, Connections:  1
     81.64.57.80: 6881, NodeId: 2d42573133304b2d7437504d65433048655a6b2a, Dwn/Up:       0/   16393 B, Ratio: inf. , Pieces Send/recv    0/   1, Connections:  1
   72.241.31.208:17437, NodeId: 2d7142343532302d7876496c315a4c3476296761, Dwn/Up:       0/   16393 B, Ratio: inf. , Pieces Send/recv    0/   1, Connections:  1
     64.44.84.39: 8047, NodeId: 2d7142343530302d73296b7e5a784c4531395976, Dwn/Up:       0/   16393 B, Ratio: inf. , Pieces Send/recv    0/   1, Connections:  1
  92.248.147.251:20286, NodeId: 2d4b4e333112302d51582e42427e397478787377, Dwn/Up:       0/   16393 B, Ratio: inf. , Pieces Send/recv    0/   1, Connections:  1