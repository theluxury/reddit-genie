from pyspark import SparkContext
import sys

logFile = 's3n://mark-wang-test/twitter_rv.net'
# TODO: Maybe put overwrite here? Meh, probably shouldn't. 
outputDirectory = 's3n://mark-wang-test/twitter-graph/results'
sc = SparkContext('spark://ip-172-31-2-13:7077', "Network Graph App")
# sc = SparkContext('local', "Network Graph App")
logData = sc.textFile(logFile)

res1 = logData.map(lambda line: (line.split('\t')[1], [line.split('\t')[0]]))
res2 = res1.reduceByKey(lambda a, b: a+b)
res3 = res2.saveAsTextFile(outputDirectory)
sc.stop()

