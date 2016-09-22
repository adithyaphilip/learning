import sys

sys.setrecursionlimit(100010)
def store_sum(root):
    if len(adj[root]) == 0:
        return val[root]
    csum = sum([store_sum(i) for i in adj[root]])
    val[root] += csum
    return val[root]

def get_min_diff():
        return min(map(lambda x: abs(x-val[0]/2), val))*2

n = int(input())
adj = [[] for i in range(n)]
val = list(map(int, input().split()))
has_p = [False]*n
has_p[0] = True
in_l = [tuple(map(lambda x: int(x)-1, input().split())) for _ in range(n-1)]

a_l = [set() for i in range(n)]
p_l = [None]*n

for a,b in in_l:
    a_l[a].add(b)
    a_l[b].add(a)

def resolve(a_l, root):
    q = [root]
    while len(q) != 0:
        root = q.pop()
        for node in a_l[root]:
            p_l[node] = root
            a_l[node].remove(root)
            q.append(node)

resolve(a_l, 0)
adj = a_l
store_sum(0)
print(int(get_min_diff()))
