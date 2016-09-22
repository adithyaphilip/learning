import functools

MOD = 10 ** 9 + 7
INF = 10 ** 9 + 7


def solve(k, a):
    a.sort()
    neg = 0
    pos = -1
    prod = 1

    neg_num = functools.reduce(lambda x, y: x + 1 if y < 0 else x, a, 0)

    if k == len(a):
        return functools.reduce(lambda x, y: (x * (y % MOD)) % MOD, a, 1)

    if neg_num == 0:
        return functools.reduce(lambda x, y: (x * (y % MOD)) % MOD, a[-1:-k - 1:-1], 1)

    if neg_num == len(a):
        if k % 2 == 0:
            return functools.reduce(lambda x, y: (x * (y % MOD)) % MOD, a[:k], 1)
        else:
            return functools.reduce(lambda x, y: (x * (y % MOD)) % MOD, a[-1: -k - 1: -1], 1)

    i = 1
    while i <= k:
        if abs(a[neg]) >= a[pos] and a[pos] != 0:
            if neg_num - neg >= 2 and i + 1 <=k:
                nprod = a[neg] * a[neg+1]
                pprod = a[pos] * a[pos-1]
                prod *= abs(a[neg])
                prod %= MOD
                neg += 2
                i += 2
        elif a[pos] > 0:
            prod *= a[pos]
            prod %= MOD
            pos -= 1
            i += 1
        elif a[pos] == 0:
            # we are here if
            # there are no more negative numbers and all remaining positive numbers are 0
            return 0
        else:
            # we have run out of positive numbers
            pass


def main():
    for _ in range(int(input())):
        n, k = map(int, input().split())
        a = list(map(int, input().split()))
        print(solve(k, a))


main()
