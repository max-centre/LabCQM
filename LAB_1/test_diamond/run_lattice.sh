#! /bin/bash 

bindir=/usr/local/bin
template=./scf.tmpl

#
# environment
#
export OMP_NUM_THREADS=1
para_prefix="mpirun -np 2"
#para_postfix="-npool 2"

#
# definitions
#
prefix=diamond
ecutwfc=40.0
nk=8
alat0=6.7402778

#
# var to loop on 
strain_list="-0.01 -0.02 -0.03 0.00 0.01 0.02 0.03"

#
# main loop
#
for strain in $strain_list
do

   # define filenames
   filein=scf.diamond_strain${strain}.in
   fileout=scf.diamond_strain${strain}.out
   #
   # define current alat
   alat=`echo $alat0 $strain | awk '{printf "%12.8f", $1*(1.0+$2)}'`
   #
   # generate the input file
   sed "s/@prefix@/$prefix/
        s/@alat@/$alat/
        s/@ecutwfc@/$ecutwfc/
        s/@nk@/$nk/g " $template > $filein

   #
   # running
   echo "Running VARS: $prefix ecutwfc=$ecutwfc nk=$nk alat=$alat"
   #
   $para_prefix $bindir/pw.x $para_postfix < $filein > $fileout

done
   
