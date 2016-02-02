import json
from elasticsearch import Elasticsearch

hosts=["ec2-52-35-132-98.us-west-2.compute.amazonaws.com", "ec2-52-34-176-185.us-west-2.compute.amazonaws.com", "ec2-52-89-115-101.us-west-2.compute.amazonaws.com", "ec2-52-88-254-51.us-west-2.compute.amazonaws.com", "ec2-52-88-247-22.us-west-2.compute.amazonaws.com", "ec2-52-89-166-197.us-west-2.compute.amazonaws.com"]
es = Elasticsearch(
    hosts,
    port=9201,
    sniff_on_start=True,    # sniff before doing anything
    sniff_on_connection_fail=True,    # refresh nodes after a node fails to respond
    sniffer_timeout=60, # and also every 60 seconds
    timeout=30
)

def elastic_search_mapper(df, year_month):
    action_json = {'index': {'_index': 'reddit_filtered_{0}'.format(year_month), '_type': 'comment', '_id': df.id}}
    es_comment_json = {}
    es_comment_json['author'] = df.author
    es_comment_json['subreddit'] = df.subreddit
    es_comment_json['score'] = df.score
    es_comment_json['created_utc'] = long(df.created_utc)
    es_comment_json['filtered_body'] = get_filtered_string(df.body)
    final_string = '\n'.join([json.dumps(action_json), json.dumps(es_comment_json)])
    return final_string

def put_to_elasticsearch(partition):
    if partition:
        json_string = ''
        for item in partition:
            if not json_string:
                json_string = item
            else:
                json_string = '\n'.join([json_string, item])
        json_string = '\n'.join([json_string, ''])  #need last empty line.
        es.bulk(body=json_string)
