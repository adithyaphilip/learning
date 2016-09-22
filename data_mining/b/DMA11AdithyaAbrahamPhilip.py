import sys

# reads epsilon, popularity threshold, and adjacency list from i/p file
def get_adj_list():
    if len(sys.argv) < 2:
        print("Error: path to input file must be first command line argument")
        sys.exit(1)
    adj_l = []
    with open(sys.argv[1]) as f:
        try:
            f.readline()  # discard comment
            eps = float(f.readline().strip())
            pop = int(f.readline().strip())

            lines = f.readlines()
            n = len(lines)

            for line in lines:
                adj_l.append(set(map(int, line.strip().split())))
                for i in adj_l[-1]:
                    if i >= n:
                        raise Exception()

        except Exception:
            print("Error: Invalid input format")
            sys.exit(2)
    return adj_l, eps, pop


def get_epsilon_neighbourhood(node, adj, eps):
    # every node is its own neighbour, as long as eps <= 1
    en = [node]
    # for each connected node
    for cn in adj[node]:
        if get_sim(cn, node, adj) >= eps:
            en.append(cn)
    return en


def get_sim(n1, n2, adj):
    num = len((adj[n1] | {n1}) & (adj[n2] | {n2}))
    # print(num)
    den = ((1 + len(adj[n1])) * (1 + len(adj[n2]))) ** 0.5
    # print(den)
    return num / den


def main():
    cluster(*get_adj_list())
#    adj,eps,pop = get_adj_list()
#    print(get_epsilon_neighbourhood(6, adj, eps))


def cluster(adj, eps, pop):
    cluster_ctr = 0
    cluster = [-1] * len(adj)
    for node in range(len(adj)):
        if cluster[node] != -1:
            # already labelled
            continue
        # if node not yet labelled
        en = get_epsilon_neighbourhood(node, adj, eps)
        if len(en) >= pop:
            # if node is a core vertex
            cluster_ctr += 1
            cluster[node] = cluster_ctr
            for w in en:
                r = get_epsilon_neighbourhood(w, adj, eps)
                if len(r) < pop:
                    # not a core
                    r = []

                for s in r:
                    cluster[s] = cluster_ctr
                    if cluster[s] == -1:
                        en.append(s)

    hubs = []
    outliers = []

    for i in range(len(cluster)):
        if cluster[i] == -1:
            # the unique clusters its neighbours belong to
            diff_clusters = set()
            for node in adj[i]:
                if cluster[node] != -1:
                    diff_clusters.add(cluster[node])
            if len(diff_clusters) > 1:
                hubs.append(i)
            else:
                outliers.append(i)

    print("Number of clusters:", cluster_ctr)
    for i in range(1, cluster_ctr + 1):
        members = [node for node in range(len(adj)) if cluster[node] == i]
        print("Cluster #%d (Size %d):" % (i, len(members)), members)

    print("Hubs:", hubs)
    print("Outliers:", outliers)

main()
