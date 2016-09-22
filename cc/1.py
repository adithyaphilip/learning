t = int(input().strip())
for _ in range(t):
    l = int(input().strip())
    xn = int(input().strip())
    x = list(filter(lambda x: x <= l, map(int, input().strip().split())))
    yn = int(input().strip())
    y = list(filter(lambda x: x <= l, map(int, input().strip().split())))

    if len(y)<2 or len(x)<2: print(0)
    else: print((len(y)-1)*(len(x)-1))

