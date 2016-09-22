def get_sorted_ranges(n, l1, r1, a, b, c1, c2, m):
    xp = l1
    yp = r1
    ranges = [(0, 0, xp), (0, 1, yp)]
    for i in range(n - 1):
        xn = (a * xp + b * yp + c1) % m
        yn = (a * yp + b * xp + c2) % m
        ranges.append((i + 1, 0, min(xn, yn)))
        ranges.append((i + 1, 1, max(xn, yn)))
        xp = xn
        yp = yn
    ranges.sort(key=lambda x: (x[2], x[1]))
    return ranges


def coverage(ranges):
    prev_open = ranges[0][2]
    tot_coverage = 0
    tot_open = 1
    for item in ranges[1:]:
        if item[1] == 0:
            if tot_open == 0:
                prev_open = item[2]
            tot_open += 1
        else:
            if tot_open == 1:
                tot_coverage += item[2] - prev_open + 1
            tot_open -= 1
    return tot_coverage


def solve(n, l1, r1, a, b, c1, c2, m):
    ranges = get_sorted_ranges(n, l1, r1, a, b, c1, c2, m)
    # print(ranges)
    tot_coverage = coverage(ranges)
    # print("Cov", tot_coverage)
    prev_ind = ranges[0][2]
    tot_open = 1
    open_set = {ranges[0][0]}
    max_rem = {}
    for item in ranges[1:]:
        if tot_open == -1:
            raise Exception("tot_open is -1!")
        if item[1] == 0:
            if tot_open == 0:
                prev_ind = item[2]
            elif tot_open == 1:
                max_rem[list(open_set)[0]] = max_rem.get(list(open_set)[0], 0) + item[2] - prev_ind  # TODO
            open_set.add(item[0])
            tot_open += 1
        else:
            if tot_open == 1:
                max_rem[list(open_set)[0]] = max_rem.get(list(open_set)[0], 0) + item[2] - prev_ind + 1
            open_set.remove(item[0])
            tot_open -= 1
            prev_ind = item[2] + 1
    # print(max_rem)
    return tot_coverage - max_rem[max(max_rem, key=lambda x: max_rem[x])]


def main():
    for _ in range(int(input())):
        print("Case #%d: %d" % (_+1, solve(*map(int, input().split()))))


main()
