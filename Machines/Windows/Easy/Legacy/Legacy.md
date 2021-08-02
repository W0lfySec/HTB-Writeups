## ---------->> Legacy <<-----------

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
