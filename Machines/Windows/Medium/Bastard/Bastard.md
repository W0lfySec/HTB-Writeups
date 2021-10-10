
![Image Bastard]()


## ------------------->> Bastard <<---------------------


// We start with nmap scan 


    $ nmap -sV -A -Pn -T4 10.10.10.9 -p-
-------

    Nmap scan report for 10.10.10.9
    Host is up (0.19s latency).
    Not shown: 65532 filtered tcp ports (no-response)
    PORT      STATE SERVICE VERSION
    80/tcp    open  http    Microsoft IIS httpd 7.5
    | http-methods: 
    |_  Potentially risky methods: TRACE
    |_http-generator: Drupal 7 (http://drupal.org)
    |_http-title: Welcome to 10.10.10.9 | 10.10.10.9
    | http-robots.txt: 36 disallowed entries (15 shown)
    | /includes/ /misc/ /modules/ /profiles/ /scripts/ 
    | /themes/ /CHANGELOG.txt /cron.php /INSTALL.mysql.txt 
    | /INSTALL.pgsql.txt /INSTALL.sqlite.txt /install.php /INSTALL.txt 
    |_/LICENSE.txt /MAINTAINERS.txt
    |_http-server-header: Microsoft-IIS/7.5
    135/tcp   open  msrpc   Microsoft Windows RPC
    49154/tcp open  msrpc   Microsoft Windows RPC
    Service Info: OS: Windows; CPE: cpe:/o:microsoft:windows

// Navigating to http://10.10.10.9 shows us ['Drupal'](https://www.drupal.org/)(Open source CMS) login webpage

