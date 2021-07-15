
mkdir htp_lo
cd RS_raw_files/RS/

for folder in `ls $l`; do
	element1=$(sed -n 6p $folder/02_calc_q_ZPR/q1-in/E0/geometry.in | awk '{print$5}')
	element2=$(sed -n 7p $folder/02_calc_q_ZPR/q1-in/E0/geometry.in | awk '{print$5}')
	mkdir ../../htp_lo/"$element1""$element2"
	cp $folder/02_calc_q_ZPR/q1-in/E0/geometry.in ../../htp_lo/"$element1""$element2"
	cp ../../phonopy.in ../../htp_lo/"$element1""$element2"

done
