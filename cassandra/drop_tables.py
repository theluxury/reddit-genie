from cassandra.cluster import Cluster
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + '/config/')
from instances import CASSANDRA_CLUSTER_IP_LIST

def main():
    cluster = Cluster(CASSANDRA_CLUSTER_IP_LIST)
    session = cluster.connect()

    session.execute("CREATE KEYSPACE IF NOT EXISTS reddit WITH replication = {"
                    + " 'class': 'SimpleStrategy', "
                    + " 'replication_factor': '3' "
                    + "};" );
    session.execute("use reddit")

    session.execute("DROP TABLE IF EXISTS subreddits_graph;")
    session.execute("DROP TABLE IF EXISTS users_graph;")
    session.execute("DROP TABLE IF EXISTS comments;")
    session.shutdown()

if __name__ == '__main__':
    main()
