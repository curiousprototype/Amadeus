#!/bin/bash
for ii in `seq -f "%02g" 0 49`; do
    mkdir cv_$ii;
    cp sisso.json data.csv cv_$ii;
    cd cv_$ii;
    mpiexec -n 2 /home/quan/Desktop/researchs/learn_SISSO/SISSO++/maindirectory/bin/sisso++ >cv_runlog;
    cd ../;
done

# seq -f "%02g" 0 9
# means generate numbers between 0 and 9
# %02g means numbers are 'double-digit' and if smaller than 'double-digit', use 0 occupied forward.

