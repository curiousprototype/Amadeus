#!/bin/bash
cd ./q1-in;
cp ../htp_effmass.py ./
echo "q1-in" >> ../all_effmass.txt

for ii in `seq -f "%g" 0 6`; do
	cd mode$ii;
	mv output_in_0.01 calculation.out;
	cd ../;
done
./htp_effmass.py;
cd ../q1-out;
cp ../htp_effmass.py ./
echo "q1-out" >> ../all_effmass.txt

for ii in `seq -f "%g" 0 6`; do
        cd mode$ii;
        mv output_out_0.01 calculation.out;
	cd ../;
done
./htp_effmass.py;
cd ../
