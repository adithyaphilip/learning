t = int(input())
def output(case, res):
    print("Case #%d: %s" % (case, str(res)))


def get_d(num):
    return set(map(int, list(str(num))))

for case in range(1, t+1):
    n = int(input())
    if n == 0:
        output(case, "INSOMNIA")
        continue
    digits = get_d(n)
    i = n
    while len(digits) != 10:
        i+=n
        digits |= get_d(i)

    output(case, i) 

