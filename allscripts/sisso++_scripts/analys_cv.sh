#!/bin/bash
for ii in `seq -f "%02g" 0 59`; do
    cd cv_$ii/models;
    sed -n '3 p' test_dim_1_model_0.dat >> ../../cv_result_1d.txt
    sed -n '12 p' test_dim_1_model_0.dat >> ../../cv_result_1d.txt
    cd ../../;
done

# sed -n 'n,m p' file1 > file2
# copy from n to m lines of file1 and add to file2

# Attention: use symbol > the result will replace origin content of file2

#            use symbol >> the result will add afterwards the final line of file2

