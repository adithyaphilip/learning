import sys

dp = []
steps = []
cross = []
n = 0
def least(lane, shop):
    al = steps[lane][shop]
    olane = 0 if lane == 1 else 1
    if shop == n-1: return al
#    print(lane, shop)
    if dp[lane][shop] != -1: return dp[lane][shop]
    cost =  al + min(least(lane, shop+1), cross[lane][shop] + least(olane, shop+1))
    dp[lane][shop] = cost
    return cost
def buildDp():
    for shop in reversed(range(n)):
        for lane in range(2):
            if(shop == n-1):
                dp[lane][shop] = steps[lane][shop]
                continue
            olane = 1 if lane == 0 else 0
            al = steps[lane][shop]
            dp[lane][shop] = al + min(dp[lane][shop+1], cross[lane][shop]
                    + dp[olane][shop + 1])

n = int(input().strip())
dp = [[-1]*n for _ in range(2)]

for j in range(2):
    steps.append([])
    for i in map(int, input().strip().split()):
        steps[j].append(i)

for j in range(2):
    cross.append([])
    for i in map(int, input().strip().split()):
        cross[j].append(i)
buildDp()
print(min(dp[0][0], dp[1][0]))

