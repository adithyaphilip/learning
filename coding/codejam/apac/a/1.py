def main():
    for i in range(1, int(input()) + 1):
        n = int(input())
        maxl = 0
        maxname = ''
        for _ in range(n):
            name = input()
            l = len(set(name) - {' '})
            if l > maxl:
                maxl = l
                maxname = name
            elif l == maxl:
                maxname = min(name, maxname)
        print("Case #%d:" % i, maxname)

main()
