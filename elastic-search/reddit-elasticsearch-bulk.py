import os
import sys
import glob
from elasticsearch import Elasticsearch
import json
import logging
import shutil

hosts=["ec2-52-35-132-98.us-west-2.compute.amazonaws.com", "ec2-52-34-176-185.us-west-2.compute.amazonaws.com", "ec2-52-89-115-101.us-west-2.compute.amazonaws.com", "ec2-52-88-254-51.us-west-2.compute.amazonaws.com", "ec2-52-88-247-22.us-west-2.compute.amazonaws.com", "ec2-52-89-166-197.us-west-2.compute.amazonaws.com"]
path=sys.argv[1]
logsFilePath = os.path.dirname(os.path.abspath(__file__)) + '/logs/'
if not os.path.exists(logsFilePath):
    os.makedirs(logsFilePath)
logging.basicConfig(filename=logsFilePath + 'reddit-elasticsearch-bulk.log',level=logging.DEBUG)
es = Elasticsearch(
    hosts,
    port=9201,
    sniff_on_start=True,    # sniff before doing anything
    sniff_on_connection_fail=True,    # refresh nodes after a node fails to respond
    sniffer_timeout=60, # and also every 60 seconds
    timeout=30
)
i = 0
for filename in glob.glob(path):
    with open(filename) as file:
        i += 1
        try:
            es.bulk(body=file.read())
            logging.debug("Sucessfully finished writing {0}".format(filename))
            print "uploaded json file number " + str(i)
            os.remove(filename) # rm if finished uploading
        except Exception as e:
            print "could not write file: {0} with error: {1}".format(filename, str(e))
# shutil.move(filename, 'logs/' + os.path.basename(filename)) #if error, want to store log somewhere to see source of error.
            logging.error("could not write file: {0} with error: {1}".format(filename, str(e)))
