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
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + '/config/')
from instances import ES_CLUSTER_PUBLIC_DNS_LIST
from aws import REGION, AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, MY_BUCKET, MY_BUCKET_S3_REDDIT_PREFIX

def download_files():
    prefixes = ["reddit-es-comments-json/2014_01", "reddit-es-comments-json/2014_12"]
    tmp_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + '/tmp/')
    conn = S3Connection(AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY)
    bucket = conn.get_bucket(MY_BUCKET)
    for prefix in prefixes:
        for key in bucket.list(prefix=prefix):
            if key.name.split('-')[-2][-4:] == 'part': # filter folder and _SUCCESS files
                # make directory if it doesnt exist
                year_month = key.name.split('/')[-2]
                file_name = key.name.split('/')[-1]
                if not os.path.exists("{0}/{1}".format(tmp_dir, year_month)):
                    os.system('mkdir -p {0}/{1}'.format(tmp_dir, year_month))
                # should do check here to see if file exists or not yet
                full_file_path = '{0}/{1}/{2}'.format(tmp_dir, year_month, file_name)
                if not os.path.exists(full_file_path):
                    key.get_contents_to_filename(full_file_path)
    return tmp_dir

def init_es():
    hosts=ES_CLUSTER_PUBLIC_DNS_LIST
    logs_file_path = os.path.dirname(os.path.abspath(__file__)) + '/logs/'
    if not os.path.exists(logs_file_path):
        os.makedirs(logs_file_path)
    logging.basicConfig(filename=logs_file_path + 'reddit-elasticsearch-bulk.log',level=logging.DEBUG)
    es = Elasticsearch(
        hosts,
        port=9200,
        sniff_on_start=True,    # sniff before doing anything
        sniff_on_connection_fail=True,    # refresh nodes after a node fails to respond
        sniffer_timeout=60, # and also every 60 seconds
        timeout=30
        )
    return es

def main():
    es = init_es()
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
                    original_path = 's3://{0}/{1}/{2}'.format(MY_BUCKET, MY_BUCKET_S3_REDDIT_PREFIX, relative_path)
                    new_path = 's3://{0}/{1}/{2}'.format(MY_BUCKET, MY_BUCKET_S3_FINISHED_PREFIX, relative_path)
                    # first move file in s3
                    os.system('aws s3 --region {0} mv {1} {2}'.format(REGION, original_path, new_path)
                    print "moved file {0}".format(relative_path)
                    # then remove from local
                    os.remove(filename)
                    print "deleted from local {0}".format(relative_path)
                except Exception as e:
                    print "could not write file: {0} with error: {1}".format(filename, str(e))
                    logging.error("could not write file: {0} with error: {1}".format(filename, str(e)))

if __name__ == '__main__':
    main()
