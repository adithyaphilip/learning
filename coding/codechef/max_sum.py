import sys

sys.setrecursionlimit(1000000)

a = []
brdp = []


def best_run(i):
    if i == len(a):
        return 0
    orig_i = i
    tot = 0
    neg = 0
    if brdp[i] == -1:
        while i < len(a) and a[i] >= 0:
            tot += a[i]
            i += 1
        while i < len(a) and a[i] < 0:
            neg -= a[i]
            i += 1
        brn = best_run(i)
        if brn > neg:
            brdp[orig_i] = tot - neg + brn
        else:
            brdp[orig_i] = tot

    return brdp[orig_i]


def solve(i):
    if i == len(a):
        return 0
    bsum = 0
    mostneg = 0
    rsum = 0
    while i < len(a):
        while i < len(a) and a[i] >= 0:
            rsum += a[i]
            i += 1
        bsum = max(bsum, rsum - mostneg)
        while i < len(a) and a[i] < 0:
            mostneg = min(mostneg, a[i])
            rsum += a[i]
            i += 1
        asum = 0
        if rsum <= 0 < rsum - mostneg:
            asum = max(rsum - mostneg + best_run(i), solve(i))
            break
        elif rsum <= 0:
            # reset run
            asum = solve(i)
            break

    bsum = max(asum, bsum)
    return bsum


def main():
    global a
    global brdp
    for _ in range(int(input())):
        input()
        a = list(map(int, input().split()))
        brdp = [-1] * len(a)
        max_a = max(a)
        print(max_a if max_a < 0 else solve(0))


main()
