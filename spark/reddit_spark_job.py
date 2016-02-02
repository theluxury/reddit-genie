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
sys.path.insert(1, os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + '/elastic-search/')
from elastic_search_helper import elastic_search_mapper, put_to_elasticsearch


SPARK_ADDRESS = sys.argv[1]
APP_NAME = "Reddit JSON Parser App"

def get_filtered_string(original_string):
    tokenized_list = word_tokenize(original_string.lower())
    filtered_tokenized_list = [word for word in tokenized_list if word not in FILTER_SET]
    return ' '.join(filtered_tokenized_list)
    
sc = SparkContext(SPARK_ADDRESS, "Reddit JSON Parser App")
sql_context = SQLContext(sc)

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
    df = sql_context.read.json(logFile)
    filtered_df = df.filter(df.author != '[deleted]')
    final_rdd = filtered_df.map(lambda line: elastic_search_mapper(line, year_month))
    final_rdd.foreachPartition(put_to_elasticsearch)

sc.stop()
