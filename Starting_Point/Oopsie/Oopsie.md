## ------>> Oopsie <<-------

// we will start with scanning using nmap

    $ nmap -sV -A -Pn -T4 10.10.10.28 -p-
    Host discovery disabled (-Pn). All addresses will be marked 'up' and scan times will be slower.
    Starting Nmap 7.91 ( https://nmap.org ) at 2021-07-31 09:23 UTC
    Stats: 0:01:52 elapsed; 0 hosts completed (1 up), 1 undergoing Connect Scan
    Connect Scan Timing: About 13.03% done; ETC: 09:38 (0:12:21 remaining)
    Nmap scan report for 10.10.10.28
    Host is up (0.30s latency).
    Not shown: 65533 closed ports
    PORT   STATE SERVICE VERSION
    22/tcp open  ssh     OpenSSH 7.6p1 Ubuntu 4ubuntu0.3 (Ubuntu Linux; protocol 2.0)
    | ssh-hostkey: 
    |   2048 61:e4:3f:d4:1e:e2:b2:f1:0d:3c:ed:36:28:36:67:c7 (RSA)
    |   256 24:1d:a4:17:d4:e3:2a:9c:90:5c:30:58:8f:60:77:8d (ECDSA)
    |_  256 78:03:0e:b4:a1:af:e5:c2:f9:8d:29:05:3e:29:c9:f2 (ED25519)
    80/tcp open  http    Apache httpd 2.4.29 ((Ubuntu))
    |_http-server-header: Apache/2.4.29 (Ubuntu)
    |_http-title: Welcome
    Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

    Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
    Nmap done: 1 IP address (1 host up) scanned in 795.95 seconds

![Test Image 1](/Screenshot_2021-07-31_09_50_13.png)
