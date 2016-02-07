from cassandra.cluster import Cluster
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + '/config/')
from instance import CASSANDRA_CLUSTER_IP_LIST

def main():
    cluster = Cluster(CASSANDRA_CLUSTER_IP_LIST)
    session = cluster.connect()


    session.execute("CREATE KEYSPACE IF NOT EXISTS reddit WITH replication = {"
                    + " 'class': 'SimpleStrategy', "
                    + " 'replication_factor': '3' "
                    + "};" );
    session.execute("use reddit")

    session.execute("CREATE TABLE IF NOT EXISTS subreddits_graph ( "
                    + " subreddit text,"
                    + " year_month text,"
                    + " users map<text, int>,"
                    + " PRIMARY KEY (subreddit, year_month));")

    session.execute("CREATE TABLE IF NOT EXISTS users_graph ( "
                    + " username text," 
                    + " year_month text,"
                    + " subreddits map<text, int>," 
                    + " PRIMARY KEY (username, year_month));")
    
    session.execute("CREATE TABLE IF NOT EXISTS comments ( "
                    + "author text,"
                    + "year_month text,"
                    + "created_utc timestamp,"
                    + "subreddit text,"
                    + "id text,"
                    + "word_count map<text, int>,"
                    + "body text,"
                    + "score int,"
                    + "ups int,"
                    + "controversiality int,"
                    + "PRIMARY KEY ((author, year_month), created_utc, subreddit, id));")
    
    session.shutdown()

if __name__ == '__main__':
    main()
