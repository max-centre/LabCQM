#! /usr/bin/env python3

import os
import sys
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d
from scipy.interpolate import CubicSpline

def main(argv):

  if (len(argv)>2 or len(argv)==1):
     print(argv[0]+ " <filein>")
     sys.exit(2)

  filedat=argv[1]

  #
  # read data
  #
  data=np.loadtxt(filedat)
  #print(data)
  xl=data[:,0]
  yl=data[:,1]

  #
  # interpolate
  #
  fint=interp1d(xl, yl, kind='cubic')
  #fint=CubicSpline(xl, yl)
  xint=np.linspace(xl.min(),xl.max(),num=2001,endpoint=True)
  yint=fint(xint)
  #
  minx=xint[list(yint).index(yint.min())]
  print("Lattice at Emin: "+str(minx))
 
  #
  # plot data
  #
  #sys.exit(0)  # avoid plotting
  #
  plt.plot(xl,yl,"ro",xint,yint,"g")
  plt.xlabel("Alat [ArbUnit]")
  plt.ylabel("Energy [Ry]")
  plt.show()


if __name__ == "__main__":
   main(sys.argv)


def readin_alt():
  fl=open(filedat,'r')
  xl=[]
  yl=[]
  for line in fl:
    xl.append(line.split()[0])
    yl.append(line.split()[1])
  fl.close()
  return xl,yl

