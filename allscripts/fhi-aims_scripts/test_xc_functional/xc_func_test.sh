
file_array=(pbe pbe0 pw-lda)
sub_array=(minimal tier1 tier2 tier3)
a=2
for var in ${file_array[*]}; do
        mkdir $var/
        cd $var/
        mkdir minimal tier1 tier2 tier3
        for sub_var in ${sub_array[*]}; do
                cp ../hf/$sub_var/control.in  $sub_var/
                cp ../geometry.in $sub_var/
                sed -i '4cxc '"${var}"'' ./$sub_var/control.in   # use '"  "' to sandwitch variables
		# sed -i '4cxxx' file_name
		# means replace the 4th line of 'file_name' by content xxx.
		# -i means rewrite the file directly, do not show at the terminal

		cd ./$sub_var
                aims.210226.scalapack.mpi.x >> output

		# Next: post-process: generate result files

		basis=$(echo `grep 'Total number of basis functions' output`)
                array=($basis)
                num_basis=$(echo ${array[7]})

               # read number of basis functions and split them into an array use 'array=($basis)'
               # echo ${array[7]} pick the 7th content out of array (it's the number)

               energy=$(echo `grep 'Total energy uncorrected' output`)
               array2=($energy)
               energy_unc=$(echo ${array2[5]})

               echo ''"$num_basis"'   '"$energy_unc"'' >> ../../result$a.dat
	       cd ../ 


        done

	a=$(($a+1))
        cd ../
done
	# Collect different basis function number for same xc function

awk 'NR==FNR{a[NR]=$0; nr=NR;} NR > FNR{print a[NR-nr], $2}' result1.dat result2.dat > sum2.dat

       # NR is the line number that awk read, for many files NR don't reset to 0 at the beginning of each file
       # FNR is similar, but set to 0 at the beginning of each file
       # NR == FNR means deal with the same file (the first file)
       # NR > FNR means deal with the second file
       # a[NR] = $0 a[NR] is an array, $0 means the whole content of the line NR. Thus this means
       # give the content of number NR lineto to a[NR]
       # nr = NR , store number of lines of the first file, so that can judge where the 2nd file start
       # {print a[NR-nr], $2} means first print content of 1st file and then the second column of the 2nd file.

for num in `seq -f "%2g" 2 3`; do


        awk 'NR==FNR{a[NR]=$0; nr=NR;} NR > FNR{print a[NR-nr], $2}' sum$num.dat result$(($num+1)).dat > sum$(($num+1)).dat
        rm sum$num.dat
done

