from cassandra.cluster import Cluster

cluster = Cluster(['127.0.0.1'])
session = cluster.connect()


session.execute("CREATE KEYSPACE IF NOT EXISTS reddit WITH replication = {"
  + " 'class': 'SimpleStrategy', "
  + " 'replication_factor': '3' "
  + "};" );
session.execute("use reddit")

session.execute("CREATE TABLE IF NOT EXISTS subreddit_graph ( "
                + " subreddit text,"
                + " month-year text,"
                + " users map<text, int>,"
                + " PRIMARY KEY (subreddit, month-year));")

session.execute("CREATE TABLE IF NOT EXISTS users_graph ( "
                + " username text," 
                + " month-year text,"
                + " subreddits map<text, int>," 
                + " PRIMARY KEY (username, month-year));")
session.shutdown()
