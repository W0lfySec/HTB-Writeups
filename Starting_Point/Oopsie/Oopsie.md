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
    
// quick directory search with FeroxBuster reveals me 'upload' directory, we will save that for later

    $ ./feroxbuster -u http://10.10.10.28/ -t 200

     ___  ___  __   __     __      __         __   ___
    |__  |__  |__) |__) | /  `    /  \ \_/ | |  \ |__
    |    |___ |  \ |  \ | \__,    \__/ / \ | |__/ |___
    by Ben "epi" Risher 🤓                 ver: 2.3.1
    ───────────────────────────┬──────────────────────
     🎯  Target Url            │ http://10.10.10.28/
     🚀  Threads               │ 200
     📖  Wordlist              │ /usr/share/seclists/Discovery/Web-Content/raft-medium-directories.txt
     👌  Status Codes          │ [200, 204, 301, 302, 307, 308, 401, 403, 405]
     💥  Timeout (secs)        │ 7
     🦡  User-Agent            │ feroxbuster/2.3.1
     🔃  Recursion Depth       │ 4
    ───────────────────────────┴──────────────────────
     🏁  Press [ENTER] to use the Scan Cancel Menu™
    ──────────────────────────────────────────────────
    301        9l       28w      311c http://10.10.10.28/images
    301        9l       28w      307c http://10.10.10.28/js
    301        9l       28w      308c http://10.10.10.28/css
    301        9l       28w      311c http://10.10.10.28/themes
    301        9l       28w      312c http://10.10.10.28/uploads

// since its a web server we can use 'curl' command to gain more information

    $ curl http://10.10.10.28/
    <!DOCTYPE html>
    <html lang="en">
    <head>
    <meta charset="UTF-8">
    ...
    <div class="col-6">
    <p><i class="fa fa-phone" aria-hidden="true"></i> +44 (0)123 456 789</p>
    <p><i class="fa fa-envelope" aria-hidden="true"></i> admin@megacorp.com</p>
    </div>
    ...
    
// we found the admin mail - admin@megacorp.com

// Navigating to to http://10.10.10.28/ present me with some automobile site, searching in the page source reveals me some login directory

![Image 1](https://github.com/W0lfySec/HTB/blob/main/Images/Oopsie/Screenshot_2021-07-31_09_50_13.png)

// Since we have Administrative credentials that assosiate wit MegaCorp from last challenge(ArcheType) 

    # cat ConsoleHost_history.txt 
    net.exe use T: \\Archetype\backups /user:administrator MEGACORP_4dm1n!!
    
// Lets try input them in the login page
// And it Works !!!

![Image 2](https://github.com/W0lfySec/HTB/blob/main/Images/Oopsie/Screenshot_2021-07-31_10_45_27.png)

// in the account directory(http://10.10.10.28/cdn-cgi/login/admin.php?content=accounts&id=1) we see
Access ID | Name | Email
----------|------|-------
34322 | admin | admin@megacorp.com

// When navigating to uploads (http://10.10.10.28/cdn-cgi/login/admin.php?content=uploads) we get error due privilleges

![Image 2](https://github.com/W0lfySec/HTB/blob/main/Images/Oopsie/Screenshot_2021-07-31_11_02_28.png)

// it seems we need super admin privilleges to upload files.  we know from account page that our id is 1 (http://10.10.10.28/cdn-cgi/login/admin.php?content=accounts&id=1) and Access ID is 34322 , since we know we need super admin id we can Brute Force the id section using BurpSuite intruder
 just get to account page and refresh using BurpSuite and then right click >> send to Intruder
 
 ![Image 2](https://github.com/W0lfySec/HTB/blob/main/Images/Oopsie/Screenshot_2021-07-31_11_32_47.png)
