
![Image ScriptKiddie]()


## --------------->> ScriptKiddie <<----------------


// We start with nmap scan 

    $nmap -sV -A -Pn -T4 10.10.10.226 -p-
------

    Nmap scan report for 10.10.10.226
    Host is up (0.62s latency).
    Not shown: 65483 closed tcp ports (conn-refused), 50 filtered tcp ports (no-response)
    PORT     STATE SERVICE VERSION
    22/tcp   open  ssh     OpenSSH 8.2p1 Ubuntu 4ubuntu0.1 (Ubuntu Linux; protocol 2.0)
    | ssh-hostkey: 
    |   3072 3c:65:6b:c2:df:b9:9d:62:74:27:a7:b8:a9:d3:25:2c (RSA)
    |   256 b9:a1:78:5d:3c:1b:25:e0:3c:ef:67:8d:71:d3:a3:ec (ECDSA)
    |_  256 8b:cf:41:82:c6:ac:ef:91:80:37:7c:c9:45:11:e8:43 (ED25519)
    5000/tcp open  http    Werkzeug httpd 0.16.1 (Python 3.8.5)
    |_http-title: k1d'5 h4ck3r t00l5

// 
