
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
       PASS_FILE            rockyou.txt  no        File containing passwords, one per line
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

// And it takes file called 'users.txt' and return '$data' that will be a string(in our case 'Success')

// Next we have function called 'update_db' that first prints string and insert string to value '$data'

// Next we have another function called 'destruct' , this function output file with 'users.txt' and '$data' content

// Next we can see there is a command to server get [arepo](https://en.wikipedia.org/wiki/Sator_Square)

// And finally [unserialize](https://www.php.net/manual/en/function.unserialize.php) with the input command to update data base.

---> [source](https://en.wikipedia.org/wiki/Sator_Square)(from wikipedia) <---

    "" In computing, serialization (US spelling) or serialisation (UK spelling) is the process of translating a data structure
    or object state into a format that can be stored (for example, in a file or memory data buffer) or transmitted
    (for example, over a computer network) and reconstructed later (possibly in a different computer environment) ""

