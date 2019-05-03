#!bin/bash
#usage: bash bash_download.sh linkfile (e.g. links_blahblah.csv)

linkfile=$1
mkdir -p "${linkfile%.*}"
cd "${linkfile%.*}"
parallel --link bash ../bash_downloader.sh {1} {2} ::: `cat <(grep -v ',$' <(tail -n +2 ../$linkfile) | cut -d, -f2)` ::: `cat <(grep -v ',$' <(tail -n +2 ../$linkfile) | cut -d, -f3)`
cd ..
