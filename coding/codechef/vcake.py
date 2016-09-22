def solve(r, c, areas):
    if sum(areas) != r * c:
        return False
    if len(areas) == 1: return True
    for a in areas:
        if a % r == 0:
            a2 = areas.copy()
            a2.remove(a)
            if solve(r, c - a // r, a2): return True
        if a % c == 0:
            a2 = areas.copy()
            a2.remove(a)
            if solve(r - a // c, c, a2): return True

    return False


def main():
    for _ in range(int(input())):
        r, c, m, k, j = map(int, input().split())
        print("Yes" if solve(r, c, [m, k, j]) else "No")


main()
