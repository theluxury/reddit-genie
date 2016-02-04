from elasticsearch import Elasticsearch

class ESHelper():   
    def __init__(self):
        hosts=["ec2-52-35-132-98.us-west-2.compute.amazonaws.com", "ec2-52-34-176-185.us-west-2.compute.amazonaws.com", "ec2-52-89-115-101.us-west-2.compute.amazonaws.com", "ec2-52-88-254-51.us-west-2.compute.amazonaws.com", "ec2-52-88-247-22.us-west-2.compute.amazonaws.com", "ec2-52-89-166-197.us-west-2.compute.amazonaws.com"]

        self.es = Elasticsearch(
            hosts,
            port=9200,
            sniff_on_start=True,    # sniff before doing anything
            sniff_on_connection_fail=True,    # refresh nodes after a node fails to respond
            sniffer_timeout=60, # and also every 60 seconds
            timeout=30
            )

    def search(self, subreddit, topic, year_month):
        response = self.es.search(index='reddit_filtered_{0}'.format(year_month), body={
                "size": 0,
                "query": {
                    "bool": {
                        "filter": [{ "match": { "subreddit": subreddit }}]
                        }
                    },
                "aggregations": {
                    "text": {
                        "terms": {
                            "field": "author",
                            "size": 1000
                            }
                        }
                    }
                })
        if response['timed_out'] == True:
            # TODO: handle this
            print 'ruhroh'
        return response

#         return reponse          
#     namesList = []
#     for jsonElement in response['aggregations']['text']['buckets']:
#         namesList.append(jsonElement['key'])
# 

