for folder in `ls $l`; do
# this command will return all files and folders under path.


        cd $folder/02_*/q1/mode0
#	mv E0/out* E0/calculation.out
#	mv E0 mode0
        if [ -f "band1001.out" ]; then
		# this command return TRUE if file "band1001.out" exist and it's a normal file.
		# use "-d" if you want to judge a directory.
		echo "OK"
	else
		echo "$folder"
	fi
	cd ../../../../
done

