for Distance in 0.7 0.8 0.85 0.87 0.89 0.91 0.93 0.95 1.0 1.1 1.2 1.3 ; do
	echo -n "$Distance  " >> Mulliken.dat
        awk '/per-atom charge/ {for (i=1;i<=4;i++){getline;print}}' $Distance/output | awk '{if (NR==3 || NR==4){printf("%-10s", $4)}}' >> Mulliken.dat
	echo -en '\n' >> Mulliken.dat
# first awk: search for line with "per-atom charge" and output the following 4 lines
# in the loop (i=1;i<=4;i++), 'getline' means go to the next line, and then print content.
# second awk: print atom charges for the 1st and 2nd atom. NR==3 is the 1st atom
# || means or, && means and
# use printf can make awk print without \n
# "%-10s" means output 10 place string or number. Here I use it for space between 2 charges.
# echo -e means explain escape characters.
done
