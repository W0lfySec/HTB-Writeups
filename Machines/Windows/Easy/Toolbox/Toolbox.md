

## ----------->> Toolbox <<-------------


// We start with nmap scan 

    $ nmap -sV -A -Pn -T4 10.10.10.236 -p-
--------

    Nmap scan report for 10.10.10.236
    Host is up (0.21s latency).
    Not shown: 65521 closed tcp ports (conn-refused)
    PORT      STATE SERVICE       VERSION
    21/tcp    open  ftp           FileZilla ftpd
    | ftp-anon: Anonymous FTP login allowed (FTP code 230)
    |_-r-xr-xr-x 1 ftp ftp      242520560 Feb 18  2020 docker-toolbox.exe
    | ftp-syst: 
    |_  SYST: UNIX emulated by FileZilla
    22/tcp    open  ssh           OpenSSH for_Windows_7.7 (protocol 2.0)
    | ssh-hostkey: 
    |   2048 5b:1a:a1:81:99:ea:f7:96:02:19:2e:6e:97:04:5a:3f (RSA)
    |   256 a2:4b:5a:c7:0f:f3:99:a1:3a:ca:7d:54:28:76:b2:dd (ECDSA)
    |_  256 ea:08:96:60:23:e2:f4:4f:8d:05:b3:18:41:35:23:39 (ED25519)
    135/tcp   open  msrpc         Microsoft Windows RPC
    139/tcp   open  netbios-ssn   Microsoft Windows netbios-ssn
    443/tcp   open  ssl/http      Apache httpd 2.4.38 ((Debian))
    |_http-server-header: Apache/2.4.38 (Debian)
    |_ssl-date: TLS randomness does not represent time
    | ssl-cert: Subject: commonName=admin.megalogistic.com/organizationName=MegaLogistic Ltd/stateOrProvinceName=Some-State/countryName=GR
    | Not valid before: 2020-02-18T17:45:56
    |_Not valid after:  2021-02-17T17:45:56
    | tls-alpn: 
    |_  http/1.1
    |_http-title: MegaLogistics
    445/tcp   open  microsoft-ds?
    5985/tcp  open  http          Microsoft HTTPAPI httpd 2.0 (SSDP/UPnP)
    |_http-server-header: Microsoft-HTTPAPI/2.0
    |_http-title: Not Found
    47001/tcp open  http          Microsoft HTTPAPI httpd 2.0 (SSDP/UPnP)
    |_http-server-header: Microsoft-HTTPAPI/2.0
    |_http-title: Not Found
    49664/tcp open  msrpc         Microsoft Windows RPC
    49665/tcp open  msrpc         Microsoft Windows RPC
    49666/tcp open  msrpc         Microsoft Windows RPC
    49667/tcp open  msrpc         Microsoft Windows RPC
    49668/tcp open  msrpc         Microsoft Windows RPC
    49669/tcp open  msrpc         Microsoft Windows RPC
    Service Info: OS: Windows; CPE: cpe:/o:microsoft:windows

    Host script results:
    | smb2-security-mode: 
    |   3.1.1: 
    |_    Message signing enabled but not required
    | smb2-time: 
    |   date: 2021-09-12T14:26:38
    |_  start_date: N/A

// 
