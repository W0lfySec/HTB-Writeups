## ------------------->> Unobtainium <<-------------------

// We start with nmap scan

    $ nmap -sV -A -Pn -T4 10.10.10.235 -p-
---------

    Nmap scan report for 10.10.10.235
    Host is up (0.22s latency).
    Not shown: 65526 closed ports
    PORT      STATE SERVICE          VERSION
    22/tcp    open  ssh              OpenSSH 8.2p1 Ubuntu 4ubuntu0.2 (Ubuntu Linux; protocol 2.0)
    | ssh-hostkey: 
    |   3072 e4:bf:68:42:e5:74:4b:06:58:78:bd:ed:1e:6a:df:66 (RSA)
    |   256 bd:88:a1:d9:19:a0:12:35:ca:d3:fa:63:76:48:dc:65 (ECDSA)
    |_  256 cf:c4:19:25:19:fa:6e:2e:b7:a4:aa:7d:c3:f1:3d:9b (ED25519)
    80/tcp    open  http             Apache httpd 2.4.41 ((Ubuntu))
    |_http-server-header: Apache/2.4.41 (Ubuntu)
    |_http-title: Unobtainium
    2379/tcp  open  ssl/etcd-client?
    | ssl-cert: Subject: commonName=unobtainium
    | Subject Alternative Name: DNS:localhost, DNS:unobtainium, IP Address:10.10.10.3, IP Address:127.0.0.1, IP Address:0:0:0:0:0:0:0:1
    | Not valid before: 2021-01-17T07:10:30
    |_Not valid after:  2022-01-17T07:10:30
    |_ssl-date: TLS randomness does not represent time
    | tls-alpn: 
    |_  h2
    | tls-nextprotoneg: 
    |_  h2
    2380/tcp  open  ssl/etcd-server?
    | ssl-cert: Subject: commonName=unobtainium
    | Subject Alternative Name: DNS:localhost, DNS:unobtainium, IP Address:10.10.10.3, IP Address:127.0.0.1, IP Address:0:0:0:0:0:0:0:1
    | Not valid before: 2021-01-17T07:10:30
    |_Not valid after:  2022-01-17T07:10:30
    |_ssl-date: TLS randomness does not represent time
    | tls-alpn: 
    |_  h2
    | tls-nextprotoneg: 
    |_  h2
    8443/tcp  open  ssl/https-alt
    | fingerprint-strings: 
    |   FourOhFourRequest: 
    |     HTTP/1.0 403 Forbidden
    |     Cache-Control: no-cache, private
    |     Content-Type: application/json
    |     X-Content-Type-Options: nosniff
    |     X-Kubernetes-Pf-Flowschema-Uid: 3082aa7f-e4b1-444a-a726-829587cd9e39
    |     X-Kubernetes-Pf-Prioritylevel-Uid: c4131e14-5fda-4a46-8349-09ccbed9efdd
    |     Date: Fri, 03 Sep 2021 10:43:05 GMT
    |     Content-Length: 212
    |     {"kind":"Status","apiVersion":"v1","metadata":{},"status":"Failure","message":"forbidden: User "system:anonymous" cannot get path "/nice ports,/Trinity.txt.bak"","reason":"Forbidden","details":{},"code":403}
    |   GenericLines: 
    |     HTTP/1.1 400 Bad Request
    |     Content-Type: text/plain; charset=utf-8
    |     Connection: close
    |     Request
    |   GetRequest: 
    |     HTTP/1.0 403 Forbidden
    |     Cache-Control: no-cache, private
    |     Content-Type: application/json
    |     X-Content-Type-Options: nosniff
    |     X-Kubernetes-Pf-Flowschema-Uid: 3082aa7f-e4b1-444a-a726-829587cd9e39
    |     X-Kubernetes-Pf-Prioritylevel-Uid: c4131e14-5fda-4a46-8349-09ccbed9efdd
    |     Date: Fri, 03 Sep 2021 10:43:03 GMT
    |     Content-Length: 185
    |     {"kind":"Status","apiVersion":"v1","metadata":{},"status":"Failure","message":"forbidden: User "system:anonymous" cannot get path "/"","reason":"Forbidden","details":{},"code":403}
    |   HTTPOptions: 
    |     HTTP/1.0 403 Forbidden
    |     Cache-Control: no-cache, private
    |     Content-Type: application/json
    |     X-Content-Type-Options: nosniff
    |     X-Kubernetes-Pf-Flowschema-Uid: 3082aa7f-e4b1-444a-a726-829587cd9e39
    |     X-Kubernetes-Pf-Prioritylevel-Uid: c4131e14-5fda-4a46-8349-09ccbed9efdd
    |     Date: Fri, 03 Sep 2021 10:43:04 GMT
    |     Content-Length: 189
    |_    {"kind":"Status","apiVersion":"v1","metadata":{},"status":"Failure","message":"forbidden: User "system:anonymous" cannot options path "/"","reason":"Forbidden","details":{},"code":403}
    |_http-title: Site doesn't have a title (application/json).
    | ssl-cert: Subject: commonName=minikube/organizationName=system:masters
    | Subject Alternative Name: DNS:minikubeCA, DNS:control-plane.minikube.internal, DNS:kubernetes.default.svc.cluster.local, DNS:kubernetes.default.svc, DNS:kubernetes.default, DNS:kubernetes, DNS:localhost, IP Address:10.10.10.235, IP Address:10.96.0.1, IP Address:127.0.0.1, IP Address:10.0.0.1
    | Not valid before: 2021-07-25T14:52:45
    |_Not valid after:  2022-07-26T14:52:45
    |_ssl-date: TLS randomness does not represent time
    | tls-alpn: 
    |   h2
    |_  http/1.1
    10249/tcp open  http             Golang net/http server (Go-IPFS json-rpc or InfluxDB API)
    |_http-title: Site doesn't have a title (text/plain; charset=utf-8).
    10250/tcp open  ssl/http         Golang net/http server (Go-IPFS json-rpc or InfluxDB API)
    |_http-title: Site doesn't have a title (text/plain; charset=utf-8).
    | ssl-cert: Subject: commonName=unobtainium@1610865428
    | Subject Alternative Name: DNS:unobtainium
    | Not valid before: 2021-01-17T05:37:08
    |_Not valid after:  2022-01-17T05:37:08
    |_ssl-date: TLS randomness does not represent time
    | tls-alpn: 
    |   h2
    |_  http/1.1
    10256/tcp open  http             Golang net/http server (Go-IPFS json-rpc or InfluxDB API)
    |_http-title: Site doesn't have a title (text/plain; charset=utf-8).
    31337/tcp open  http             Node.js Express framework
    | http-methods: 
    |_  Potentially risky methods: PUT DELETE
    |_http-title: Site doesn't have a title (application/json; charset=utf-8).


