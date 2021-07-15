#!/bin/bash -l
# Standard output and error:
#SBATCH -o ./job.out.%j
#SBATCH -e ./job.err.%j
# Initial working directory:
#SBATCH -D ./
# Job Name:
#SBATCH -J zb_polar
#SBATCH --nodes=8
#SBATCH --ntasks-per-node=12
#SBATCH --cpus-per-task=8

# Wall clock limit (max. is 24 hours):
#SBATCH --time=24:00:00
#SBATCH --mem=240000

ulimit -s unlimited
export OMP_NUM_THREADS=$SLURM_CPUS_PER_TASK

# For pinning threads correctly:
export OMP_PLACES=cores
srun /u/jquan/download/SISSO++/bin/sisso++ 

