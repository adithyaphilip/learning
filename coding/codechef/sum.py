k = 0

def cost_kill(i, l):
    return cost_resolve(i + 1, l) + l[i][0] * l[i][1]


def cost_reduce(i, l):
    tot = 0
    for j in range(len(l),i,-1):
        if l[j][0] - l[i][0] <= k: break
        tot+=l[j][1]*(l[j][0]-l[i][0])


def cost_resolve(i, l):
    if i == len(l):
        return 0
    return min(cost_kill(i, l), cost_reduce(i, l))


def get_list(w):
    l = [0] * 26
    for c in w:
        l[ord(c)] += 1
    d = {}
    for i in l:
        if i > 0:
            d[i] = d.get(i, 0) + 1

    l = list(sorted(d.items(), key=lambda x: x[0]))
    return l


def main():
    for _ in range(int(input())):
        input()
        global k
        w, k = input().split()
        k = int(k)

        l = get_list(w)
        print(l)


main()
