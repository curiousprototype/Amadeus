
for Distance in 0.7 0.8 0.85 0.87 0.89 0.91 0.93 0.95 1.0 1.1 1.2 1.3 ; do

#  FLAG  -n means do not output line breaks.
#  so that these two values can write in the same line.
        echo -n "$Distance   " >> result_energy.dat
        grep 'Total energy uncor' $Distance/output | awk '{print $6}' >> result_energy.dat


# The other method is: assign these 2 values to variables, and then use echo to write in file.
#echo ''"$distance"'   '"$energy"'' >> test.dat
done
