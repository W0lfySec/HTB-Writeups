## ------------>> Base <<----------------

// We start with nmap scan

    $ nmap -sC -sV -A -Pn 10.10.10.48 -p-
-----    
    
    Host discovery disabled (-Pn). All addresses will be marked 'up' and scan times will be slower.
    Starting Nmap 7.91 ( https://nmap.org ) at 2021-07-02 21:35 EDT
    Stats: 0:01:30 elapsed; 0 hosts completed (1 up), 1 undergoing Connect Scan
    Connect Scan Timing: About 7.28% done; ETC: 21:55 (0:18:53 remaining)
    Nmap scan report for 10.10.10.48
    Host is up (0.37s latency).
    Not shown: 65533 closed ports
    PORT   STATE SERVICE VERSION
    22/tcp open  ssh     OpenSSH 7.6p1 Ubuntu 4ubuntu0.3 (Ubuntu Linux; protocol 2.0)
    | ssh-hostkey: 
    |   2048 f6:5c:9b:38:ec:a7:5c:79:1c:1f:18:1c:52:46:f7:0b (RSA)
    |   256 65:0c:f7:db:42:03:46:07:f2:12:89:fe:11:20:2c:53 (ECDSA)
    |_  256 b8:65:cd:3f:34:d8:02:6a:e3:18:23:3e:77:dd:87:40 (ED25519)
    80/tcp open  http    Apache httpd 2.4.29 ((Ubuntu))
    |_http-server-header: Apache/2.4.29 (Ubuntu)
    |_http-title: Site doesn't have a title (text/html).
    Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

![Image 1](https://github.com/W0lfySec/HTB-Writeups/blob/main/Images/Base/1.png)



![Image 2](https://github.com/W0lfySec/HTB-Writeups/blob/main/Images/Base/2.png)







Access ID | Name | Email
----------|------|-------
34322 | admin | admin@megacorp.com

