#! /usr/bin/env python3

import os
import sys
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import UnivariateSpline, interp1d


def main(argv):

  #
  # units
  # 1 Ha/Bohr3 = 29421.02648438959 GPa
  #
  conv_RYAU_2_GPA=14710.513242194795

  if (len(argv)==1):
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
  # and perform the second derivative
  #
  x=np.asarray(xl)
  y=np.asarray(yl)

  fint=UnivariateSpline(x, y, k=4, s=0)
  xint=np.linspace(x.min(),x.max(),num=1001,endpoint=True)
  yint=fint(xint)
  d2yint=fint.derivative(n=2)(xint)

  #
  # extract the value at the minimum
  #
  ind=list(yint).index(yint.min())
  Bmod=xint[ind]*d2yint[ind]
  print("Bulk Modulus = "+str(Bmod) + " [Ry/a0^3]")
  print("             = "+str(Bmod*conv_RYAU_2_GPA) + " [GPa]")

  #
  # plot data
  #
  sys.exit(0)  # avoid plotting
  #
  #plt.plot(x,y,"ro",xint,yint,"g",xint,d2yint,"b")
  plt.plot(x,y,"ro",xint,yint,"g")
  plt.xlabel("Volume [a0^3]")
  plt.ylabel("Energy [Ry]")
  plt.show()


if __name__ == "__main__":
   main(sys.argv)


