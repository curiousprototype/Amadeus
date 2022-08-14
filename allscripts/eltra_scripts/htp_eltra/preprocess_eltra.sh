
Temp=5
eltra_workpath='/u/jquan/workplace/eltra/He_Chain/5k'


for SC in 2 4 8 10 12 20 ; do
   sample_file="samples_${SC}_${Temp}K"
   KP=$(echo 20.0/$SC |bc)
   sed "s/NNNN/He${SC}/g" job_que.sh.template > $SC/job_que.sh
   sed "s/SC/$SC/g" eltra.in.template > $SC/eltra.in
   sed -i "s/KP/$KP/g" $SC/eltra.in 
   cd $SC
   eltra utils map-prim2super -p geometry.in.primitive -s geometry.in.supercell
   eltra init -sd $sample_file
   eltra submit
   cd ../
done
