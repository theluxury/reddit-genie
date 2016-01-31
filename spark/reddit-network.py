from pyspark import SparkContext, SQLContext
import sys
import ast
from cassandra.cluster import Cluster
from boto.s3.connection import S3Connection
from os import environ

GRAPH_NAME = sys.argv[1]
if GRAPH_NAME == 'subreddits_graph':
    PRIMARY_KEY = 'subreddit'
    PARTITION_KEY = 'year_month'
    DICTIONARY = 'users'
#elif GRAPH_NAME == 'users_graph':
 #   PRIMARY_KEY = 'user'
  #  PARTITION_KEY = 'year_month'
   # DICTIONARY = 'subreddits'


def add_up_unique(dict1, dict2):
    for key, value in dict1.iteritems():
        if not key in dict2:
            dict2[key] = value
        else:
            dict2[key] += value
    return dict2

def insert_into_cassandra(partition):         
   if partition:
       cluster = Cluster(['52.88.244.205', '52.35.233.194', '52.34.55.16', '52.89.167.189', '52.88.247.22', '52.89.166.197'])
       session = cluster.connect('reddit')
       for item in partition:
           preparedStmt = session.prepare("INSERT INTO {0} ({1}, {2}, {3}) VALUES (?, ?, ?)".format(GRAPH_NAME, PRIMARY_KEY, PARTITION_KEY, DICTIONARY))
           boundStmt = preparedStmt.bind([item[0], item[1][0], item[1][1]]) #username then subreddit
           session.execute(boundStmt)
       session.shutdown()
       cluster.shutdown()
    
sc = SparkContext('spark://ip-172-31-2-10:7077', "Reddit Subreddits Graph App")
sqlContext = SQLContext(sc)
mainRedditPageId = 't5_6' # going to filter this since we're doing subreddit graphs. 

conn = S3Connection(environ['AWS_ACCESS_KEY_ID'], environ['AWS_SECRET_ACCESS_KEY'])
bucket = conn.get_bucket('reddit-comments')
for key in bucket.list():
    if '-' not in key.name.encode('utf-8'):
        continue
    print key.name.encode('utf-8')
    logFile = 's3n://reddit-comments/' + key.name.encode('utf-8')
    year = logFile.split('-')[1][-4:] 
    if int(year) < 2012:
        continue
    month = logFile.split('-')[2]
    df = sqlContext.read.json(logFile)
    subRedditRDD = df.filter(df['subreddit_id'] != mainRedditPageId)
    follows = subRedditRDD.map(lambda json: (json.subreddit, ('{0}_{1}'.format(year, month), {json.author: 1})))
    followsList = follows.reduceByKey(lambda a,b: (a[0], add_up_unique(a[1], b[1]))) 
    followsList.foreachPartition(insert_into_cassandra)

sc.stop()


