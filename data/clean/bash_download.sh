#!bin/bash
#usage: bash bash_download.sh linkfile (e.g. links_blahblah.csv)

linkfile=$1
paste <(grep -v ',$' <(tail -n +2 $linkfile) | cut -d, -f2) <(grep -v ',$' <(tail -n +2 $linkfile) | cut -d, -f3) > "$linkfile"_ids_and_photos
cut -f2 "$linkfile"_ids_and_photos | parallel wget {}
mkdir "${linkfile%.*}"
for i in `grep -v ',$' <(tail -n +2 "$linkfile") | cut -d, -f2`; do for j in `grep $i "$linkfile" | cut -f3 | sed 's/.*\///g' | sed 's/\..*//g'`.*; do mv "$j" "${linkfile%.*}"/"$i"_"$j"; done done

