#! /bin/bash


#
# environment
#
export OMP_NUM_THREADS=1

bindir="/usr/local/bin"
para_prefix="mpirun -np 2"
#para_postfix="-npool 2"

#
# set vars
#
ecut=60.0
alat=6.741
#
nk_list="2 4 6 8 12 16" 

#
# main loop
#
for nk     in $nk_list ; do

   #
   # define filenames
   #
   label="nk${nk}"  
   # label  needs to be updated when other parameters 
   #        are changed at the same time
   #
   filein=scf_${label}.in
   fileout=scf_${label}.out

   #
   # generate the input file
   #
   cat > $filein << EOF

 &CONTROL
    prefix="diamond",
    calculation = "scf"
    restart_mode="from_scratch"
    pseudo_dir = '/home/max/LabQSM/pseudo/'
    outdir = "./SCRATCH"
 /
 &SYSTEM
    ibrav = 2, 
    celldm(1) = $alat
    nat = 2, 
    ntyp = 1,
    ecutwfc =  $ecut
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
 $nk $nk $nk  0 0 0 

EOF

   #
   # running
   echo "Running $label"
   #
   $para_prefix $bindir/pw.x $para_postfix < $filein > $fileout

done
   
