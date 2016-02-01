from pyspark import SparkContext, SQLContext
import sys
import ast
from nltk import word_tokenize
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + '/config/')
from constants import FILTER_SET
from cassandra.cluster import Cluster
from boto.s3.connection import S3Connection
from os import environ
import json

SPARK_ADDRESS = sys.argv[1]
APP_NAME = "Reddit JSON Parser App"

def elastic_search_mapper(df):
    final_string = ""
    action_json = {'index': {'_index': 'reddit_filtered', '_type': 'comment', '_id': df.id}}  
    final_string += json.dumps(action_json)
    final_string +='\n'
    es_comment_json = {}
    es_comment_json['author'] = df.author
    es_comment_json['subreddit'] = df.subreddit
    es_comment_json['score'] = df.score
    es_comment_json['created_utc'] = long(df.created_utc)
    es_comment_json['filtered_body'] = get_filtered_string(df.body)
    final_string += json.dumps(es_comment_json)
    return final_string

def get_filtered_string(original_string):
    tokenized_list = word_tokenize(original_string.lower())
    filtered_tokenized_list = [word for word in tokenized_list if word not in FILTER_SET]
    return ' '.join(filtered_tokenized_list)
    
sc = SparkContext(SPARK_ADDRESS, "Reddit JSON Parser App")
sqlContext = SQLContext(sc)

conn = S3Connection(environ['AWS_ACCESS_KEY_ID'], environ['AWS_SECRET_ACCESS_KEY'])
reddit_bucket = conn.get_bucket('reddit-comments')
my_bucket = conn.get_bucket('mark-wang-test')
for key in reddit_bucket.list():
    if '-' not in key.name.encode('utf-8'):
        continue
    logFile = 's3n://reddit-comments/' + key.name.encode('utf-8')
    year = logFile.split('-')[1][-4:] 
    month = logFile.split('-')[2]
    year_month = '{0}_{1}'.format(year, month)
    if int(year) == 2007: # already did first year
        continue
    df = sqlContext.read.json(logFile)
    filtered_df = df.filter(df.author != '[deleted]')
    final_string = filtered_df.map(lambda line: elastic_search_mapper(line))
    outputDirectory = 's3n://mark-wang-test/reddit-es-comments-json/{0}/'.format(year_month)
    # delete files if it already exists.
    for my_key in my_bucket.list(prefix='reddit-es-comments-json/{0}'.format(year_month)):
        my_key.delete()
    final_string.saveAsTextFile(outputDirectory)

sc.stop()
