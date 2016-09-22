import sys

sys.setrecursionlimit(1000000)
dp = {}
next_dup = {}


def it_solve(a):
    dp[len(a) - 1] = len(a) -1
    for i in range(len(a) - 2, -1, -1):
        dp[i] = min(dp[i + 1], next_dup.get(i, len(a)) - 1)

#
# def solve(start, a):
#     print(start)
#     if start not in dp:
#         if start == len(a) - 1:
#             pass
#             # dp[start] = start
#         else:
#             end_index = solve(start + 1, a)
#             # act_end = min(end_index, next_dup.get(start, len(a)) - 1)
#             # dp[start] = act_end
#
#     # return dp[start]
#     return 0


def populate_next_dup(b):
    global next_dup
    for i in range(len(b) - 1):
        if b[i][1] == b[i + 1][1]:
            next_dup[b[i][0]] = b[i + 1][0]


def main():
    for _ in range(int(input().strip())):
        global dp
        global next_dup
        dp = {}
        next_dup = {}
        input()
        a = list(map(int, input().strip().split()))
        b = list(sorted(enumerate(a), key=lambda x: x[1]))
        populate_next_dup(b)
        # solve(0, a)
        it_solve(a)
        # print(b, next_dup)

        score = 0
        for start, end in dp.items():
            l = end - start + 1
            score += l * (l + 1) // 2

        # print(dp)

        print(score)


main()
