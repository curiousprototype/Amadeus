#!/bin/bash -l
# Standard output and error:
#SBATCH -o ./job.out.%j
#SBATCH -e ./job.err.%j
# Initial working directory:
#SBATCH -D ./
# Job Name:
#SBATCH -J RS_htp
#SBATCH --nodes=4
#SBATCH --ntasks-per-node=72
# Wall clock limit (max. is 24 hours):
#SBATCH --time=24:00:00
#SBATCH --mem=200000

export OMP_NUM_THREADS=1

for folder in `ls $l`; do
        if [ -d $folder ]; then

	        cd $folder
	        vibes run phonopy &> log.phonopy



                vibes output phonopy phonopy/trajectory.son -v -bs > result.txt
                echo -n "$folder   " >> ../RS_W_LO.dat
                #tac result.txt | sed -n 5p | awk '{print$2}' >> collect.txt
                lo_THz=$(tac result.txt | sed -n 5p | awk '{print$2}')
                lo_cm=$(echo "$lo_THz * 33.35641" |bc)
                echo "$lo_THz  $lo_cm" >> ../RS_W_LO.dat
	        cd ../
	fi
done
