from cassandra.cluster import Cluster

cluster = Cluster(['127.0.0.1'])
session = cluster.connect()


session.execute("CREATE KEYSPACE IF NOT EXISTS reddit WITH replication = {"
  + " 'class': 'SimpleStrategy', "
  + " 'replication_factor': '3' "
  + "};" );
session.execute("use reddit")

session.execute("DROP TABLE IF EXISTS subreddit_graph;")
session.execute("DROP TABLE IF EXISTS users_graph;")
session.shutdown()
