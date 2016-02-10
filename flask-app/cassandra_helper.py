from cassandra.cluster import Cluster
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + '/config/')
from instances import CASSANDRA_CLUSTER_IP_LIST
from heapq import heappush, heappop, heappushpop

class CassandraHelper():
    def connect_to_cassandra(self, column):
        KEYSPACE = 'reddit'
        TABLE = 'comments'
        self._cluster = Cluster(CASSANDRA_CLUSTER_IP_LIST)
        self._session = self._cluster.connect(KEYSPACE)
        self._prepared_stmt = self._session.prepare("select {1} from {0} where (author = ?) and (year_month = ?) and (created_utc = ?) and (subreddit = ?) and (id = ?)".format(TABLE, column))

    def get_highest_ranked_comments(self, filtered_comments_list, year_month):
        self.connect_to_cassandra('body')
        top_comments = []
        for comment in filtered_comments_list:
            bound_stmt = self._prepared_stmt.bind([comment['author'], year_month, comment['created_utc'], comment['subreddit'], comment['id']])
            row = self._session.execute(bound_stmt)
#            top_comments.append(row[0].word_count)

        self._cluster.shutdown()
        print top_comments

    def get_word_frequency_from_comments(self, filtered_comments_list, year_month):
        self.connect_to_cassandra('word_count')
        total_dict = {}
        for comment in filtered_comments_list:
            bound_stmt = self._prepared_stmt.bind([comment['author'], year_month, comment['created_utc'], comment['subreddit'], comment['id']])
            row = self._session.execute(bound_stmt)
            self.sum_word_frequency(total_dict, row[0].word_count)
        self._cluster.shutdown()
        sorted_dict = sorted(total_dict.items(), key=lambda (k, v): -v)
        print sorted_dict

    def sum_word_frequency(self, total_dict, row_dict):
        for k, v in row_dict.iteritems():
            count = total_dict.get(k, 0) + v
            total_dict[k] = count
