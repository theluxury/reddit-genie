from pyspark import SparkContext, SQLContext
import sys
import ast
from cassandra.cluster import Cluster
from boto.s3.connection import S3Connection
from os import environ

# GRAPH_NAME = sys.argv[1]
GRAPH_NAME = 'subreddits_graph'
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

def main():
    sc = SparkContext('spark://ip-172-31-2-10:7077', "Reddit Subreddits Graph App {0} {1}".format(sys.argv[1], sys.argv[2]))
    sqlContext = SQLContext(sc)
    mainRedditPageId = 't5_6' # going to filter this since we're doing subreddit graphs. 

    conn = S3Connection(environ['AWS_ACCESS_KEY_ID'], environ['AWS_SECRET_ACCESS_KEY'])
    bucket = conn.get_bucket('reddit-comments')
    for key in bucket.list():
        if '-' not in key.name.encode('utf-8'):
            continue
        logFile = 's3n://reddit-comments/' + key.name.encode('utf-8')
        year = logFile.split('-')[1][-4:] 
        month = logFile.split('-')[2]
        year_month = '{0}_{1}'.format(year, month)
        if year_month != sys.argv[1]:
            continue
        outputDirectory = 's3n://mark-wang-test/subreddit-graph/{0}'.format(year_month)
        df = sqlContext.read.json(logFile)
        subRedditRDD = df.filter(df['subreddit_id'] != mainRedditPageId)
        follows = subRedditRDD.map(lambda json: (json.subreddit, (year_month, {json.author: 1})))
        followsList = follows.reduceByKey(lambda a,b: (a[0], add_up_unique(a[1], b[1]))) 
        if sys.argv[2] == 's3':
            followsList.saveAsTextFile(outputDirectory)
        elif sys.argv[2] == 'cassandra':
            followsList.foreachPartition(insert_into_cassandra)

    sc.stop()


if __name__ == '__main__':
    main()
