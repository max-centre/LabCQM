#!/usr/bin/env python3

import sys
import numpy as np

if (len(sys.argv)<=1):
   print("USAGE: %s <filein> " % sys.argv[0])
   sys.exit(2)

filein=sys.argv[1]

#
# parse the file
#
with open(filein,'r') as f:
   #  
   line=f.readline()
   #
   line=f.readline()
   nfft=[int(x) for x in line.split()[0:3]]
   natom=int(line.split()[-2])
   nsp=int(line.split()[-1])
   #
   line=f.readline()
   celldm=[float(x) for x in line.split()[1:7]]
   #
   line=f.readline()
   #
   print("nfft",nfft)
   print("natom",natom)
   print("nspecies",nsp)
   print("celldm",celldm)
   #
   # (index, symbol, pp_charge)
   pseudo=[]  
   for i in range(nsp):
     line=f.readline() 
     pseudo.append(line.split())
   print("Pseudo ",pseudo)
   #
   # (coords, type)
   atoms=[]
   for ia in range(natom):
     line=f.readline() 
     atoms.append(line.split()[1:5])
   #
   for atom in atoms: print("Atom ",atom)

   # read the main field
   #
   rho=[]
   for line in f.readlines():
      for x in line.split(): rho.append(float(x))

#
# some checks
#
if (celldm[3]!=0.0 or celldm[4]!=0.0 or celldm[5]!=0.0):
   print("Cell is not orthorombic")
   sys.exit(3)

alat=[None]*3
alat[0]=celldm[0]
alat[1]=celldm[0]*celldm[1]
alat[2]=celldm[0]*celldm[2]
volume=celldm[0]**3 * celldm[1]*celldm[2]
print("volume",volume)


#
# grid map
#
def grid(n,nfft):
  ''' returns the x,y,z coordinates of the grid point
      in crystal units 
      n = i + (j-1)*nx + (k-1)*nx*ny
      i=0,nx-1  j=0,ny-1  z=0,nz
  '''
  i=1+(n)%nfft[0]
  j=1+(n+1-i)%(nfft[0]*nfft[1])//nfft[0]
  k=1+(n+1-i-(j-1)*nfft[0])//(nfft[0]*nfft[1])
  return ((i-1)/nfft[0],(j-1)/nfft[1],(k-1)/nfft[2])
  
def renorm(x):
  y=x%1.0
  if (y>0.5):  y=y-1.0
  if (y<-0.5): y=y+1.0
  if (y<-0.5 or y>0.5):
    print("Error: Unexpected val")
    sys.exit(4)
  return y

#
# ionic dipole
#
center=np.zeros(3)
q_ion=0.0
#
for atom in atoms:
  ityp = int(atom[3])
  q    = float(pseudo[ityp-1][-1])
  q_ion += q
  for i in range(3):
    center[i] = center[i] + q * float(atom[i])*alat[0]

center=center/q_ion

print()
print("charge ion: %15.9f [e]" % q_ion)
print("center ion: %15.9f %15.9f %15.9f [bohr]" % tuple(center))
print("dipole ion: %15.9f %15.9f %15.9f [e*bohr]" % (0.0,0.0,0.0) )
   
#
# electronic dipole
#
dipole_el=np.zeros(3)
q_el=0.0
#
#fout=open('file.dat','w')

for n in range(len(rho)):
  val=rho[n]
  q_el += val
  x=grid(n,nfft)
  #
  for i in range(3):
    dipole_el[i] = dipole_el[i] - val * renorm( x[i]-center[i]/alat[i] ) *alat[i]

const=volume/len(rho)
q_el=q_el*const
dipole_el=dipole_el*const   
conv_au2debye = 2.541766
#
print()
print("charge el:  %15.9f [e]" % q_el)
print("dipole el:  %15.9f %15.9f %15.9f [e*bohr]" % tuple(dipole_el))
print("    norm =  %15.9f [e*bohr]" % np.linalg.norm(dipole_el))
print("            %15.9f %15.9f %15.9f [Debye]"  % tuple(dipole_el*conv_au2debye))
print("    norm =  %15.9f [Debye]"  % np.linalg.norm(dipole_el*conv_au2debye))

