#!/bin/bash -l

ulimit -s unlimited
export OMP_NUM_THREADS=1


srun /u/jquan/download/FHIaims/bin/aims.210513.scalapack.mpi.x
