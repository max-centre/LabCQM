
#
# load a datafile
# and create plot-ready arrays
#
  import numpy as np

  data=np.loadtxt(filedat)
  x=data[:,0]
  y=data[:,1]

#
# plot
#
  import matplotlib.pyplot as plt

  plt.plot(x,y,"b-")
  plt.show()

#
# interpolate
#
  from scipy.interpolate import interp1d, CubicSpline

  f_int=interp1d(x, y, kind='cubic')
  # here is an alternative option
  #f_int=CubicSpline(x, y)

  x_int=np.linspace(x.min(),x.max(),num=1001,endpoint=True)
  y_int=f_int(x_int)

  # replot
  plt.plot(x,y,"ro",x_int,y_int,"g")
  plt.show()

#
# polynomial fitting
#
  import numpy as np

  pc = np.polyfit(x, y, deg=2)    # fit the coefficients
  p  = np.poly1d(pc)              # define the fitting polynomial
  #
  x_int=np.linspace(minval,maxval,num=1001,endpoint=True)
  y_int=p(x_int)                  # eval the polynomial

