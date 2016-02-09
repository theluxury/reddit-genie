from cassandra.cluster import Cluster
from heapq import heappush, heappop

def main():
    cluster_ips = ['52.88.244.205', '52.35.233.194', '52.34.55.16', '52.89.167.189']
    keyspace = 'reddit'
    table = 'comments'
    some_values = ['dlmcleo1', '2013_10']
    cluster = Cluster(cluster_ips)
    session = cluster.connect(keyspace)
    prepared_stmt = session.prepare("select * from {0} where (author = ?) and (year_month = ?)".format(table))
    bound_stmt = prepared_stmt.bind(some_values)
    rows = session.execute(bound_stmt)

    score_queue = []
    # probably want, uh, a queue with score.
    for row in rows:
        heappush(score_queue, (-row.score, row.body))

    print heappop(score_queue)
    print heappop(score_queue)
if __name__ == '__main__':
    main()
