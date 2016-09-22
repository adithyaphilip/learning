import sys

sys.setrecursionlimit(10 ** 6)


# returns the index of first element after streak
def streak(l, first, start):
    i = start
    while i < len(l) and l[i] > first:
        first = l[i]
        i += 1
    return i


def eat(l, start, limit):
    if start == len(l):
        return start
    if limit == 1:
        return streak(l, l[start], start + 1)
    si = start
    nsi = eat(l, si, limit - 1)
    while nsi < len(l) and l[si] < l[nsi]:
        si = nsi
        nsi = eat(l, si, limit - 1)
    return nsi


def solve(l, start=0):
    min_sf = start
    m_time = 0
    i = start + 1
    while i < len(l):  # change to min_sf
        if l[min_sf] >= l[i]:
            min_sf = i
            i += 1
            continue
        time = 1
        i = streak(l, l[min_sf], min_sf + 1)
        while i < len(l):
            si = i
            nsi = eat(l, si, time)
            while nsi < len(l) and l[si] < l[nsi]:
                si = nsi
                nsi = eat(l, si, time)
            time += 1
            if nsi == len(l):
                i = nsi
            elif l[nsi] <= l[min_sf]:
                min_sf = nsi
                i = min_sf + 1
                break
            else:
                i = nsi

        m_time = max(m_time, time)

    return m_time


def main():
    n = int(input())
    l = list(map(int, input().split()))
    print(solve(l))


main()
