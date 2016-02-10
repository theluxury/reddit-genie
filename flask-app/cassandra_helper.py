from cassandra.cluster import Cluster
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + '/config/')
from instances import CASSANDRA_CLUSTER_IP_LIST
from heapq import heappush, heappop, heappushpop

class CassandraHelper():
    def __init__(self):
        KEYSPACE = 'reddit'
        TABLE = 'comments'
        cluster = Cluster(CASSANDRA_CLUSTER_IP_LIST)
        self.session = cluster.connect(KEYSPACE)
        self.prepared_stmt = self.session.prepare("select body from {0} where (author = ?) and (year_month = ?) and (created_utc = ?) and (subreddit = ?) and (id = ?)".format(TABLE))

    def get_highest_ranked_comments(self, filtered_comments_list, year_month):
        top_comments = []
        for comment in filtered_comments_list:
            bound_stmt = self.prepared_stmt.bind([comment['author'], year_month, comment['created_utc'], comment['subreddit'], comment['id']])
            row = self.session.execute(bound_stmt)
            top_comments.append(row[0].body)

#        print top_comments

    def close_session(self):
        self.session.close()
