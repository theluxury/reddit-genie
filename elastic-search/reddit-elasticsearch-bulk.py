import os
from os import environ
import sys
import glob
from elasticsearch import Elasticsearch
import json
import logging
import shutil
import boto
from boto.s3.connection import S3Connection

def download_files():
    prefixes = ["reddit-es-comments-json/2007_10", "reddit-es-comments-json/2008_01", "reddit-es-comments-json/2008_12"]
    tmp_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + '/tmp/')
    conn = S3Connection(environ['AWS_ACCESS_KEY_ID'], environ['AWS_SECRET_ACCESS_KEY'])
    bucket = conn.get_bucket('mark-wang-test')
    for prefix in prefixes:
        for key in bucket.list(prefix=prefix):
            if key.name.split('-')[-2][-4:] == 'part': # filter folder and _SUCCESS files
                # make directory if it doesnt exist
                year_month = key.name.split('/')[-2]
                file_name = key.name.split('/')[-1]
                if not os.path.exists("{0}/{1}".format(tmp_dir, year_month)):
                    os.system('mkdir -p {0}/{1}'.format(tmp_dir, year_month))
                # should do check here to see if file exists or not yet
                print full_file_path
                if not os.path.exists(full_file_path):
                    key.get_contents_to_filename(full_file_path)
    return tmp_dir

hosts=["ec2-52-35-132-98.us-west-2.compute.amazonaws.com", "ec2-52-34-176-185.us-west-2.compute.amazonaws.com", "ec2-52-89-115-101.us-west-2.compute.amazonaws.com", "ec2-52-88-254-51.us-west-2.compute.amazonaws.com", "ec2-52-88-247-22.us-west-2.compute.amazonaws.com", "ec2-52-89-166-197.us-west-2.compute.amazonaws.com"]
logsFilePath = os.path.dirname(os.path.abspath(__file__)) + '/logs/'
if not os.path.exists(logsFilePath):
    os.makedirs(logsFilePath)
logging.basicConfig(filename=logsFilePath + 'reddit-elasticsearch-bulk.log',level=logging.DEBUG)
es = Elasticsearch(
    hosts,
    port=9200,
    sniff_on_start=True,    # sniff before doing anything
    sniff_on_connection_fail=True,    # refresh nodes after a node fails to respond
    sniffer_timeout=60, # and also every 60 seconds
    timeout=30
)

def main():
    s3_reddit_prefix = 'reddit-es-comments-json'
    tmp_dir = download_files()
    for dirname in os.walk(tmp_dir):
        if dirname[0] == tmp_dir: # walk returns a tuple. first element is string of sub directory. 
            continue
        for filename in glob.glob(dirname[0] + '/*'):
            with open(filename) as file:
                try:
                    es.bulk(body=file.read())
                    logging.debug("Sucessfully finished writing {0}".format(filename))
                    relative_path = '/'.join([filename.split('/')[-2], filename.split('/')[-1]])
                    print "uploaded json file {0}".format(relative_path)
                    # first move file in s3
                    os.system('aws s3 --region us-west-2 mv s3://mark-wang-test/{0}/{1} s3://mark-wang-test/reddit-finished/{1}'.format(s3_reddit_prefix, relative_path))
                    print "moved file"
                    # then remove from local
                    os.remove(filename)
                    print "deleted from local"
                except Exception as e:
                    print "could not write file: {0} with error: {1}".format(filename, str(e))
                    logging.error("could not write file: {0} with error: {1}".format(filename, str(e)))

if __name__ == '__main__':
    main()
