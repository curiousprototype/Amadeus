# This script is to generate summary of convergence test for different xc functionals

awk 'NR==FNR{a[NR]=$0; nr=NR;} NR > FNR{print a[NR-nr], $2}' result1.dat result2.dat > sum2.dat

# NR is the line number that awk read, for many files NR don't reset to 0 at the beginning of each file
# FNR is similar, but set to 0 at the beginning of each file
# NR == FNR means deal with the same file (the first file)
# NR > FNR means deal with the second file
# a[NR] = $0 a[NR] is an array, $0 means the whole content of the line NR. Thus this means
# give the content of number NR lineto to a[NR]
# nr = NR , store number of lines of the first file, so that can judge where the 2nd file start
# {print a[NR-nr], $2} means first print content of 1st file and then the second column of the 2nd file.

for num in `seq -f "%g" 2 3`; do
       	
	awk 'NR==FNR{a[NR]=$0; nr=NR;} NR > FNR{print a[NR-nr], $2}' sum$num.dat result$(($num+1)).dat > sum$(($num+1)).dat
        rm sum$num.dat
done