// 


    $ python3 dirsearch.py -u http://10.10.10.235/ -t 100 -w /usr/share/dirb/wordlists/big.txt 
--------

      _|. _ _  _  _  _ _|_    v0.4.1
     (_||| _) (/_(_|| (_| )

    Extensions: php, aspx, jsp, html, js | HTTP method: GET | Threads: 100 | Wordlist size: 20469

    Output File: /home/r4r3/Desktop/HTB/main-Tools/web/directories_scanners/dirsearch/reports/10.10.10.235/_21-09-03_06-51-47.txt

    Error Log: /home/r4r3/Desktop/HTB/main-Tools/web/directories_scanners/dirsearch/logs/errors-21-09-03_06-51-47.log

    Target: http://10.10.10.235/

    [06:51:48] Starting: 
    [06:51:53] 301 -  313B  - /assets  ->  http://10.10.10.235/assets/
    [06:51:58] 301 -  316B  - /downloads  ->  http://10.10.10.235/downloads/
    [06:52:02] 301 -  313B  - /images  ->  http://10.10.10.235/images/
    [06:52:12] 403 -  277B  - /server-status

// 


    $ python3 dirsearch.py -u https://10.10.10.235:8443/ -t 100 -w /usr/share/dirb/wordlists/big.txt 
---------

      _|. _ _  _  _  _ _|_    v0.4.1
     (_||| _) (/_(_|| (_| )

    Extensions: php, aspx, jsp, html, js | HTTP method: GET | Threads: 100 | Wordlist size: 20469

    Output File: /home/r4r3/Desktop/HTB/main-Tools/web/directories_scanners/dirsearch/reports/10.10.10.235/_21-09-03_06-52-29.txt

    Error Log: /home/r4r3/Desktop/HTB/main-Tools/web/directories_scanners/dirsearch/logs/errors-21-09-03_06-52-29.log

    Target: https://10.10.10.235:8443/

    [06:52:30] Starting: 
    [06:53:28] 200 -  263B  - /version


//

    $ python3 dirsearch.py -u https://10.10.10.235:10250/ -t 100 -w /usr/share/dirb/wordlists/big.txt 
------------

      _|. _ _  _  _  _ _|_    v0.4.1
     (_||| _) (/_(_|| (_| )

    Extensions: php, aspx, jsp, html, js | HTTP method: GET | Threads: 100 | Wordlist size: 20469

    Output File: /home/r4r3/Desktop/HTB/main-Tools/web/directories_scanners/dirsearch/reports/10.10.10.235/_21-09-03_07-08-09.txt

    Error Log: /home/r4r3/Desktop/HTB/main-Tools/web/directories_scanners/dirsearch/logs/errors-21-09-03_07-08-09.log

    Target: https://10.10.10.235:10250/

    [07:08:09] Starting: 
    [07:08:15] 401 -   12B  - /attach
    [07:08:22] 401 -   12B  - /exec
    [07:08:29] 301 -   41B  - /logs  ->  /logs/
    [07:08:30] 401 -   12B  - /metrics
    [07:08:33] 401 -   12B  - /pods
    [07:08:36] 401 -   12B  - /run
    [07:08:38] 301 -   42B  - /stats  ->  /stats/

    Task Completed

//

    $ python3 dirsearch.py -u http://10.10.10.235:10249/ -t 100 -w /usr/share/dirb/wordlists/big.txt 
---------

      _|. _ _  _  _  _ _|_    v0.4.1
     (_||| _) (/_(_|| (_| )

    Extensions: php, aspx, jsp, html, js | HTTP method: GET | Threads: 100 | Wordlist size: 20469

    Output File: /home/r4r3/Desktop/HTB/main-Tools/web/directories_scanners/dirsearch/reports/10.10.10.235/_21-09-03_07-09-46.txt

    Error Log: /home/r4r3/Desktop/HTB/main-Tools/web/directories_scanners/dirsearch/logs/errors-21-09-03_07-09-46.log

    Target: http://10.10.10.235:10249/

    [07:09:47] Starting: 
    [07:10:05] 200 -   27KB - /metrics


// 




// https://10.10.10.235:8443/version


{
  "major": "1",
  "minor": "20",
  "gitVersion": "v1.20.0",
  "gitCommit": "af46c47ce925f4c4ad5cc8d1fca46c7b77d13b38",
  "gitTreeState": "clean",
  "buildDate": "2020-12-08T17:51:19Z",
  "goVersion": "go1.15.5",
  "compiler": "gc",
  "platform": "linux/amd64"
}



// http://10.10.10.235:31337/

[{"icon":"__","id":1,"timestamp":1630666833826,"userName":"felamos"},{"icon":"__","id":2,"timestamp":1630666879163,"userName":"felamos"}]



