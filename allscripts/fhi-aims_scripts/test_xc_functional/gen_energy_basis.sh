#!/bin/bash

basis=$(echo `grep 'Total number of basis functions' output`)
array=($basis)
num_basis=$(echo ${array[7]})

# read number of basis functions and split them into an array use 'array=($basis)'
# echo ${array[7]} pick the 7th content out of array (it's the number)

energy=$(echo `grep 'Total energy uncorrected' output`)
array2=($energy)
energy_unc=$(echo ${array2[5]})

echo ''"$num_basis"' '"$energy_unc"'' >> test.dat

# use echo to write to 'result.dat'
# Attention: when we have variables to write, except for echo ' content ', we use '" $var  "' to sandwitch variables.
# Attention: use one ' and one " to sandwitch variables, and write strings outside.
