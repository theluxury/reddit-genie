import os
import sys
import glob
from elasticsearch import Elasticsearch
import json
import logging
import shutil

host=sys.argv[1]
path=sys.argv[2]
logsFilePath = os.path.dirname(os.path.abspath(__file__)) + '/logs/'
if not os.path.exists(logsFilePath):
    os.makedirs(logsFilePath)
logging.basicConfig(filename=logsFilePath + 'reddit-elasticsearch-bulk.log',level=logging.DEBUG)
es = Elasticsearch(
    [host],
    sniff_on_start=True,    # sniff before doing anything
    sniff_on_connection_fail=True,    # refresh nodes after a node fails to respond
    sniffer_timeout=60, # and also every 60 seconds
    timeout=30
)
i = 0
for filename in glob.glob(path):
    with open(filename) as file:
        i += 1
        print "uploaded json file number " + str(i)
        try:
            es.bulk(body=file.read())
            logging.debug("Sucessfully finished writing {0}".format(filename);
       #     os.remove(filename) # rm if finished uploading
        except Exception as e:
            print 'meh'
# shutil.move(filename, 'logs/' + os.path.basename(filename)) #if error, want to store log somewhere to see source of error.
            logging.error("could not write file: " + filename + " with error: " + str(e))
