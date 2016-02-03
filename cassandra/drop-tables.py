from cassandra.cluster import Cluster

cluster = Cluster(['52.89.166.197', '52.89.166.250', '52.89.167.189', '52.89.167.219'])
session = cluster.connect()


session.execute("CREATE KEYSPACE IF NOT EXISTS reddit WITH replication = {"
  + " 'class': 'SimpleStrategy', "
  + " 'replication_factor': '3' "
  + "};" );
session.execute("use reddit")

session.execute("DROP TABLE IF EXISTS subreddits_graph;")
session.execute("DROP TABLE IF EXISTS users_graph;")
session.shutdown()
