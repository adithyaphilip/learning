A = [[(x ** x * y ** y * i * j, x, i, y, j) for i in range(1, 2 * x) for j in range(1, 2 * y)] for x in range(1, 8) for
     y in range(1, 8)]
A2 = []
for x in A:
    for y in x:
        if y[0] <= 100000:
            A2.append(y)

A3 = []
for x in A2:
    A3.append((x[0], x[1], x[2], 0, 0))
    for y in A2:
        A3.append((x[0] * y[0], x[1], x[2], y[1], y[2]))

A3.sort()

A = A3
ctr = len(A)


def bsearch(n, val):
    beg = 0
    end = n - 1
    mid = -1
    while (beg <= end):
        mid = (beg + end) >> 1
        if (A[mid][0] < val):
            beg = mid + 1
        elif (A[mid][0] > val):
            end = mid - 1
        else:
            for i in range(mid, end + 1):
                if (A[mid][0] == A[i][0]):
                    mid += 1
            break
    return mid if A[mid][0] <= val else mid - 1


for n in range(1, 100000):

    count = 0
    l = []
    ans = []
    while (n > 1):
        val, x, k1, y, k2 = A[bsearch(ctr, n)]
        # print(val, x, k1, y, k2, n)
        # DUDE PLEASE TRY TO UNDERSTAND AND FINISH
        # this means x**x*k1 * y**y*k2
        l.append((x, x, k1, y, y, k2))  # MODIFY TRY TO GROUP
        n -= val
    if (n == 1):
        l.append((0, 0, 1, 0, 0, 0))  # MODIFY

    length = max(l, key=lambda x: x[1])[1] + 1  # MODIFY

    # print(l)
    # MODIFY ENTIRE LOOP
    # TRY MAKING EXAMPLES AND TESTING FOR THEM
    for i, j, k, a, b, c in l:
        temp = []
        for jj in range(j):
            for ii in range(i):
                temp.append(count + i * (jj + 1) - ii)
        count += i * j

        for ii in range(k):
            temp.append(count + k - ii)

        count += k

        for ii in range(length - j - 1)[::-1]:
            temp.append(count + ii)

        count += a * b + c

        ans.extend(temp)
    if (count > 100):
        print(count)
        # print(l)
        # print(count, ' '.join([str(x) for x in ans]), sep='\n')
