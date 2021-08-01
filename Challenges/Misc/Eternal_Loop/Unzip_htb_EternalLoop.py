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

