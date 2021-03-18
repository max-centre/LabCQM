#!/usr/bin/env python3

import sys
import numpy as np

if (len(sys.argv)<=1):
   print("USAGE: %s <filein> " % sys.argv[0])
   sys.exit(2)

filein=sys.argv[1]
#
conv=0.529177
shift=[14.0*conv, 14.0*conv, 0.0]

#=======

with open(filein) as f:
  print(f.readline().strip("\n"))
  print(f.readline().strip("\n"))
  #
  for line in f.readlines():
     lineout=line.split()
     if (len(lineout)<4):
        print(str(lineout)[1:-1])
        continue
     for i in range(3): 
        lineout[i+1]=float(lineout[i+1])+shift[i]
     print("%5s  %15.9f %15.9f %15.9f" % tuple(lineout))
  

