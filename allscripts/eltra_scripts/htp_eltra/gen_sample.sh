Temp=5

for SC in 2 4 8 10 12 20 ; do
   KP=$(echo 20.0/$SC |bc)
   echo $SC
#   mkdir $SC
#   cp ./geometry.in $SC/
#   sed "s/SC/$SC/g" phonopy.in.template > $SC/phonopy.in
#   sed -i "s/KP/$KP/g" $SC/phonopy.in
   cd $SC


#   vibes run phonopy &> log.phonopy

#   vibes output phonopy phonopy/trajectory.son -bs > result.txt
   cd phonopy/output/
#   vibes utils fc remap >> sample_log.txt
   vibes utils create-samples geometry.in.supercell -fc FORCE_CONSTANTS_remapped -n 10 -T $Temp >> sample_log.txt
   cd ../../../

done

