#! /usr/bin/env python3
import sys

def parse_output(fileout):
   outd={}
   fl=open(fileout,"r") 
   for line in fl: 
     if "lattice parameter (alat)" in line:
       outd["alat"]=float(line.split()[-2])
     if "unit-cell volume" in line:
       outd["volume"]=float(line.split()[-2])
     if "number of Kohn-Sham states" in line:
       outd["nbnd"]=int(line.split()[-1])
     if "kinetic-energy cutoff" in line:
       outd["ecutwfc"]=float(line.split()[-2])
     if "charge density cutoff" in line:
       outd["ecutrho"]=float(line.split()[-2])
     if "Exchange-correlation" in line:
       outd["xc-functional"]=line.split()[2:]
     if "number of k points" in line:
       outd["nkpts"]=int(line.split()[4])
     if "FFT dimensions" in line:
       outd["rho_gvectors"]=int(line.split()[2])
       outd["nfft1"]=int(line.split()[-3].replace(",",""))
       outd["nfft2"]=int(line.split()[-2].replace(",",""))
       outd["nfft3"]=int(line.split()[-1].replace(")",""))
     if "!" in line: 
       outd["energy"]=float(line.split()[-2])
   fl.close()
   return outd

def main(argv):
   flist=argv
   for f in flist[1:]:
     outd=parse_output(f)
     print("file: "+f)
     print(outd)
     print()

if __name__ == "__main__":
   main(sys.argv)
