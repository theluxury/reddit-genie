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

    def get_top_users(self, subreddit, year_month, num_users):
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
                            "size": num_users
                            }
                        }
                    }
                })
        if response['timed_out'] == True:
            return []
        else:
            names_list = []
            for json_element in response['aggregations']['text']['buckets']:
                names_list.append(json_element['key'])
            return names_list

    def get_top_words(self, topic, year_month, users, num_terms):
        response = self.es.search(index='reddit_filtered_{0}'.format(year_month), body={
                "size": 0,
                "query": {
                    "bool": {
                        "filter": [
                            { "match": {"filtered_body": topic}},
                            { "terms" : { "author": users }}
                            ]
                    }
                },
                "aggregations": {
                    "text": {
                        "terms": {
                            "field": "filtered_body",
                            "size": num_terms
                            }
                        }
                    }
                })
        if response['timed_out'] == True:
            return []
        else:
            words_list = []
            bad_words_set = {topic, 'm', 'people', 'think','going', 'something', 'guy', 'things'}
            for json_element in response['aggregations']['text']['buckets']:
                if json_element['key'] not in bad_words_set:
                    words_list.append({'text': json_element['key'], 'size': json_element['doc_count']})
            return words_list
