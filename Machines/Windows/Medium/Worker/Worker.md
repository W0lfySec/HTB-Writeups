
![Image Worker]()


## ------------>> Worker <<------------


// We start with nmap scan

    $ nmap -sV -A -Pn -T4 10.10.10.203 -p-
------

    Nmap scan report for 10.10.10.203
    Host is up (0.19s latency).
    Not shown: 65532 filtered tcp ports (no-response)
    PORT     STATE SERVICE  VERSION
    80/tcp   open  http     Microsoft IIS httpd 10.0
    |_http-title: IIS Windows Server
    | http-methods: 
    |_  Potentially risky methods: TRACE
    |_http-server-header: Microsoft-IIS/10.0
    3690/tcp open  svnserve Subversion
    5985/tcp open  http     Microsoft HTTPAPI httpd 2.0 (SSDP/UPnP)
    |_http-title: Not Found
    |_http-server-header: Microsoft-HTTPAPI/2.0
    Service Info: OS: Windows; CPE: cpe:/o:microsoft:windows

// Navigating to http://10.10.10.203/

![Image 1]()

// Search for any directories or files didnt get much.. for now.

    $python3 dirsearch.py -u http://10.10.10.203/ -t 100
-----

      _|. _ _  _  _  _ _|_    v0.4.1
     (_||| _) (/_(_|| (_| )

    Extensions: php, aspx, jsp, html, js | HTTP method: GET | Threads: 100 | Wordlist size: 10903

    Output File: /home/r4r3/Desktop/HTB/main-Tools/web/directories_scanners/dirsearch/reports/10.10.10.203/_21-09-10_21-19-26.txt

    Error Log: /home/r4r3/Desktop/HTB/main-Tools/web/directories_scanners/dirsearch/logs/errors-21-09-10_21-19-26.log

    Target: http://10.10.10.203/

    [21:19:27] Starting: 
    [21:19:33] 403 -  312B  - /%2e%2e//google.com
    [21:19:40] 403 -    2KB - /Trace.axd
    [21:19:41] 403 -  312B  - /\..\..\..\..\..\..\..\..\..\etc\passwd
    [21:19:46] 403 -    1KB - /aspnet_client/
    [21:19:46] 301 -  157B  - /aspnet_client  ->  http://10.10.10.203/aspnet_client/
    [21:19:56] 400 -    3KB - /jolokia/read/java.lang:type=*/HeapMemoryUsage
    [21:19:56] 400 -    3KB - /jolokia/exec/java.lang:type=Memory/gc
    [21:19:56] 400 -    3KB - /jolokia/exec/com.sun.management:type=DiagnosticCommand/help/*
    [21:19:56] 400 -    3KB - /jolokia/search/*:j2eeType=J2EEServer,*
    [21:19:56] 400 -    3KB - /jolokia/read/java.lang:type=Memory/HeapMemoryUsage/used
    [21:19:56] 400 -    3KB - /jolokia/exec/com.sun.management:type=DiagnosticCommand/vmSystemProperties
    [21:19:56] 400 -    3KB - /jolokia/exec/com.sun.management:type=DiagnosticCommand/jfrStart/filename=!/tmp!/foo
    [21:19:56] 400 -    3KB - /jolokia/exec/com.sun.management:type=DiagnosticCommand/vmLog/disable
    [21:19:56] 400 -    3KB - /jolokia/write/java.lang:type=Memory/Verbose/true
    [21:19:56] 400 -    3KB - /jolokia/exec/com.sun.management:type=DiagnosticCommand/compilerDirectivesAdd/!/etc!/passwd
    [21:19:56] 400 -    3KB - /jolokia/exec/com.sun.management:type=DiagnosticCommand/jvmtiAgentLoad/!/etc!/passwd
    [21:19:56] 400 -    3KB - /jolokia/exec/com.sun.management:type=DiagnosticCommand/vmLog/output=!/tmp!/pwned


### SVN service

The [article](https://svnbook.red-bean.com/en/1.7/svn.serverconfig.svnserve.html)

" The svnserve program is a lightweight server, capable of speaking to clients over TCP/IP using a custom,

stateful protocol. Clients contact an svnserve server by using URLs that begin with the svn:// or svn+ssh:// scheme.

This section will explain the different ways of running svnserve, how clients authenticate themselves to the server,

and how to configure appropriate access control to your repositories."

// Lets check the files

    $ svn checkout svn://10.10.10.203
-----

    A    dimension.worker.htb
    A    dimension.worker.htb/LICENSE.txt
    A    dimension.worker.htb/README.txt
    ...[SNIP]...
    A    moved.txt

// We've got interesting file called 'moved.txt', lets see his content

    $ cat moved.txt 

    This repository has been migrated and will no longer be maintaned here.
    You can find the latest version at: http://devops.worker.htb

    // The Worker team :)

// Now we add the domain to /etc/hosts.

    $ cat /etc/hosts

    # Host addresses
    10.10.10.203 devops.worker.htb

// 


