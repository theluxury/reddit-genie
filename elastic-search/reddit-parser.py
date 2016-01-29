import sys
import os
import logging
import json

fileName=sys.argv[1]
logsFilePath = os.path.dirname(os.path.abspath(__file__)) + '/logs/'
if not os.path.exists(logsFilePath):
    os.makedirs(logsFilePath)
logging.basicConfig(filename=logsFilePath + 'reddit-parser-errors.log',level=logging.ERROR)
i = 0
outputFileName = sys.argv[2] + str(i)

with open(fileName) as file:
    for line in file:
        try:
            commentJson = json.loads(line)
            if commentJson['author'] == '[deleted]' or commentJson['body'] == '[deleted]':
                continue
            # what fields do I need? username, year_month, subreddit, and body.
            esCommentJson = {}
            esCommentJson['username'] = commentJson['author']
            year_month = fileName.split('_')[-1]
            esCommentJson['year_month'] = '{0}_{1}'.format(year_month.split('-')[0], year_month.split('-')[1]) # save filename intelligently
            esCommentJson['subreddit'] = commentJson['subreddit']
            esCommentJson['text'] = commentJson['body']
            actionJson = {'index': {'_index': 'reddit', '_type': 'comment', '_id': commentJson['id']}}                    
            with open(outputFileName, 'a+') as elasticSearchActionFile:
                json.dump(actionJson, elasticSearchActionFile)
                elasticSearchActionFile.write('\n')
                json.dump(esCommentJson, elasticSearchActionFile)
                elasticSearchActionFile.write('\n')
                if os.stat(outputFileName).st_size > 10485760: # roughly 10 MB
                    print "aggregate json file number " + str(i)
                    i += 1
                    outputFileName = sys.argv[2] + str(i)
        except Exception as e:
#                shutil.move(filename, "logs/" + os.path.basename(filename))
            logging.error("could not write file: " + fileName + " with error: " + str(e))
