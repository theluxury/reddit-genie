from pyspark import SparkContext, SQLContext
import sys
import ast
from cassandra.cluster import Cluster

def add_up_unique(dict1, dict2):
    for key, value in dict1.iteritems():
        if not key in dict2:
            dict2[key] = value
        else:
            dict2[key] += value
    return dict2

def insert_into_cassandra(partition):         
   if partition:
       cluster = Cluster(['52.89.166.197', '52.89.166.250', '52.89.167.189', '52.89.167.219'])
       session = cluster.connect('reddit')
       for item in partition:
           preparedStmt = session.prepare("INSERT INTO users_graph (username, subreddit) VALUES (?, ?)")
           boundStmt = preparedStmt.bind([item[0], item[1]]) #username then subreddit
           session.execute(boundStmt)
       session.shutdown()
       cluster.shutdown()
    
mainRedditPageId = 't5_6' # going to filter this since we're doing subreddit graphs. 
logFile = 's3n://reddit-comments/2007/RC_2007-11'
# TODO: Maybe put overwrite here? Meh, probably shouldn't.
outputDirectory = 's3n://mark-wang-test/reddit-graph/results'
sc = SparkContext('spark://ip-172-31-2-13:7077', "Reddit Network Graph App")
sqlContext = SQLContext(sc)
df = sqlContext.read.json(logFile)
subRedditRDD = df.filter(df['subreddit_id'] != mainRedditPageId)
follows = subRedditRDD.map(lambda json: (json.author, {json.subreddit: 1}))
followsList = follows.reduceByKey(lambda a,b: add_up_unique(a, b)) 
followsList.foreachPartition(insert_into_cassandra)

sc.stop()
