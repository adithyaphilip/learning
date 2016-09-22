def op(case, msg):
    print("Case #%d: %s" % (case, str(msg)))

def opp(c):
    return '+' if c == '-' else '-'

def get_steps(e, c, l):
    if e == -1:
        return 0
    if l[e] == c:
        return get_steps(e-1, c, l)
    else:
        return 1 + get_steps(e-1, opp(c), l)

def main():
    t = int(input())
    for case in range(1, t+1):
        l = input()
        op(case, get_steps(len(l)-1, '+', l))

main()
