## --------------->> Beep <<-----------------

// We start with nmap scan

    $ nmap -sV -A -Pn -T4 10.10.10.7 -p-
------

    Nmap scan report for 10.10.10.7
    Host is up (0.38s latency).
    Not shown: 65519 closed ports
    PORT      STATE SERVICE    VERSION
    22/tcp    open  ssh        OpenSSH 4.3 (protocol 2.0)
    | ssh-hostkey: 
    |   1024 ad:ee:5a:bb:69:37:fb:27:af:b8:30:72:a0:f9:6f:53 (DSA)
    |_  2048 bc:c6:73:59:13:a1:8a:4b:55:07:50:f6:65:1d:6d:0d (RSA)
    25/tcp    open  smtp       Postfix smtpd
    |_smtp-commands: beep.localdomain, PIPELINING, SIZE 10240000, VRFY, ETRN, ENHANCEDSTATUSCODES, 8BITMIME, DSN, 
    80/tcp    open  http       Apache httpd 2.2.3
    |_http-server-header: Apache/2.2.3 (CentOS)
    |_http-title: Did not follow redirect to https://10.10.10.7/
    110/tcp   open  pop3       Cyrus pop3d 2.3.7-Invoca-RPM-2.3.7-7.el5_6.4
    |_pop3-capabilities: EXPIRE(NEVER) TOP APOP AUTH-RESP-CODE UIDL IMPLEMENTATION(Cyrus POP3 server v2) USER RESP-CODES LOGIN-DELAY(0) PIPELINING STLS
    111/tcp   open  rpcbind    2 (RPC #100000)
    | rpcinfo: 
    |   program version    port/proto  service
    |   100000  2            111/tcp   rpcbind
    |   100000  2            111/udp   rpcbind
    |   100024  1            875/udp   status
    |_  100024  1            878/tcp   status
    143/tcp   open  imap       Cyrus imapd 2.3.7-Invoca-RPM-2.3.7-7.el5_6.4
    |_imap-capabilities: Completed LISTEXT OK SORT CHILDREN MAILBOX-REFERRALS ACL ID NO URLAUTHA0001 X-NETSCAPE IDLE ATOMIC LIST-SUBSCRIBED RIGHTS=kxte IMAP4rev1 CATENATE QUOTA CONDSTORE UIDPLUS ANNOTATEMORE MULTIAPPEND THREAD=ORDEREDSUBJECT LITERAL+ NAMESPACE SORT=MODSEQ THREAD=REFERENCES BINARY STARTTLS UNSELECT IMAP4 RENAME
    443/tcp   open  ssl/https?
    | ssl-cert: Subject: commonName=localhost.localdomain/organizationName=SomeOrganization/stateOrProvinceName=SomeState/countryName=--
    | Not valid before: 2017-04-07T08:22:08
    |_Not valid after:  2018-04-07T08:22:08
    |_ssl-date: 2021-08-14T15:03:44+00:00; -1s from scanner time.
    878/tcp   open  status     1 (RPC #100024)
    993/tcp   open  ssl/imap   Cyrus imapd
    |_imap-capabilities: CAPABILITY
    995/tcp   open  pop3       Cyrus pop3d
    3306/tcp  open  mysql      MySQL (unauthorized)
    |_ssl-cert: ERROR: Script execution failed (use -d to debug)
    |_ssl-date: ERROR: Script execution failed (use -d to debug)
    |_sslv2: ERROR: Script execution failed (use -d to debug)
    |_tls-alpn: ERROR: Script execution failed (use -d to debug)
    |_tls-nextprotoneg: ERROR: Script execution failed (use -d to debug)
    4190/tcp  open  sieve      Cyrus timsieved 2.3.7-Invoca-RPM-2.3.7-7.el5_6.4 (included w/cyrus imap)
    4445/tcp  open  upnotifyp?
    4559/tcp  open  hylafax    HylaFAX 4.3.10
    5038/tcp  open  asterisk   Asterisk Call Manager 1.1
    10000/tcp open  http       MiniServ 1.570 (Webmin httpd)
    |_http-server-header: MiniServ/1.570
    |_http-title: Site doesn't have a title (text/html; Charset=iso-8859-1).
    Service Info: Hosts:  beep.localdomain, 127.0.0.1, example.com, localhost; OS: Unix

    Host script results:
    |_clock-skew: -1s

    Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
    Nmap done: 1 IP address (1 host up) scanned in 1631.55 seconds

// Navigating to http://10.10.10.7/ redirect us to HTTPS(port 443) https://10.10.10.7/ , its a login page of elastix(private branch exchange software)

![Image 1]()

// 

