import sys
import os
import logging
import json
from nltk import word_tokenize
from constants import FILTER_SET

file_name=sys.argv[1]
logs_file_path = os.path.dirname(os.path.abspath(__file__)) + '/logs/'
if not os.path.exists(logs_file_path):
    os.makedirs(logs_file_path)
logging.basicConfig(filename=logs_file_path + 'reddit-parser-errors.log',level=logging.ERROR)
i = 0
output_file_name = sys.argv[2] + str(i)

def get_filtered_string(original_string):
    tokenized_list = word_tokenize(original_string.lower())
    filtered_tokenized_list = [word for word in tokenized_list if word not in FILTER_SET]
    return ' '.join(filtered_tokenized_list)

with open(file_name) as file:
    for line in file:
        try:
            comment_json = json.loads(line)
            # remove pointless deleted comments.
            if comment_json['author'] == '[deleted]' or comment_json['body'] == '[deleted]':
                continue
            # The fields I eventually want in elasticsearch are username, year_month, subreddit for easy searching
            # Score and timestamp for possible eventual queries that filter by either
            # The most interesting field is text, except that I strip out stop words and conjunctions.
            # Thsi is because for my primary use case (making word clouds based on subreddits), these are filtered
            # out anyways. This winds up sparing a lot of space. Full comments are stored in cassandra. 
            es_comment_json = {}
            es_comment_json['author'] = comment_json['author']
            year_month = file_name.split('_')[-1]
            # save filename intelligently
            es_comment_json['year_month'] = '{0}_{1}'.format(year_month.split('-')[0], year_month.split('-')[1]) 
            es_comment_json['subreddit'] = comment_json['subreddit']
            es_comment_json['score'] = comment_json['score']
            es_comment_json['created_utc'] = long(comment_json['created_utc'])
            es_comment_json['filtered_body'] = get_filtered_string(comment_json['body'])
            actionJson = {'index': {'_index': 'reddit_filtered', '_type': 'comment', '_id': comment_json['id']}}                   
            with open(output_file_name, 'a+') as elastic_search_action_file:
                json.dump(actionJson, elastic_search_action_file)
                elastic_search_action_file.write('\n')
                json.dump(es_comment_json, elastic_search_action_file)
                elastic_search_action_file.write('\n')
                if os.stat(output_file_name).st_size > 10485760: # roughly 10 MB
                    print "aggregate json file number " + str(i)
                    i += 1
                    output_file_name = sys.argv[2] + str(i)
        except Exception as e:
            logging.error("could not write file: " + file_name + " with error: " + str(e))

