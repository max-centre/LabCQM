#! /usr/bin/env python3

import os
import numpy as np
import sys


def main():

   #
   bindir = "/opt/QE/qe-6.2/bin"

   #
   # environment
   #
   os.environ["OMP_NUM_THREADS"] = "1"

   para_prefix = "mpirun -np 2 "
   para_postfix="-npool 2 "

   #
   # var to loop on 
   #
   nk_list=[2,4,6,8,12,16]
   ecut=60.0
   alat=6.741
   #
   param_list=[ {"nk":x} for x in nk_list ]

   #
   # main loops
   #
   for param in param_list: 

      nk=param["nk"]
      #
      param["alat"]=alat
      param["ecut"]=ecut

      #
      # define filenames
      #
      label = "nk"+str(nk)
      filein= "scf_"+label+".in"
      fileout="scf_"+label+".out"

      #
      # generate the input file
      #
      fi=open(filein,'w')
      #
      strtmp='''

 &CONTROL
    prefix='diamond',
    calculation = 'scf'
    restart_mode='from_scratch',
    pseudo_dir = '/opt/QE/pseudo/'
    outdir = './SCRATCH'
 /
 &SYSTEM
    ibrav = 2, 
    celldm(1) = @alat@
    nat = 2, 
    ntyp = 1,
    ecutwfc =  @ecut@
 /
 &ELECTRONS
    mixing_mode = 'plain'
    mixing_beta = 0.7
    conv_thr =  1.0d-8
 /
ATOMIC_SPECIES
 C   12.011   C.pz-vbc.UPF
ATOMIC_POSITIONS (alat)
 C 0.00 0.00 0.00
 C 0.25 0.25 0.25
K_POINTS {automatic}
 @nk@ @nk@ @nk@   0 0 0 

      '''
      #
      for key,val in param.items():
         strtmp=strtmp.replace("@"+key+"@",str(val))
      #
      fi.write(strtmp)
      fi.close()

      #
      # running
      print ("Running ",param)
      #
      os.system(para_prefix + bindir+"/pw.x "+para_postfix+" < "+filein+" > "+fileout)


################################

if __name__ == "__main__":
   main()

