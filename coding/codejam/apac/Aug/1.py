def main():
    for _ in range(int(input())):
        n = min(map(int, input().split()))
        print("Case #%d: %d" % (_+1, n*(n+1)//2))

main()