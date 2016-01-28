from cassandra.cluster import Cluster

cluster = Cluster(['52.88.244.205', '52.35.233.194', '52.34.55.16', '52.89.167.189', '52.88.247.22', '52.89.166.197'])
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
session.shutdown()
