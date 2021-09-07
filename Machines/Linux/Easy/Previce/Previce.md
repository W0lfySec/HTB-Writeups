## -------------->> Previce <<----------

// We start with nmap scan

    $ nmap -sV -A -Pn -T4 10.10.11.104
-----

    Nmap scan report for 10.129.214.117
    Host is up (0.32s latency).
    Not shown: 65533 closed ports
    PORT   STATE SERVICE VERSION
    22/tcp open  ssh     OpenSSH 7.6p1 Ubuntu 4ubuntu0.3 (Ubuntu Linux; protocol 2.0)
    | ssh-hostkey: 
    |   2048 53:ed:44:40:11:6e:8b:da:69:85:79:c0:81:f2:3a:12 (RSA)
    |   256 bc:54:20:ac:17:23:bb:50:20:f4:e1:6e:62:0f:01:b5 (ECDSA)
    |_  256 33:c1:89:ea:59:73:b1:78:84:38:a4:21:10:0c:91:d8 (ED25519)
    80/tcp open  http    Apache httpd 2.4.29 ((Ubuntu))
    | http-cookie-flags: 
    |   /: 
    |     PHPSESSID: 
    |_      httponly flag not set
    |_http-server-header: Apache/2.4.29 (Ubuntu)
    | http-title: Previse Login
    |_Requested resource was login.php
    Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel


// Lets search some directories with [dirsearch](https://github.com/maurosoria/dirsearch)(By maurosoria)

$ python3 dirsearch.py -u http://10.10.11.104/ -t 100 

  _|. _ _  _  _  _ _|_    v0.4.1
 (_||| _) (/_(_|| (_| )

Extensions: php, aspx, jsp, html, js | HTTP method: GET | Threads: 100 | Wordlist size: 10903

Output File: /home/kali/Desktop/Tools/dirsearch/reports/10.129.214.117/_21-08-10_20-00-52.txt

Error Log: /home/kali/Desktop/Tools/dirsearch/logs/errors-21-08-10_20-00-52.log

Target: http://10.129.214.117/

[20:00:52] Starting: 
[20:00:59] 301 -  313B  - /js  ->  http://10.129.214.117/js/
[20:01:00] 403 -  279B  - /.ht_wsr.txt
[20:01:00] 403 -  279B  - /.htaccess.bak1
[20:01:00] 403 -  279B  - /.htaccess.orig
[20:01:00] 403 -  279B  - /.htaccess.save
[20:01:00] 403 -  279B  - /.htaccess_orig
[20:01:00] 403 -  279B  - /.htaccessBAK
[20:01:00] 403 -  279B  - /.htaccess_extra
[20:01:00] 403 -  279B  - /.htaccess.sample
[20:01:00] 403 -  279B  - /.htaccess_sc
[20:01:00] 403 -  279B  - /.htaccessOLD2
[20:01:00] 403 -  279B  - /.htaccessOLD
[20:01:00] 403 -  279B  - /.html
[20:01:00] 403 -  279B  - /.htm
[20:01:00] 403 -  279B  - /.htpasswd_test
[20:01:00] 403 -  279B  - /.httr-oauth
[20:01:00] 403 -  279B  - /.htpasswds
[20:01:02] 403 -  279B  - /.php
[20:01:12] 302 -    4KB - /accounts.php  ->  login.php
[20:01:28] 200 -    0B  - /config.php
[20:01:29] 301 -  314B  - /css  ->  http://10.129.214.117/css/
[20:01:31] 302 -    0B  - /download.php  ->  login.php
[20:01:34] 200 -   15KB - /favicon.ico
[20:01:34] 302 -    5KB - /files.php  ->  login.php
[20:01:34] 200 -  217B  - /footer.php
[20:01:35] 200 -  980B  - /header.php
[20:01:37] 302 -    3KB - /index.php  ->  login.php
[20:01:37] 302 -    3KB - /index.php/login/  ->  login.php
[20:01:38] 200 -    1KB - /js/
[20:01:40] 200 -    2KB - /login.php
[20:01:40] 302 -    0B  - /logout.php  ->  login.php
[20:01:51] 403 -  279B  - /server-status
[20:01:51] 403 -  279B  - /server-status/
[20:01:53] 302 -    3KB - /status.php  ->  login.php



$unzip siteBackup.zip 
Archive:  siteBackup.zip
  inflating: accounts.php            
  inflating: config.php              
  inflating: download.php            
  inflating: file_logs.php           
  inflating: files.php               
  inflating: footer.php              
  inflating: header.php              
  inflating: index.php               
  inflating: login.php               
  inflating: logout.php              
  inflating: logs.php                
  inflating: nav.php                 
  inflating: status.php              

$cat config.php 
<?php

function connectDB(){
    $host = 'localhost';
    $user = 'root';
    $passwd = 'mySQL_p@ssw0rd!:)';
    $db = 'previse';
    $mycon = new mysqli($host, $user, $passwd, $db);
    return $mycon;
}

?>

