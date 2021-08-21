## ---------------->> Active <<----------------

// We start with nmap scan

    $ nmap -sV -A -Pn -T4 10.10.10.100 -p-
------

    Host is up (0.32s latency).
    Not shown: 65512 closed ports
    PORT      STATE SERVICE       VERSION
    53/tcp    open  domain        Microsoft DNS 6.1.7601 (1DB15D39) (Windows Server 2008 R2 SP1)
    | dns-nsid: 
    |_  bind.version: Microsoft DNS 6.1.7601 (1DB15D39)
    88/tcp    open  kerberos-sec  Microsoft Windows Kerberos (server time: 2021-08-21 01:38:02Z)
    135/tcp   open  msrpc         Microsoft Windows RPC
    139/tcp   open  netbios-ssn   Microsoft Windows netbios-ssn
    389/tcp   open  ldap          Microsoft Windows Active Directory LDAP (Domain: active.htb, Site: Default-First-Site-Name)
    445/tcp   open  microsoft-ds?
    464/tcp   open  kpasswd5?
    593/tcp   open  ncacn_http    Microsoft Windows RPC over HTTP 1.0
    636/tcp   open  tcpwrapped
    3268/tcp  open  ldap          Microsoft Windows Active Directory LDAP (Domain: active.htb, Site: Default-First-Site-Name)
    3269/tcp  open  tcpwrapped
    5722/tcp  open  msrpc         Microsoft Windows RPC
    9389/tcp  open  mc-nmf        .NET Message Framing
    47001/tcp open  http          Microsoft HTTPAPI httpd 2.0 (SSDP/UPnP)
    |_http-server-header: Microsoft-HTTPAPI/2.0
    |_http-title: Not Found
    49152/tcp open  msrpc         Microsoft Windows RPC
    49153/tcp open  msrpc         Microsoft Windows RPC
    49154/tcp open  msrpc         Microsoft Windows RPC
    49155/tcp open  msrpc         Microsoft Windows RPC
    49157/tcp open  ncacn_http    Microsoft Windows RPC over HTTP 1.0
    49158/tcp open  msrpc         Microsoft Windows RPC
    49169/tcp open  msrpc         Microsoft Windows RPC
    49171/tcp open  msrpc         Microsoft Windows RPC
    49182/tcp open  msrpc         Microsoft Windows RPC
    Service Info: Host: DC; OS: Windows; CPE: cpe:/o:microsoft:windows_server_2008:r2:sp1, cpe:/o:microsoft:windows

    Host script results:
    | smb2-security-mode: 
    |   2.02: 
    |_    Message signing enabled and required
    | smb2-time: 
    |   date: 2021-08-21T01:39:00
    |_  start_date: 2021-08-21T01:21:20

// We can see that smb service is active

// Lets see if we can see shared directories with [smbmap](https://github.com/ShawnDEvans/smbmap)

    $ smbmap -H 10.10.10.100
------

    [+] IP: 10.10.10.100:445	Name: 10.10.10.100                                      
            Disk                                                  	Permissions	Comment
      ----                                                  	-----------	-------
      ADMIN$                                            	NO ACCESS	Remote Admin
      C$                                                	NO ACCESS	Default share
      IPC$                                              	NO ACCESS	Remote IPC
      NETLOGON                                          	NO ACCESS	Logon server share 
      Replication                                       	READ ONLY	
      SYSVOL                                            	NO ACCESS	Logon server share 
      Users                                             	NO ACCESS	

// There is one directory that we have read permissions - Replication 

// Lets search recursivly this directory

    $ smbmap -H 10.10.10.100 -R Replication

// After some search the most interesting file is in Groups folder and called 'Groups.xml'

    $ smbmap -H 10.10.10.100 -R Replication/active.htb/Policies/{31B2F340-016D-11D2-945F-00C04FB984F9}/MACHINE/Preferences/
-------

    [+] IP: 10.10.10.100:445	Name: 10.10.10.100                                      
            Disk                                                  	Permissions	Comment
      ----                                                  	-----------	-------
      Replication                                       	READ ONLY	
      .\Replicationactive.htb\Policies\{31B2F340-016D-11D2-945F-00C04FB984F9}\MACHINE\Preferences\*
      dr--r--r--                0 Sat Jul 21 06:37:44 2018	.
      dr--r--r--                0 Sat Jul 21 06:37:44 2018	..
      dr--r--r--                0 Sat Jul 21 06:37:44 2018	Groups
      .\Replicationactive.htb\Policies\{31B2F340-016D-11D2-945F-00C04FB984F9}\MACHINE\Preferences\Groups\*
      dr--r--r--                0 Sat Jul 21 06:37:44 2018	.
      dr--r--r--                0 Sat Jul 21 06:37:44 2018	..
      fr--r--r--              533 Sat Jul 21 06:38:11 2018	Groups.xml

// 

Replication/active.htb/Policies/{31B2F340-016D-11D2-945F-00C04FB984F9}/MACHINE/Preferences/Groups/Groups.xml
