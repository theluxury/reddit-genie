import os
import sys
import glob
import json
import logging
import shutil

path=sys.argv[1]
if not os.path.exists('logs/'):
    os.makedirs('logs/')
logging.basicConfig(filename='logs/json-errors.log',level=logging.ERROR)
i = 0
outputFileName = sys.argv[2] + str(i)
for filename in glob.glob(path):
    with open(filename) as file:
        for line in file:
            try:
                tweetJson = json.loads(line)
                actionJson = {'index': {'_index': 'twitter', '_type': 'tweet', '_id': tweetJson['id']}}                    
                with open(outputFileName, 'a+') as elasticSearchActionFile:
                    json.dump(actionJson, elasticSearchActionFile)
                    elasticSearchActionFile.write('\n')
                    json.dump(tweetJson, elasticSearchActionFile)
                    elasticSearchActionFile.write('\n')
                    if os.stat(outputFileName).st_size > 10485760: # roughly 10 MB
                        print "aggregate json file number " + str(i)
                        i += 1
                        outputFileName = sys.argv[2] + str(i)
            except Exception as e:
#                shutil.move(filename, "logs/" + os.path.basename(filename))
                logging.error("could not write file: " + filename + " with error: " + str(e))
