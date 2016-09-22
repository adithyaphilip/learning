def main():
    for _ in range(int(input())):
        n = int(input())
        a = 0
        for i in range(n):
            a %= 26
            print(chr(97 + a), end="")
            a += 1
        print()

main()
