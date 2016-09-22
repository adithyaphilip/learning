def solve(s):
    for i in range(len(s) - 1):
        d = abs(ord(s[i]) - ord(s[i + 1]))
        if d != 1 and d != 25:
            return False

    return True


def main():
    for _ in range(int(input())):
        print("YES" if solve(input()) else "NO")


main()
