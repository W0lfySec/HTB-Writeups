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
