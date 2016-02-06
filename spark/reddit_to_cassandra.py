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
from nltk import word_tokenize

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
        cluster = Cluster(['52.88.244.205', '52.35.233.194', '52.34.55.16', '52.89.167.189']) #, '52.88.247.22', '52.89.166.197'])
        session = cluster.connect('reddit')
        prepared_stmt = session.prepare("INSERT INTO {0} ({1}, {2}, {3}, {4}, {5}, {6}, {7}, {8}, {9}, {10}) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)".format(GRAPH_NAME, COLUMN_ONE, COLUMN_TWO, COLUMN_THREE, COLUMN_FOUR, COLUMN_FIVE, COLUMN_SIX, COLUMN_SEVEN, COLUMN_EIGHT, COLUMN_NINE, COLUMN_TEN))
        batch = BatchStatement(consistency_level=ConsistencyLevel.ONE)
        for item in partition:
            bound_stmt = prepared_stmt.bind([item[0], item[1], int(item[2]) * 1000, item[3], item[4], item[5], item[6], item[7], item[8], item[9]])
            session.execute(bound_stmt)
        session.shutdown()
        cluster.shutdown()

           
 #          boundStmt = preparedStmt.bind([item[0], item[1][0], item[1][1]]) #username then subreddit
#           session.execute(boundStmt)

def word_frequency(text):
    word_list = get_filtered_string_list(text)
    word_dict = {}
    for word in word_list:
        count = word_dict.get(word, 0) + 1
        word_dict[word] = count
    return word_dict
    
    
sc = SparkContext('spark://ip-172-31-2-10:7077', "Reddit Subreddits Graph App")
sqlContext = SQLContext(sc)
# mainRedditPageId = 't5_6' # going to filter this since we're doing subreddit graphs. 

conn = S3Connection(environ['AWS_ACCESS_KEY_ID'], environ['AWS_SECRET_ACCESS_KEY'])
bucket = conn.get_bucket('reddit-comments')
for key in bucket.list():
    if '-' not in key.name.encode('utf-8'):
        continue
    print key.name.encode('utf-8')
    logFile = 's3n://reddit-comments/' + key.name.encode('utf-8')
    year = logFile.split('-')[1][-4:] 
    month = logFile.split('-')[2]
    if int(year) < 2013 or (int(year) == 2013 and int(month) <6):
        continue
    df = sqlContext.read.json(logFile)
    users_rdd = df.filter(df['author'] != '[deleted]') #df['subreddit_id'] != mainRedditPageId and df['author'] != '[deleted]')
    users_row = users_rdd.map(lambda json: (json.author, '{0}_{1}'.format(year, month), json.created_utc, json.subreddit, json.id, word_frequency(json.body), json.body, json.score, json.ups, json.controversiality))
    users_row.foreachPartition(insert_into_cassandra)

sc.stop()
