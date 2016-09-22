import heapq

def op(s, n):
    print("Case #%d:" % (n+1), s)

def main():
    l = {"W":2, "X":6, "U":4, "S":7, "F":5, "Z":0, "O":1, "R":3, "H":8, "I":9}

    inv_map = {v: k for k, v in l.items()}

    order = ["W", "X", "U", "S", "F", "Z", "O", "R", "H", "I"]
    dep = {"W":"O", "X":"SI", "U":"FOR", "S":"", "F":"I", "Z":"RO", "O":"", "R":"H", "H":"I", "I":""}

    for _ in range(int(input())):
        sw = {a: 0 for a in order}
        ans = [0 for i in range(10)]
        s = input()
        for a in s:
            if a in sw:
                sw[a]+=1

        for a in order:
            for b in dep[a]:
                sw[b]-=sw[a]

        x = []
        for num in inv_map:
            x.extend([num]*sw[inv_map[num]])

        op("".join(map(str, x)), _)

main()

