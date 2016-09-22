def maxSubArraySum(a, size):
    # bwk
    max_so_far = 0
    max_ending_here = 0
    start = list(range(size))
    index = size - 1
    for i in range(size - 1, -1, -1):
        max_ending_here = max_ending_here + a[i]
        if max_ending_here < 0:
            max_ending_here = 0
        if (max_so_far < max_ending_here):
            max_so_far = max_ending_here  # 1 2 3 -1 4.
            index = i
        start[i] = max_so_far, index
    # fwd
    max_ending_here = 0
    prefix_sums = [0] * size
    x = list(range(size))
    for i in range(0, size):
        max_ending_here = max_ending_here + a[i]
        if max_ending_here < 0:
            max_ending_here = 0
        x[i] = max_ending_here
        prefix_sums[i] = prefix_sums[i - 1] + a[i]

    global_max = max(max_so_far, start[1][0])

    for i in range(1, size - 1):
        index = start[i + 1][1]
        curr = max(start[i + 1][0] + x[i - 1] + prefix_sums[index - 1] - prefix_sums[i], start[i + 1][0])
        if (curr > global_max):
            global_max = curr
    if (global_max == 0):
        return max(a)
    return global_max

a = [201, -1000, -2000, 200, -200, 4, -1003]
print(maxSubArraySum(a, len(a)))
