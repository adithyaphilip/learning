dp = {}


def get_sum(a, d, n):
    return 2 * a + (n - 1) * d


def bin_search(beg_a, end_a, beg_d, end_d, nc, n):
    mid_a = (beg_a + end_a) // 2
    mid_d = (beg_d + end_d) // 2

    if beg_a > end_a or beg_d > end_d:
        return False

    if mid_a in dp:
        if mid_d in dp[mid_a]:
            return dp[mid_a][mid_d]
    else:
        dp[mid_a] = {}

    if nc == get_sum(mid_a, mid_d, n):
        dp[mid_a][mid_d] = True
    elif nc > get_sum(mid_a, mid_d, n):
        dp[mid_a][mid_d] = bin_search(mid_a + 1, end_a, beg_d, end_d, nc, n) \
                           or bin_search(beg_a, end_a, mid_d + 1, end_d, nc, n)
    else:
        dp[mid_a][mid_d] = bin_search(beg_a, mid_a - 1, beg_d, end_d, nc, n) or bin_search(beg_a, end_a, beg_d,
                                                                                           mid_d // 2, nc, n)

    return dp[mid_a][mid_d]


def solve(n, c):
    if n == 1:
        return True
    if (2 * c) % n != 0:
        return False
    nc = (2 * c) // n
    max_a = (nc - (n - 1)) // 2
    max_d = (nc - 2) // (n - 1)

    return bin_search(1, max_a, 1, max_d, nc, n)


def main():
    for i in range(int(input())):
        n, c = map(int, input().split())
        print("Yes" if solve(n, c) else "No")


main()
