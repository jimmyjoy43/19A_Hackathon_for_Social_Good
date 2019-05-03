#!/bin/bash

csv=$1
cd links_"$csv"
rm ids_and_stamps.txt
for i in ./[0-9]*
do 
paste <(basename $i) <(grep $(basename $i) ../"$csv".csv | cut -d';' -f2) >> ids_and_stamps.txt
done
cp ../timeseries_folderizer.sh .
bash timeseries_folderizer.sh ids_and_stamps.txt
cd ..
