#! /usr/bin/env python3
import sys

def parse_output(fileout,shift):
   #
   skip=True
   read_vkpt=False
   verbosity=False
   lines=[]
   dims={"vkpt":[]}
   with open(fileout,"r") as fl:
     for line in fl: 
       if "number of Kohn-Sham states" in line:
          dims["nbnd"]=int(line.split()[-1])
       #
       if "number of k points" in line:
          dims["nkpts"]=int(line.split()[4])
          read_vkpt=True
       if "Crystallographic axes" in line: verbosity=True
       if ( "k(" in line and read_vkpt):
          k=[float(x.strip("),")) for x in line.split()[4:7] ]
          dims["vkpt"].append(k) 
       if "cryst. coord." in line: read_vkpt=False
       #
       if "End of band structure calculation" in line: skip=False
       if "Writing output data file" in line: skip=True
       if (not skip): lines.append(line)

   #
   # now parse the list of lines
   #
   lines.pop(0)
   #
   nlines=dims["nbnd"]//8
   if (dims["nbnd"]%8>0): nlines+=1

   bands=[]
   for k in range(dims["nkpts"]):
      #
      # parse eigs for a given kpt
      eigs=[]
      for ind in range(3,3+nlines):
         for x in lines[ind].split(): eigs.append(float(x)-shift)
      #
      # add kpt to previous kpt list
      bands.append(eigs)

      #
      # delete lines
      nlines_to_pop=3+nlines
      #
      # AF: parsing fixed, occupations not printed while verbosity=high
      #
      #if verbosity: nlines_to_pop+= 2+nlines
      #
      for ind in range(nlines_to_pop):
         lines.pop(0)
      
      
   #print(bands)
   return dims,bands


if __name__ == "__main__":

   #
   # get cmd line args
   #
   if (len(sys.argv) < 1): 
      print("Usage: %s <file> [opts]",sys.argv[0])
      sys.exit(2)
   #
   filename = sys.argv[1]
   # 
   shift=0.0
   if (len(sys.argv) >= 4 and (sys.argv[2]=="--shift" or sys.argv[2]=="-s")): 
      shift=float(sys.argv[3])

   #
   # parsing
   #
   dims,bands = parse_output(filename,shift)

   #
   # printout
   #
   for ib in range(dims["nbnd"]):
     #
     for ik in range(dims["nkpts"]):
       xk = float(ik)*0.5/float(dims["nkpts"]-1)
       en = bands[ik][ib]    
       print("%15.9f %15.9f" % (xk,en) )
     #
     print("")

