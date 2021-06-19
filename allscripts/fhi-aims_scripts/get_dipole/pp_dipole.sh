
for Distance in 0.7 0.8 0.85 0.87 0.89 0.91 0.93 0.95 1.0 1.1 1.2 1.3 ; do
	echo -n "$Distance   " >> dipole.dat
        grep 'Absolute dipole' $Distance/output | awk '{print$9}' >> dipole.dat
done
