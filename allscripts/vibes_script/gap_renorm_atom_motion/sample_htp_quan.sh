########################################
# Following the tutorial 6, all calculation results were collected in one output file
# However, the script 'extract_bandgaps.py' need every sample's calculation in seperated files
# Thus I wrote this script to do calculation of every sample and record output seperately.
# Need samples already been generated in dir: ../gen_samples/$temp

temp=300K

########################################
# Copy sample geometries to this dir
mkdir samples_$temp
cp ../gen_samples/$(echo ''"$temp"'_quan')/geometry.in.supercell.0* ./samples_$temp
cp ../gen_samples/$(echo ''"$temp"'_quan')/geometry.in.supercell ./
cp ../gen_samples/$(echo ''"$temp"'_quan')/geometry.in.pri* ./


########################################




#######################################
# Do samples calculation
# use 6 samples at this Temperature
#######################################
for sample in 0 1 2 3 4 5; do
        mkdir Sample$sample
        sed '2cgeometry:   ../samples_'"$temp"'/geometry.in.supercell.0300K.00'"$sample"'' aims.in > Sample$sample/aims.in
	cd Sample$sample
	vibes run singlepoint aims.in | tee aims.log
	cd ../
done

for other_sample in 1 2 3 4 5; do
	cd Sample$other_sample/aims/calculations/
	mkdir sample$other_sample
	cp aims.out  control.in  geometry.in  parameters.ase ./sample$other_sample
	mv sample$other_sample ../../../Sample0/aims/calculations/
	cd ../../../
done

cd Sample0
mv aims $temp
cd $temp/calculations/
mkdir sample0
cp aims.out  control.in  geometry.in  parameters.ase ./sample0

