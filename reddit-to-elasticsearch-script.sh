#!/bin/bash
set -e
# delete and remake the folders if they exist, since if you don't, could lead to repeated data if script fails later.
if [ -d tmp/ ]; then
    rm -rf tmp/
fi

mkdir -p tmp/es-json

aws s3 --recursive --region us-west-2 cp s3://mark-wang-test/namenode tmp/raw-data-download/ #download data
if [ -d tmp/raw-data-download ]; then # if you got a file
    for filename in tmp/raw-data-download/*; do 
	python elastic-search/reddit-parser.py "$filename" "tmp/es-json/" # aggregate data
	python elastic-search/elasticsearch-bulk.py "http://ec2-52-35-132-98.us-west-2.compute.amazonaws.com:9201" "tmp/es-json/*" #puts into ES

	rm "$filename"
        aws s3 --region us-west-2 mv s3://mark-wang-test/namenode/$(basename $filename) s3://mark-wang-test/reddit-finished/$(basename $filename)
    done
fi
rm -rf tmp/





