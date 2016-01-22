import os
import sys
import glob
import json
import logging

path=sys.argv[1]
logging.basicConfig(filename='logs/json-errors.log',level=logging.ERROR)
outputFileName = sys.argv[2] + str(i)
i = 0
for filename in glob.glob(path):
    with open(filename) as file:
        for line in file:
            try:
                tweetJson = json.loads(line)
                actionJson = {'index': {'_index': 'twitter', '_type': 'tweet', '_id': tweetJson['id']}}                    
                with open(sys.argv[2]+str(i), 'a+') as elasticSearchActionFile:
                    json.dump(actionJson, elasticSearchActionFile)
                    elasticSearchActionFile.write('\n')
                    json.dump(tweetJson, elasticSearchActionFile)
                    elasticSearchActionFile.write('\n')
                    if os.stat(outputFilename).st_size > 10485760: # roughly 10 MB
                        i += 1
                        outputFileName = sys.argv[2] + str(i)
            except Exception as e:
               logging.error("could not write file: " + filename + " with error: " + e


