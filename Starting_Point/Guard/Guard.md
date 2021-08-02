## ------>> Guard <<--------

// We have daniel's ssh private key from last machine (MarkUp).

// We start with nmap scan

    $ nmap -sC -sV -A -Pn 10.10.10.50 -p-
    
    Host discovery disabled (-Pn). All addresses will be marked 'up' and scan times will be slower.
    Starting Nmap 7.91 ( https://nmap.org ) at 2021-07-02 20:22 EDT
    Connect Scan Timing: About 95.09% done; ETC: 20:35 (0:00:37 remaining)
    Nmap scan report for 10.10.10.50
    Host is up (0.44s latency).
    Not shown: 65534 closed ports
    PORT   STATE SERVICE VERSION
    22/tcp open  ssh     OpenSSH 7.6p1 Ubuntu 4ubuntu0.3 (Ubuntu Linux; protocol 2.0)
    | ssh-hostkey: 
    |   2048 2a:64:23:e0:a7:ec:1d:3b:f0:63:72:a7:d7:05:57:71 (RSA)
    |   256 b3:86:5d:3d:c9:d1:70:ea:d6:3d:36:a6:c5:f2:be:5d (ECDSA)
    |_  256 c0:5b:13:0f:d6:e6:d1:71:2d:55:e2:4a:e2:27:0e:c2 (ED25519)
    Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel


// Since we know all the machines in starting point are "Chained-Up", and we have ssh private key for user daniel from last machine 
we can try to connect with him

    $ ssh -i ssh_daniel.key daniel@10.10.10.50

    Welcome to Ubuntu 18.04.3 LTS (GNU/Linux 4.15.0-88-generic x86_64)
    daniel@guard:~$ id
    uid=1000(daniel) gid=1000(picasso) groups=1000(picasso),27(sudo)


// cat not work but less yes

    daniel@guard:~$ less user.txt
    209333....................
    user.txt (END)
    
    
// cat /etc/passwd we can see that daniel do not have regolar shell but have rbash

    daniel@guard:~$ cat /etc/passwd
    ...
    daniel:x:1000:1000:picasso:/home/picasso:/bin/rbash
    ...

// there is a trick to add some confirguration like vim with command more

// and shrink the window to small as possible then you can add ur on syntax

// and execute other shell (our case we want /bin/bash so locate !bash)
![Image 1](https://github.com/W0lfySec/HTB-Writeups/blob/main/Images/Guard/1.png)
![Image 2](https://github.com/W0lfySec/HTB-Writeups/blob/main/Images/Guard/2.png)
![Image 3](https://github.com/W0lfySec/HTB-Writeups/blob/main/Images/Guard/3.png)





Access ID | Name | Email
----------|------|-------
34322 | admin | admin@megacorp.com
