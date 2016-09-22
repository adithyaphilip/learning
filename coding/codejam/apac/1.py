MOD = 10 ** 9 + 7


def solve(line):
    prod = 1
    for i in range(len(line) - 2):
        prod *= len(set(line[i:i + 3]))
        prod %= MOD
    prod *= len(set(line[:2]))
    prod %= MOD
    if len(line) > 1:
        prod *= len(set(line[-2:]))
        prod %= MOD

    return prod


def main():
    for _ in range(int(input())):
        print("Case #%d:" % (_ + 1), solve(input()))


main()
