## --------->> WriteUp <<-----------

// We start with nmap scan

    $ nmap -sV -A -Pn 10.10.10.138 -p-
----

    Nmap scan report for 10.10.10.138
    Host is up (0.17s latency).
    Not shown: 65533 filtered ports
    PORT   STATE SERVICE VERSION
    22/tcp open  ssh     OpenSSH 7.4p1 Debian 10+deb9u6 (protocol 2.0)
    | ssh-hostkey: 
    |   2048 dd:53:10:70:0b:d0:47:0a:e2:7e:4a:b6:42:98:23:c7 (RSA)
    |   256 37:2e:14:68:ae:b9:c2:34:2b:6e:d9:92:bc:bf:bd:28 (ECDSA)
    |_  256 93:ea:a8:40:42:c1:a8:33:85:b3:56:00:62:1c:a0:ab (ED25519)
    80/tcp open  http    Apache httpd 2.4.25 ((Debian))
    | http-robots.txt: 1 disallowed entry 
    |_/writeup/
    |_http-server-header: Apache/2.4.25 (Debian)
    |_http-title: Nothing here yet.
    Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel
    
// navigating to http://10.10.10.138/

![Image 1](https://github.com/W0lfySec/HTB-Writeups/blob/main/Images/WriteUp/1.png)

// When tried to search for any directories in http://10.10.10.138/

// I had Errors, what means this site is protected as written in the site
