import random
import time
import sys

num_parts = 5
while True:
    parts = input().split(":")
    p = random.randint(0,9)
    if not p:
        print("Dropping packet!", file=sys.stderr)
        continue
    delay = random.randint(0,3)
    #delay = 1
    for i in range(num_parts):
        p = random.randint(0, 19)  # (0.95)**5 = 33% chance of error overall
        if not p:
            print("Introducing error in packet!", file=sys.stderr)
            parts[i] += "11111"

    time.sleep(delay)
    print(*parts, sep=":")
    print("Sending packet!", ":".join(parts), file=sys.stderr)