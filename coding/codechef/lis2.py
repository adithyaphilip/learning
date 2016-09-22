import math


def solve(n):
    l = []
    s = 1

    while n != 1:
        b = n % 2
        l.append(b)
        b //= 2


def main():
    print(solve(11))


main()
