def get_duplicates(a, pos):
    ctr = 1
    lpos = pos - 1
    while lpos >= 0 and a[lpos] == a[pos]:
        ctr += 1
        lpos -= 1
    rpos = pos + 1
    while rpos < len(a) and a[rpos] == a[pos]:
        ctr += 1
        rpos += 1
    return ctr


def binary_search(a, x):
    beg = 0
    end = len(a) - 1
    while beg <= end:
        mid = (beg + end) // 2
        if x > a[mid]:
            beg = mid + 1
        elif x < a[mid]:
            end = mid - 1
        else:
            return get_duplicates(a, mid)
    return 0


def solve(a, b, c, d, k, dp):
    s = 0
    d.sort()
    for i in set(d):
        dp[i] = binary_search(d, i)

    for n1 in a:
        for n2 in b:
            for n3 in c:
                n = k ^ n1 ^ n2 ^ n3
                if n in dp:
                    s += dp[n]
    return s


def main():
    for i in range(int(input())):
        n, k = map(int, input().split())
        a, b, c, d = [list(map(int, input().split())) for _ in range(4)]
        dp = {}
        print("Case #%d:" % (i + 1), solve(a, b, c, d, k, dp))


main()
