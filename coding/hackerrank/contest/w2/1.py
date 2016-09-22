def solve(n, x,y):
    a = min(x,y)
    b = max(x,y)
    d = b-a 
    if a == b:
        print((n-1)*a)
    else:
        print(*[(n-1)*a + d*i for i in range(n)])

for _ in range(int(input())):
    solve(int(input()), int(input()), int(input()))
