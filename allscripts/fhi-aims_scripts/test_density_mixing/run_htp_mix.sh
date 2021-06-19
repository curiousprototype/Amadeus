#Variable defintion:
AIMSBIN='aims.210226.scalapack.mpi.x' #This variable should point to your local FHI-aims executable
mix_type='pulay'
param=0.1
#Loop over the distances
for pulay in 3 8 5 ; do
   echo $pulay
   mkdir $pulay;                                                                            # Create directory with the distance as name
   cp geometry.in.template $pulay/geometry.in                                                 # copy the control file into the new directoy
   sed "s/TYPE/$mix_type/g" control.in.template > $pulay/control.in
   sed -i "s/NUM/$pulay/g" $pulay/control.in                       # Flay -i means change origin file directly
   sed -i "s/PARA/$param/g" $pulay/control.in
   param=$(echo '0'"$(echo $param+0.1 |bc)"'')                # bc is the decimal calculator in shell
   cd $pulay;                                                                               
   $AIMSBIN | tee output;                                                                      # Run aims and pipe the output into a file named "output"
   cd ..                                                                                       # Go back to the original directory
done
