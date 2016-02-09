from pyspark import SparkContext, SQLContext
import sys
import ast
from nltk import word_tokenize
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + '/config/')
from constants import FILTER_SET
from spark_constants import SPARK_ADDRESS 
from aws import AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, RAW_JSON_REDDIT_BUCKET, MY_BUCKET, MY_BUCKET_S3_REDDIT_PREFIX
from cassandra.cluster import Cluster
from boto.s3.connection import S3Connection
from os import environ
import json
import logging
from elasticsearch import Elasticsearch
    
def elastic_search_mapper(df, year_month):
    action_json = {'index': {'_index': 'reddit_filtered_{0}'.format(year_month), '_type': 'comment', '_id': df.id}}  
    es_comment_json = {}
    es_comment_json['author'] = df.author
    es_comment_json['subreddit'] = df.subreddit
    es_comment_json['score'] = df.score
    es_comment_json['created_utc'] = long(df.created_utc)
    es_comment_json['filtered_body'] = get_filtered_string(df.body)
    final_string = '\n'.join([json.dumps(action_json), json.dumps(es_comment_json)])
    return final_string

def get_filtered_string(original_string):
    tokenized_list = word_tokenize(original_string.lower())
    filtered_tokenized_list = [word for word in tokenized_list if word not in FILTER_SET]
    return ' '.join(filtered_tokenized_list)

<<<<<<< HEAD
def main():
    sc = SparkContext(SPARK_ADDRESS, "Reddit JSON Parser App")
    sql_context = SQLContext(sc)
    conn = S3Connection(AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY)
    reddit_bucket_conn = conn.get_bucket(RAW_JSON_REDDIT_BUCKET)
    my_bucket = conn.get_bucket(MY_BUCKET)
    for key in reddit_bucket.list():
        if '-' not in key.name.encode('utf-8'): # filter out folders and _SUCCESS
            continue
        log_file = 's3n://{0}/{1}'.format(RAW_JSON_REDDIT_BUCKET, key.name.encode('utf-8'))
        year = log_file.split('-')[1][-4:]
        month = log_file.split('-')[2]
        if int(year) > 2011 or (int(year) == 2011 and int(month) > 7):
            continue
        year_month = '{0}_{1}'.format(year, month)
        df = sql_context.read.json(log_file)
        filtered_df = df.filter(df.author != '[deleted]') # get rid of the comments with deleted authors
        final_rdd = filtered_df.map(lambda line: elastic_search_mapper(line, year_month))
        output_directory = 's3n://{0}/{1}/{2}/'.format(MY_BUCKET, MY_BUCKET_S3_REDDIT_PREFIX, year_month)
        # delete stuff in there from before otherwise saveAsTextFile fails
        for my_key in my_bucket.list(prefix='{0}/{1}'.format(MY_BUCKET_S3_REDDIT_PREFIX, year_month)): 
            my_key.delete()
        final_rdd.saveAsTextFile(output_directory)
    sc.stop()
=======
conn = S3Connection(environ['AWS_ACCESS_KEY_ID'], environ['AWS_SECRET_ACCESS_KEY'])
reddit_bucket = conn.get_bucket('reddit-comments')
my_bucket = conn.get_bucket('mark-wang-test')
for key in reddit_bucket.list():
    if '-' not in key.name.encode('utf-8'):
        continue
    log_file = 's3n://reddit-comments/' + key.name.encode('utf-8')
    year = log_file.split('-')[1][-4:]
    month = log_file.split('-')[2]
    if int(year) < 2015 or (int(year) == 2015 and int(month) < 2):
        continue
    year_month = '{0}_{1}'.format(year, month)
    df = sql_context.read.json(log_file)
    filtered_df = df.filter(df.author != '[deleted]')
    final_rdd = filtered_df.map(lambda line: elastic_search_mapper(line, year_month))#.repartition(600)
    output_directory = 's3n://mark-wang-test/reddit-es-comments-json/{0}/'.format(year_month)
    for my_key in my_bucket.list(prefix='reddit-es-comments-json/{0}'.format(year_month)):
        my_key.delete()
    final_rdd.saveAsTextFile(output_directory)
    # final_rdd.foreachPartition(put_to_elasticsearch)
>>>>>>> master

if __name__ == '__main__':
    main()
