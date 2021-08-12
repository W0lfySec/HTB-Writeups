## -------------->> Blocky <<--------------

// We start with nmap scan

    $ nmap -sV -A -Pn -T4 10.10.10.37 -p-
-----------

    Nmap scan report for 10.10.10.37
    Host is up (0.14s latency).
    Not shown: 65530 filtered ports
    PORT      STATE  SERVICE   VERSION
    21/tcp    open   ftp       ProFTPD 1.3.5a
    22/tcp    open   ssh       OpenSSH 7.2p2 Ubuntu 4ubuntu2.2 (Ubuntu Linux; protocol 2.0)
    | ssh-hostkey: 
    |   2048 d6:2b:99:b4:d5:e7:53:ce:2b:fc:b5:d7:9d:79:fb:a2 (RSA)
    |   256 5d:7f:38:95:70:c9:be:ac:67:a0:1e:86:e7:97:84:03 (ECDSA)
    |_  256 09:d5:c2:04:95:1a:90:ef:87:56:25:97:df:83:70:67 (ED25519)
    80/tcp    open   http      Apache httpd 2.4.18 ((Ubuntu))
    |_http-generator: WordPress 4.8
    |_http-server-header: Apache/2.4.18 (Ubuntu)
    |_http-title: BlockyCraft &#8211; Under Construction!
    8192/tcp  closed sophos
    25565/tcp open   minecraft Minecraft 1.11.2 (Protocol: 127, Message: A Minecraft Server, Users: 0/20)
    Service Info: OSs: Unix, Linux; CPE: cpe:/o:linux:linux_kernel

    Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
    Nmap done: 1 IP address (1 host up) scanned in 184.05 seconds

// Navigating to http://10.10.10.37/ , display us a game website in development

// Rolling down the site there is a 'Login' button

![Image 1]()

// Clicking on the login redirect us to http://10.10.10.37/wp-login.php

![Image 2]()

// Since we know now we dilling with Wordpress CMS we can use [wpscan](https://wpscan.com/wordpress-security-scanner) to scan for vulnerabillities

    $ wpscan --url http://10.10.10.37/ --api-token YOUR_API_KEY --plugins-detection mixed -e
-----

    _______________________________________________________________
             __          _______   _____
             \ \        / /  __ \ / ____|
              \ \  /\  / /| |__) | (___   ___  __ _ _ __ ®
               \ \/  \/ / |  ___/ \___ \ / __|/ _` | '_ \
                \  /\  /  | |     ____) | (__| (_| | | | |
                 \/  \/   |_|    |_____/ \___|\__,_|_| |_|

             WordPress Security Scanner by the WPScan Team
                             Version 3.8.18
           Sponsored by Automattic - https://automattic.com/
           @_WPScan_, @ethicalhack3r, @erwan_lr, @firefart
    _______________________________________________________________

    [+] URL: http://10.10.10.37/ [10.10.10.37]
    [+] Started: Thu Aug 12 06:04:31 2021
    
    ...

    [+] WordPress version 4.8 identified (Insecure, released on 2017-06-08).
     | Found By: Rss Generator (Passive Detection)
     |  - http://10.10.10.37/index.php/feed/, <generator>https://wordpress.org/?v=4.8</generator>
     |  - http://10.10.10.37/index.php/comments/feed/, <generator>https://wordpress.org/?v=4.8</generator>
     |
     | [!] 51 vulnerabilities identified:

// 






