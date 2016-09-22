def solve(h, n):
    l = [0] * (2 ** (h + 1))
    n += 2 ** h - 1
    limit = 2 ** h - 1
    left = False
    i = 1
    rooms = 0
    fails = 0
    while True:
        left = not left
        if fails == 2:
            fails = 0
            i //= 2
        if left:
            if l[2 * i] == 0:
                fails = 0
                l[2 * i] = 1
                rooms += 1
                ni = 2 * i
                if ni > limit:
                    # leaf
                    if ni == n:
                        return rooms
                else:
                    i = ni
            else:
                fails += 1
        else:
            if l[2 * i + 1] == 0:
                fails = 0
                l[2 * i + 1] = 1
                rooms += 1
                ni = 2 * i + 1
                if ni > limit:
                    if ni == n:
                        return rooms
                else:
                    i = ni
            else:
                fails += 1


def main():
    t = int(input())
    for i in range(t):
        print(solve(*map(int, input().split())))


main()
