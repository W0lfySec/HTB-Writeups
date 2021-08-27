#!/usr/bin/env python

f2 = open("combined_pass.txt", "x")
f = open("pass_extention.txt", "r")

x = 1
d = 100000

while d > x:
   x +=1
   line1 = f.readline(x)
   pass1 = 'Th4C00lTheacha'
   combined = pass1 + line1

   f2.write(combined)


f.close()
f2.close()
