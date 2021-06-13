array=(pbe pbe0 pw-lda)
sub_array=(minimal tier1 tier2 tier3)
for var in ${array[*]}; do
	mkdir $var/
	cd $var/
	mkdir minimal tier1 tier2 tier3
	for sub_var in ${sub_array[*]}; do
		cp ../control.in  $sub_var/
		cp ../geometry.in $sub_var/
		sed -i '4cxc '"${var}"'' ./$sub_var/control.in
	        aims.210226.scalapack.mpi.x >> output
	done
	cd ../
done
#cp control.in geometry.in ./pbe
#sed -i '4c/xc pbe' control.in
