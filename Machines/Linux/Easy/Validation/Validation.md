
![Image Validation]()

## ------------>> Validation <<--------------

// We start with nmap scan 

    $ nmap -sV -A -Pn -T4 10.10.11.116 -p-
---------

    Nmap scan report for 10.10.11.116
    Host is up (0.13s latency).
    Not shown: 65459 closed tcp ports (conn-refused), 72 filtered tcp ports (no-response)
    PORT     STATE SERVICE VERSION
    22/tcp   open  ssh     OpenSSH 8.2p1 Ubuntu 4ubuntu0.3 (Ubuntu Linux; protocol 2.0)
    | ssh-hostkey: 
    |   3072 d8:f5:ef:d2:d3:f9:8d:ad:c6:cf:24:85:94:26:ef:7a (RSA)
    |   256 46:3d:6b:cb:a8:19:eb:6a:d0:68:86:94:86:73:e1:72 (ECDSA)
    |_  256 70:32:d7:e3:77:c1:4a:cf:47:2a:de:e5:08:7a:f8:7a (ED25519)
    80/tcp   open  http    Apache httpd 2.4.48 ((Debian))
    |_http-title: Site doesn't have a title (text/html; charset=UTF-8).
    |_http-server-header: Apache/2.4.48 (Debian)
    4566/tcp open  http    nginx
    |_http-title: 403 Forbidden
    8080/tcp open  http    nginx
    |_http-title: 502 Bad Gateway

// Navigating to http://10.10.11.116/ show us some registration webpage with input for username and country selection

![Image 1]()

// Lets search for interesting directories or files with [dirsearch](https://github.com/maurosoria/dirsearch)(By maurosoria)

    $ python3 dirsearch.py -u http://10.10.11.116/ -t 100
------

      _|. _ _  _  _  _ _|_    v0.4.1
     (_||| _) (/_(_|| (_| )

    Extensions: php, aspx, jsp, html, js | HTTP method: GET | Threads: 100 | Wordlist size: 10903

    Output File: /home/r4r3/Desktop/HTB/main-Tools/web/directories_scanners/dirsearch/reports/10.10.11.116/_21-09-17_00-37-31.txt

    Error Log: /home/r4r3/Desktop/HTB/main-Tools/web/directories_scanners/dirsearch/logs/errors-21-09-17_00-37-31.log

    Target: http://10.10.11.116/

    [00:37:31] Starting: 
    [00:37:40] 403 -  277B  - /.ht_wsr.txt
    [00:37:40] 403 -  277B  - /.htaccess.orig
    [00:37:40] 403 -  277B  - /.htaccess_extra
    [00:37:40] 403 -  277B  - /.htaccess.bak1
    [00:37:40] 403 -  277B  - /.htaccess.sample
    [00:37:40] 403 -  277B  - /.htaccess.save
    [00:37:40] 403 -  277B  - /.htaccess_orig
    [00:37:40] 403 -  277B  - /.htaccess_sc
    [00:37:40] 403 -  277B  - /.htaccessBAK
    [00:37:40] 403 -  277B  - /.htaccessOLD2
    [00:37:40] 403 -  277B  - /.htaccessOLD
    [00:37:40] 403 -  277B  - /.htpasswds
    [00:37:40] 403 -  277B  - /.html
    [00:37:40] 403 -  277B  - /.htm
    [00:37:41] 403 -  277B  - /.httr-oauth
    [00:37:41] 403 -  277B  - /.htpasswd_test
    [00:37:46] 200 -   16B  - /account.php
    [00:37:52] 200 -    0B  - /config.php
    [00:37:52] 301 -  310B  - /css  ->  http://10.10.11.116/css/
    [00:37:54] 200 -   16KB - /index.php
    [00:37:55] 200 -   16KB - /index.php/login/
    [00:37:55] 403 -  277B  - /js/
    [00:38:01] 403 -  277B  - /server-status/
    [00:38:01] 403 -  277B  - /server-status

    Task Completed

// Noting much there(accounts.php its the redirection after register and /config.php is blank page), Moving on ..

// Earlier with nmap we can see there is http service running on ports 8080 and 4566

// Navigating to http://10.10.11.116:8080/ get us ERROR: Bad gateway

// Navigating to http://10.10.11.116:4566/ status 403 (Forbbiden)









