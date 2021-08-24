## ----------------->> Proper <<----------------

// We start with nmap scan

    $nmap -sV -A -Pn -T4 10.10.10.231 -p-
----------

    Nmap scan report for 10.10.10.231
    Host is up (0.23s latency).
    Not shown: 65534 filtered ports
    PORT   STATE SERVICE VERSION
    80/tcp open  http    Microsoft IIS httpd 10.0
    | http-methods: 
    |_  Potentially risky methods: TRACE
    |_http-server-header: Microsoft-IIS/10.0
    |_http-title: OS Tidy Inc.
    Service Info: OS: Windows; CPE: cpe:/o:microsoft:windows

// We can see only port 80(http) open, Lets check it out

![Image 1]()

// Its seems like some company products website,

// Move on to search for interesting directories or files with [dirsearch](https://github.com/maurosoria/dirsearch)(By maurosoria)

    $ python3 dirsearch.py -u http://10.10.10.231/ -t 100 -w /usr/share/dirb/wordlists/big.txt 
--------

      _|. _ _  _  _  _ _|_    v0.4.1
     (_||| _) (/_(_|| (_| )

    Extensions: php, aspx, jsp, html, js | HTTP method: GET | Threads: 100 | Wordlist size: 20469

    Output File: /home/r4r3/Desktop/HTB/main-Tools/web/directories_scanners/dirsearch/reports/10.10.10.231/_21-08-24_09-17-58.txt

    Error Log: /home/r4r3/Desktop/HTB/main-Tools/web/directories_scanners/dirsearch/logs/errors-21-08-24_09-17-58.log

    Target: http://10.10.10.231/

    [09:17:58] Starting: 
    [09:18:07] 301 -  150B  - /assets  ->  http://10.10.10.231/assets/
    [09:18:26] 301 -  152B  - /licenses  ->  http://10.10.10.231/licenses/

    Task Completed

// We found two directories /assets/ its Forbbiden but /licenses/ get us to login page

![Image 4]()

// guessing and sql injection syntaxes didnt work...

// Moving on to BurpSuite and open the first page (http://10.10.10.231/index.html) With Reapeter

// The response shows us that there another directory that load with the /index.html

![Image 2]()

    /products-ajax.php?order=id+desc&h=a1b30d31d344a5a4e41e8496ccbdd26b
    
// Navigating to there, shows us all the company products

![Image 3]()

// Also 'order=id+desc' looks like SQL query i will change desc to asc(read more abot [desc&asc](https://www.guru99.com/order-by-desc-and-asc.html))

![Image 5]()

// We got Forbidden page, Moving on...

// When removing the md5 hash from the browser we got error for parameter missing

![Image 6]()

// Lets try to remove 'h' parameter

// Now we get the same error but this time we get also with crash details

![Image 7]()

// We got the secure-salt !

    'SECURE_PARAM_SALT','hie0shah6ooNoim'

// 

