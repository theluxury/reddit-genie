import sys
import glob
from elasticsearch import Elasticsearch
import json
import logging
import shutil

host=sys.argv[1]
path=sys.argv[2]
logging.basicConfig(filename='logs/es-errors.log',level=logging.ERROR)
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
        print i
        i += 1
        try:
            es.bulk(body=file.read())
            os.rm(filename) # rm if finished uploading
        except Exception as e:
            shutil.move(filename, 'logs/' + filename) #if error, want to store log somewhere to see source of error. 
            logging.error("could not write file: " + filename + " with error: " + e 
