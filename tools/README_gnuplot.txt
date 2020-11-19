
GNUPLOT
 Standard GNU utility to plot 2D and 3D data sets.
 Available on most Unix/Linux machines by default.

Usage:
 type  gnuplot   to start and interactive prompt   
 quit  to exit
 man gnuplot to start the helper 
 Once inside the prompt, follow the commnands below

Plot: 
 > plot 'my-file-name.dat'  using 1:2                # plot cols 1 and 2
 > plot 'my-file-name.dat'  u 1:2                    # as above
 > plot 'my-file-name.dat'  using 1:2  with lines    # as before, with lines
 > plot 'my-file-name.dat'  u 1:2  w l               # as above
 > 

Fit:
 > f(x) = a + b*x + c*x**2
 > fit [xmin:xmax] f(x) 'my-file-name.dat' u 1:2  via a,b,c


===============
Tutorials:
===============

* http://people.duke.edu/~hpgavin/gnuplot.html
 
 
