__author__ = 'aishwaryamathuria'
import math
from collections import deque

f = open("input_scan.txt")
epsilon = float(f.readline())
pop_thresh = int(f.readline())
label = [0,0,0,0,0,0,0,0,0,0,0,0,0,0]
cluster = [0,0,0,0,0,0,0,0,0,0,0,0,0,0]
nonmembers =[]
vertices = []
hub = []
outlier = []
G = []

for i in range(0,14):
    G.append([])
    adj = []
    adj = f.readline().split(" ")
    for j in range(0,len(adj)):
        G[i].append(int(adj[j]))
    vertices.append(i)


def neighbours(u):
    neighbours_u = []
    for i in range(0,len(G[u])):
        if G[u][i] == 1:
            neighbours_u.append(i)

    neighbours_u.insert(0,u)
    return neighbours_u

def similarity(u,v):
     u_matrix = set(neighbours(u))
     v_matrix = set(neighbours(v))
     common = set.intersection(*[u_matrix,v_matrix])
     sim = len(common)/math.sqrt(len(u_matrix)*len(v_matrix))
     return sim


def epsilon_neighbours(u):
    neighbours_u = neighbours(u)
    eps_neighbours = []
    for i in range(0,len(neighbours_u)):
        if similarity(u,neighbours_u[i]) >= epsilon:
            eps_neighbours.append(neighbours_u[i])

    return eps_neighbours


def isCore(u):
    u_eps = epsilon_neighbours(u)
    if len(u_eps) >= pop_thresh:
        return True
    else:
        return False


def SCAN():
    cluster_id = 0
    for u in vertices:
        if label[u]==0:
            if isCore(u)==True:
                cluster_id += 1
                q = epsilon_neighbours(u)
                while len(q) > 0:
                    w = q.pop(0)
                    if not isCore(w):
                        continue
                    R = epsilon_neighbours(w)
                    for s in R:
                        if label[s] is not None or label[s] == "nonmember":
                            cluster[s] = cluster_id
                            label[s] = "labeled"
                        if label[s] is None:
                            cluster[s] = cluster_id
                            label[s] = "labeled"
                            q.append(s)
            else:
                label[u] = "nonmember"
                nonmembers.append(u)

    for v in nonmembers:
        neighbours_v = neighbours(v)
        neighbours_v.remove(v)
        for x in neighbours_v:
            for y in neighbours_v:
                if cluster[x] != cluster[y]:
                    hub.append(v)
                    break
        if v not in hub:
            outlier.append(v)



SCAN()
print(label)
print(cluster)

for i in range(0,14):
    print(i)
    print("Cluster id",cluster[i])

print("HUB: ",set(hub))
print("OUTLIER: ",set(outlier))

