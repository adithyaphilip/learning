from queue import Queue

def store_sum(root):
    s = []
    q = Queue()
    q.put(root)
    while q.qsize() != 0:
        a = q.get()
        for node in adj[a]:
            q.put(node)
        s.append(a)
    
    while len(s) != 0:
        a = s.pop()
        if p_l[a] is None: break
        val[p_l[a]] += val[a]

def get_min_diff():
#    print(val)
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
#print(p_l)
adj = a_l
store_sum(0)
print(int(get_min_diff()))
