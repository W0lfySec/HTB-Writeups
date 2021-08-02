## ------>> Blue <<-------

// We will start with nmap scan

    $ nmap -sV -A -Pn 10.10.10.40 -p-
-----

    Nmap scan report for 10.10.10.40
    Host is up (0.46s latency).
    Not shown: 65526 closed ports
    PORT      STATE SERVICE      VERSION
    135/tcp   open  msrpc        Microsoft Windows RPC
    139/tcp   open  netbios-ssn  Microsoft Windows netbios-ssn
    445/tcp   open  microsoft-ds Windows 7 Professional 7601 Service Pack 1 microsoft-ds (workgroup: WORKGROUP)
    49152/tcp open  msrpc        Microsoft Windows RPC
    49153/tcp open  msrpc        Microsoft Windows RPC
    49154/tcp open  msrpc        Microsoft Windows RPC
    49155/tcp open  msrpc        Microsoft Windows RPC
    49156/tcp open  msrpc        Microsoft Windows RPC
    49157/tcp open  msrpc        Microsoft Windows RPC
    Service Info: Host: HARIS-PC; OS: Windows; CPE: cpe:/o:microsoft:windows

    Host script results:
    |_clock-skew: mean: -8m45s, deviation: 34m37s, median: 11m12s
    | smb-os-discovery: 
    |   OS: Windows 7 Professional 7601 Service Pack 1 (Windows 7 Professional 6.1)
    |   OS CPE: cpe:/o:microsoft:windows_7::sp1:professional
    |   Computer name: haris-PC
    |   NetBIOS computer name: HARIS-PC\x00
    |   Workgroup: WORKGROUP\x00
    |_  System time: 2021-06-17T04:37:57+01:00
    | smb-security-mode: 
    |   account_used: guest
    |   authentication_level: user
    |   challenge_response: supported
    |_  message_signing: disabled (dangerous, but default)
    | smb2-security-mode: 
    |   2.02: 
    |_    Message signing enabled but not required
    | smb2-time: 
    |   date: 2021-06-17T03:38:00
    |_  start_date: 2021-06-17T03:22:12


// From the scan we can see the host OS[Operation System] is Windows 7 and there is SMBv2 service open

// The combinaniton of Win7 os and smb v2 its the requirments for the famous Eternal-Blue Exploit

// Lets open MetaSploit

    $ msfconsole

// 
