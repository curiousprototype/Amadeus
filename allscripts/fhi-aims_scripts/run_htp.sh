#Variable defintion:
AIMSBIN='aims.210226.scalapack.mpi.x' #This variable should point to your local FHI-aims executable


#Loop over the distances
for Distance in 0.7 0.8 0.85 0.87 0.89 0.91 0.93 0.95 1.0 1.1 1.2 1.3 ; do
   echo $Distance
   mkdir $Distance;                                                                            # Create directory with the distance as name
   cp control.in.template $Distance/control.in                                                 # copy the control file into the new directoy
   sed "s/Dist/$Distance/g" geometry.in.template > $Distance/geometry.in                       # the the geometry template, replace the term DIST by the current distance and copy the new file into the directory
   cd $Distance;                                                                               # Change directoy
   $AIMSBIN | tee output;                                                                      # Run aims and pipe the output into a file named "output"
   cd ..                                                                                       # Go back to the original directory
done
