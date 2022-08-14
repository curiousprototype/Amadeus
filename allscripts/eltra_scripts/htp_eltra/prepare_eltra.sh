
Temp=5
eltra_workpath='/u/jquan/workplace/eltra/He_Chain/5k'


for SC in 2 4 8 10 12 20 ; do
  sample_file="samples_${SC}_${Temp}K"
  echo $sample_file
  mkdir $eltra_workpath/$SC/$sample_file
  cp $SC/phonopy/output/geometry.in.supercell.00* $eltra_workpath/$SC/$sample_file
  cp $SC/phonopy/output/geometry.in.supercell $eltra_workpath/$SC/
  cp $SC/phonopy/output/geometry.in.primitive $eltra_workpath/$SC/
done
