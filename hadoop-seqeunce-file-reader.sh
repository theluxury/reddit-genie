#!/bin/bash
set -e
# aws s3 --region us-west-2 cp s3://mark-wang-test/raw_logs/secor_backup/my-topic/offset=0/1_0_00000000000000000000 raw-data-download/ 
# delete and remake the folders if they exist, since if you don't, could lead to repeated data if script fails later.
if [ -d tmp/ ]; then
    rm -rf tmp/
fi

mkdir -p tmp/decoded-tweets # since forqlift doesn't make new directories
mkdir tmp/es-json

aws s3 --recursive --region us-west-2 cp s3://mark-wang-test/dummy/ tmp/raw-data-download/ #download data
if [ -d tmp/raw-data-download ]; then # if you got a file
    for filename in tmp/raw-data-download/*; do 
	forqlift-0.9.0/bin/forqlift extract --file="$filename" --dir=tmp/decoded-tweets/ #decode data
	python elastic-search/json-aggregator.py "tmp/decoded-tweets/*" "tmp/es-json/" # aggregate data
	python elastic-search/elaticsearch-bulk.py "http://ec2-52-89-166-197.us-west-2.compute.amazonaws.com:9200" "tmp/es-json/*" #puts into ES

	aws s3 --region us-west-2 mv s3://mark-wang-test/dummy/$(basename $filename) s3://mark-wang-test/destination/$(basename $filename) 

	rm "$filename" # delete raw file
	mkdir empty_dir # hack to delete everything in tmp/decoded-tweets
	rsync -a --delete empty_dir/    tmp/decoded-tweets
	rm -rf empty_dir
    done
fi
rm -rf tmp/





