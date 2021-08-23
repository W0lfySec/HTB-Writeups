## ---------------->> Irked <<-----------------

// We start with nmap scan

    $ nmap -sV -A -Pn -T4 10.10.10.117 -p-
-------

    Nmap scan report for 10.10.10.117
    Host is up (0.39s latency).
    Not shown: 65444 closed ports, 84 filtered ports
    PORT      STATE SERVICE VERSION
    22/tcp    open  ssh     OpenSSH 6.7p1 Debian 5+deb8u4 (protocol 2.0)
    | ssh-hostkey: 
    |   1024 6a:5d:f5:bd:cf:83:78:b6:75:31:9b:dc:79:c5:fd:ad (DSA)
    |   2048 75:2e:66:bf:b9:3c:cc:f7:7e:84:8a:8b:f0:81:02:33 (RSA)
    |   256 c8:a3:a2:5e:34:9a:c4:9b:90:53:f7:50:bf:ea:25:3b (ECDSA)
    |_  256 8d:1b:43:c7:d0:1a:4c:05:cf:82:ed:c1:01:63:a2:0c (ED25519)
    80/tcp    open  http    Apache httpd 2.4.10 ((Debian))
    |_http-server-header: Apache/2.4.10 (Debian)
    |_http-title: Site doesn't have a title (text/html).
    111/tcp   open  rpcbind 2-4 (RPC #100000)
    | rpcinfo: 
    |   program version    port/proto  service
    |   100000  2,3,4        111/tcp   rpcbind
    |   100000  2,3,4        111/udp   rpcbind
    |   100000  3,4          111/tcp6  rpcbind
    |   100000  3,4          111/udp6  rpcbind
    |   100024  1          43569/tcp6  status
    |   100024  1          47827/tcp   status
    |   100024  1          54210/udp6  status
    |_  100024  1          57310/udp   status
    6697/tcp  open  irc     UnrealIRCd
    8067/tcp  open  irc     UnrealIRCd
    47827/tcp open  status  1 (RPC #100024)
    65534/tcp open  irc     UnrealIRCd
    Service Info: Host: irked.htb; OS: Linux; CPE: cpe:/o:linux:linux_kernel

// Navigating to http://10.10.10.117/ , represent us with a picture

![Image 1]()

// Lets search for some directories or files with [dirsearch](https://github.com/maurosoria/dirsearch) Tool (By maurosoria)

    $ python3 dirsearch.py -u http://10.10.10.117/ -i 100-400 -t 100
--------

      _|. _ _  _  _  _ _|_    v0.4.1
     (_||| _) (/_(_|| (_| )

    Extensions: php, aspx, jsp, html, js | HTTP method: GET | Threads: 100 | Wordlist size: 10903

    Output File: /home/r4r3/Desktop/HTB/main-Tools/web/directories_scanners/dirsearch/reports/10.10.10.117/_21-08-22_21-09-54.txt

    Error Log: /home/r4r3/Desktop/HTB/main-Tools/web/directories_scanners/dirsearch/logs/errors-21-08-22_21-09-54.log

    Target: http://10.10.10.117/

    [21:09:56] Starting: 
    [21:10:15] 200 -   72B  - /index.html
    [21:10:17] 200 -  626B  - /manual/index.html
    [21:10:17] 301 -  313B  - /manual  ->  http://10.10.10.117/manual/

// Navigating to http://10.10.10.117/manual/ , represent us with apache 2.4 manual

![Image 2]()

// Nothing much there, lets move on.

// We notice also we have service called UnrealIRCd on ports 6697,8067,65534

    6697/tcp  open  irc     UnrealIRCd
    8067/tcp  open  irc     UnrealIRCd
    65534/tcp open  irc     UnrealIRCd

// Lets search for exploit for that service with 'searchsploit'

    $ searchsploit UnrealIRCd
------------

    UnrealIRCd 3.2.8.1 - Backdoor Command Execution (Metasploit)                                                | linux/remote/16922.rb
    UnrealIRCd 3.2.8.1 - Local Configuration Stack Overflow                                                     | windows/dos/18011.txt
    UnrealIRCd 3.2.8.1 - Remote Downloader/Execute                                                              | linux/remote/13853.pl
    UnrealIRCd 3.x - Remote Denial of Service                                                                   | windows/dos/27407.pl

// We can see there is a Metasploit module for exploit this service, lets try this 

https://www.exploit-db.com/exploits/13853
