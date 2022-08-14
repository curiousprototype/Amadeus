echo "RS      tdA      tdB      average  (unit: 100A^2)   " >> /u/jquan/workplace/zpr-aims/RS/htp_lo/thermo_displacement.dat
for folder in `ls $l`; do
        if [ -d $folder ]; then

                cd $folder/phonopy/output
                mkdir td_calculate
                cp FORCE_SETS geometry.in.primitive ./td_calculate
                cp /u/jquan/workplace/zpr-aims/RS/htp_lo/mesh.conf ./td_calculate
                cd td_calculate
                mv geometry.in.primitive geometry.in
                phonopy --td --aims mesh.conf
                echo -n "$folder   " >> /u/jquan/workplace/zpr-aims/RS/htp_lo/thermo_displacement.dat
                tdA_raw=$(sed -n 7p thermal_displacements.yaml | awk '{print$3}')
                tdB_raw=$(sed -n 8p thermal_displacements.yaml | awk '{print$3}')
                # read thermal displacement of element A from this .yaml file
                # Attention: it's with comma at it's tail, use ${td_raw%?} to delete the comma.

                tdA=${tdA_raw%?}
                tdB=${tdB_raw%?}

                tdA_sqrt=$(echo "sqrt($tdA * 100)" |bc | awk '{printf "%.6f", $0}')
                # change unit from A^2 to 100A^2
                tdB_sqrt=$(echo "sqrt($tdB * 100)" |bc | awk '{printf "%.6f", $0}')
                average_td=$(awk 'BEGIN{print ('$tdA_sqrt'+'$tdB_sqrt')/2}')
                echo "$tdA_sqrt   $tdB_sqrt   $average_td " >> /u/jquan/workplace/zpr-aims/RS/htp_lo/thermo_displacement.dat
                cd ../../../../
        fi
done

