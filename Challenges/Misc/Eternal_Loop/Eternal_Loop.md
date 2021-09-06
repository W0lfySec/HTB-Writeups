## -->> Eternal Loop <<--
(attach file = Unzip_htb_EternalLoop.py )

// First we got ziped file called Eternal_Loop.zip , unzip file password: hackthebox
 Now we got another zip file called 37366.zip to unzip this zipped folder we need password
 the password can eazily cracked using [john the ripper](https://www.openwall.com/john/)

    $ zip2john 37366.zip > hash.txt
    Created directory: /home/kali/.john
    ver 2.0 37366.zip/5900.zip PKZIP Encr: cmplen=460497, decmplen=460340, crc=4DB4F8A
    
    $ ls -al
    total 1824
    drwxr-xr-x 2 kali kali   4096 Jul 22 18:51  .
    drwxr-xr-x 4 kali kali   4096 Jul 22 18:47  ..
    -rw-r--r-- 1 kali kali 460611 May 23  2018  37366.zip
    -rw-r--r-- 1 kali kali 460775 Jul 22 18:46 'Eternal Loop.zip'
    -rw-r--r-- 1 kali kali 921113 Jul 22 18:51  hash.txt
    
    $ john hash.txt 
    Using default input encoding: UTF-8
    Loaded 1 password hash (PKZIP [32/64])
    Will run 4 OpenMP threads
    Proceeding with single, rules:Single
    Press 'q' or Ctrl-C to abort, almost any other key for status
    5900             (37366.zip/5900.zip)
    1g 0:00:00:00 DONE 1/3 (2021-07-22 18:52) 12.50g/s 200.0p/s 200.0c/s 200.0C/s z5900..Zip5900
    Use the "--show" option to display all of the cracked passwords reliably
    Session completed
    
// The password 5900 and we extracted another zipped folder but her name is 5900.zip
 Instersting, the password and name of the zipped file are matched
 continued to next file and try the passord that is the name of the zipped file inside.
 I have follow that like 20 times till iquit and understand its not the way.
 I was thinking how to automate that and got to conclution that i need to write a little script that
 will automate the steps of get the name of the inside zipped folder and output the name to unzip password
 
 // i found a way to that with python
 
     #!/usr/bin/env python

    import zipfile
    import time

    # zip file handler
    user_input = input('ZIP file name: ')
    zip = zipfile.ZipFile(user_input + '.zip')

    # list avalible files in container
    print (zip.namelist())
    next_zip = str(zip.namelist())
    print ('---Zipped File---: ' + next_zip)

    # edit the password for contain only numbers
    pass1 = str(''.join(i for i in next_zip if i.isdigit()))
    print ('=Password=: ' + pass1)

    # extract file
    zip.extractall(pwd=bytes(pass1,'utf-8'))

    # wait 4 seconds to extract
    time.sleep(4)
    print ('success!!!')


    a = 100000
    b = 0
    pass2 = 2
    while a > 0:
       testing = str(pass2)
       if testing.isdigit():
          a -= 1
          b += 1
          print('Loop Number: ' + str(b))
          zip2 = zipfile.ZipFile(pass1 + '.zip')
          time.sleep(2)
          next_zip2 = str(zip2.namelist())
          pass2 = str(''.join(i for i in next_zip2 if i.isdigit()))
          print ('Next password: ' + pass2)
          zip2.extractall(pwd=bytes(pass2,'utf-8'))
          pass1 = pass2
       else:
          print ('!!!!!!!! Done !!!!!!!!!!!')
          break


// Output:

    $ python3 Unzip_htb_EternalLoop.py
    ZIP file name: 37366
    ['5900.zip']
    ---Zipped File---: ['5900.zip']
    =Password=: 5900
    success!!!
    Loop Number: 1
    Next password: 49805
    Loop Number: 2
    Next password: 13811
    Loop Number: 3
    Next password: 45133
    Loop Number: 4
    Next password: 4030
    Loop Number: 5
    Next password: 12132
    Loop Number: 6
    .........
    
 // it will run for a while(sorry, didnt found way to make that faster)
 // finally it stops at 6969.zip and for crack this password we will use another tool called fcrackzip
 
    $ fcrackzip -D -p ../../../../wordlists--/rockyou.txt 6969.zip -u

    PASSWORD FOUND!!!!: pw == letmeinplease

// Extracted file called DoNotTouch

    $ file DoNotTouch 
    DoNotTouch: SQLite 3.x database, last written using SQLite version 3021000
// seems to be a sql database file
// we can navigate to online sql viewer: https://inloop.github.io/sqlite/viewer/
// After a lot digging in the tables i found the flag
![Image 1](https://github.com/W0lfySec/HTB-Writeups/blob/main/Images/Eternal_loop/1.png)


### HTB{z1p_and_unz1p_ma_bruddahs}

// could also just search for strings 'HTB' since we know its the start of the flag

    $ strings DoNotTouch | grep 'HTB'
    1969-01-01 00:00:002069-01-01 00:00:00Chillin with SatanHellHTB{z1p_and_unz1p_ma_bruddahs}

