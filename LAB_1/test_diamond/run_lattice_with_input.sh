#! /bin/bash -x

bindir=/usr/local/bin

alat0=6.7402778
strain_list="-0.03 -0.02 -0.01 0.0 0.01 0.02 0.03"

for strain in $strain_list
do

   #
   # vars and names
   #
   alat=`echo $alat0 $strain | awk '{print $1*(1.0+$2)}'` 

   filein=scf_strain$strain.in
   fileout=scf_strain$strain.out

   #
   # generate input
   #
   cat > $filein << EOF

 &CONTROL
    prefix='diamond',
    calculation = 'scf'
    restart_mode='from_scratch',
    pseudo_dir = '/home/max/LabQSM/pseudo/'
    outdir = './SCRATCH'
 /
 &SYSTEM
    ibrav = 2, 
    celldm(1) = $alat
    nat = 2, 
    ntyp = 1,
    ecutwfc =  40.0
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
 4 4 4   0 0 0 

EOF

   echo Running $filein
   $bindir/pw.x < $filein > $fileout

done
   

