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

// we will scan UDP also

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



Access ID | Name | Email
----------|------|-------
34322 | admin | admin@megacorp.com

// When navigating to uploads (http://10.10.10.28/cdn-cgi/login/admin.php?content=uploads) we get error due privilleges


