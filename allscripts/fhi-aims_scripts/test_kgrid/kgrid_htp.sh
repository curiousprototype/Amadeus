# Your FHI-aims version
AIMSBIN='aims.210226.scalapack.mpi.x'

for kgrids in 8 12 16 ; do
       echo "kgrids: $kgrids $kgrids $kgrids"
       mkdir $kgrids
       cp geometry.in $kgrids/
       ctrl_kgrid=$(echo "$kgrids $kgrids $kgrids")
       sed "s/3 3 3/$ctrl_kgrid/g" control.in.template > $kgrids/control.in
       cd $kgrids
       $AIMSBIN >> aims.out
       cd ..


done
