from pyspark import SparkContext, SQLContext
import sys

def add_up_unique(dict1, dict2):
    for key, value in dict1.iteritems():
        if not key in dict2:
            dict2[key] = value
        else:
            dict2[key] += value
    return dict2


mainRedditPageId = 't5_6' # going to filter this since we're doing subreddit graphs. 
logFile = 's3n://reddit-comments/2007/RC_2007-11'
# TODO: Maybe put overwrite here? Meh, probably shouldn't.
outputDirectory = 's3n://mark-wang-test/reddit-graph/results'
sc = SparkContext('spark://ip-172-31-2-13:7077', "Reddit Network Graph App")
sqlContext = SQLContext(sc)
df = sqlContext.read.json(logFile)
subRedditDf = df.filter(df['subreddit_id'] != mainRedditPageId)
follows = subRedditDf.map(lambda json: (json.author, {json.subreddit: 1}))
followsList = follows.reduceByKey(lambda a,b: add_up_unique(a, b)) 
followsList.saveAsTextFile(outputDirectory)


#res1 = logData.map(lambda line: (line.split('\t')[1], [line.split('\t')[0]]))
#res2 = res1.reduceByKey(lambda a, b: a+b)
#res3 = res2.saveAsTextFile(outputDirectory)
sc.stop()
