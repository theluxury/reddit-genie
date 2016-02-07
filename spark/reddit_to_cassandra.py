from pyspark import SparkContext, SQLContext
import sys
import ast
from cassandra.cluster import Cluster
from cassandra.query import BatchStatement
from cassandra import ConsistencyLevel
from boto.s3.connection import S3Connection
import os
from os import environ
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + '/config/')
from constants import FILTER_SET
from aws import AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, RAW_JSON_REDDIT_BUCKET
from instances import CASSANDRA_CLUSTER_IP_LIST
from spark_constants import SPARK_ADDRESS
from nltk import word_tokenize

KEY_SPACE = 'reddit'
GRAPH_NAME = 'comments'
COLUMN_ONE = 'author'
COLUMN_TWO = 'year_month'
COLUMN_THREE = 'created_utc'
COLUMN_FOUR = 'subreddit'
COLUMN_FIVE = 'id'
COLUMN_SIX = 'word_count'
COLUMN_SEVEN = 'body'
COLUMN_EIGHT = 'score'
COLUMN_NINE = 'ups'
COLUMN_TEN = 'controversiality'

def get_filtered_string_list(original_string):
    tokenized_list = word_tokenize(original_string.lower())
    filtered_tokenized_list = [word for word in tokenized_list if word not in FILTER_SET]
    return filtered_tokenized_list

def insert_into_cassandra(partition):         
    if partition:
        cluster = Cluster(CASSANDRA_CLUSTER_IP_LIST)
        session = cluster.connect(KEY_SPACE)
        prepared_stmt = session.prepare("INSERT INTO {0} ({1}, {2}, {3}, {4}, {5}, {6}, {7}, {8}, {9}, {10}) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)".format(GRAPH_NAME, COLUMN_ONE, COLUMN_TWO, COLUMN_THREE, COLUMN_FOUR, COLUMN_FIVE, COLUMN_SIX, COLUMN_SEVEN, COLUMN_EIGHT, COLUMN_NINE, COLUMN_TEN))
        batch = BatchStatement(consistency_level=ConsistencyLevel.ONE)
        for item in partition:
            bound_stmt = prepared_stmt.bind([item[0], item[1], int(item[2]) * 1000, item[3], item[4], item[5], item[6], item[7], item[8], item[9]])
            session.execute(bound_stmt)
        session.shutdown()
        cluster.shutdown()

def word_frequency(text):
    word_list = get_filtered_string_list(text)
    word_dict = {}
    for word in word_list:
        count = word_dict.get(word, 0) + 1
        word_dict[word] = count
    return word_dict
    

def main():    
    sc = SparkContext(SPARK_ADDRESS, "Reddit Subreddits Graph App")
    sqlContext = SQLContext(sc)

    conn = S3Connection(AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY)
    bucket = conn.get_bucket(RAW_JSON_REDDIT_BUCKET)
    for key in bucket.list():
        if '-' not in key.name.encode('utf-8'): # filter out folders and _SUCCESS
            continue
        logFile = 's3n://{0}/{1}'.format(RAW_JSON_REDDIT_BUCKET, key.name.encode('utf-8'))
        year = logFile.split('-')[1][-4:] 
        month = logFile.split('-')[2]
        if int(year) < 2013 or (int(year) == 2013 and int(month) <6):
            continue
        df = sqlContext.read.json(logFile)
        users_rdd = df.filter(df['author'] != '[deleted]') 
        users_row = users_rdd.map(lambda json: (json.author, '{0}_{1}'.format(year, month), json.created_utc, json.subreddit, json.id, word_frequency(json.body), json.body, json.score, json.ups, json.controversiality))
        users_row.foreachPartition(insert_into_cassandra)
    sc.stop()

if __name__ == '__main__':
    main()
