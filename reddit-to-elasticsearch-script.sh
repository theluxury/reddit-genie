#!/bin/bash
set -e
# delete and remake the folders if they exist, since if you don't, could lead to repeated data if script fails later.
#if [ -d tmp/ ]; then
#    rm -rf tmp/
#fi

#mkdir -p tmp/es-json

#aws s3 --recursive --region us-west-2 cp s3://mark-wang-test/namenode tmp/raw-data-download/ #download data
if [ -d tmp/raw-data-download ]; then # if you got a file
    for directory in tmp/raw-data-download/*; do
	if [ -d "${directory}" ]; then
	    python elastic-search/reddit-elasticsearch-bulk.py "tmp/raw-data-download/${directory##*/}/*" #puts into ES
	fi



#	rm "$filename"
 #       aws s3 --region us-west-2 mv s3://mark-wang-test/namenode/$(basename $filename) s3://mark-wang-test/reddit-finished/$(basename $filename)
    done
fi
#rm -rf tmp/





