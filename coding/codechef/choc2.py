def solve(n, c):
    if n == 1:
        return True
    if (2 * c) % n != 0:
        return False
    return True


def main():
    for i in range(int(input())):
        n, c = map(int, input().split())
        print("Yes" if solve(n, c) else "No")


main()
