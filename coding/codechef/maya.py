n, k = map(int, input().split())
l = list(map(int, input().split()))
ma = l[0]
mi = l[0]
if n == 1:
    print("YES")
else:
    for num in l:
        ma = max(num, ma)
        mi = min(num, mi)

    print("YES" if abs(ma - mi) <= k else "NO")
