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



// Lets search for interesting directories in the website, for that we will use tool called ![dirsearch.py](https://github.com/maurosoria/dirsearch)
