chunks_d = {}


def max_chunks(n, m):
    if n not in chunks_d:
        sum_c = (n ** 2) % m
        for i in range(n - 2, 0, -1):
            sum_c += (max_chunks(i, m) ** 2) % m
            sum_c %= m

    return chunks_d[n]


def main():
    pass


main()
