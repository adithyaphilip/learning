p,q = map(int, input().split())
pl = [1 for _ in range(p)]
queries = [list(map(int, input().split())) for _ in range(q)]

nl = []
for i in queries:
    nl.append({"s":i[0], "n":i[2]})
    nl.append({"e":i[1], "n":i[2]})

nl = sorted(nl, key = lambda x: x["e"] if "e" in x else (x["s"] - 0.1))
#print(nl)

ps = None
pe = None
cm = 1
fq = []
for i in nl:
    if "s" in i:
        if ps is None:
            ps = i
            cm = i["n"]
            continue
        if i["s"] == ps["s"]:
            cm*=i["n"]
        else:
            nr = [ps["s"], i["s"] - 1, cm]
            fq.append(nr)
            ps = i
            cm*=i["n"]
    else:
        if pe is None or pe["e"] != i["e"] :
            fq.append([ps["s"], i["e"], cm])
            ps = {"s":i["e"] +1}
        cm //= i["n"]
        pe = i

#print(fq)

for i in fq:
    for j in range(i[0], i[1]+1):
        pl[j] = i[2]

#print(pl)

def palindrome(l):
    n = len(l)
    for i in range(n//2):
        if l[i] != l[n - 1 - i]:
            return False
    return True

print(palindrome(pl))

