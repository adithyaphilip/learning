def op(s, n):
    print("Case #%d:" % (n+1), s)

def diff(a,b):
    return abs(int("".join(a)) - int("".join(b)))

def solve_d(h,l):
    return list("".join(h).replace("?", "0")), list("".join(l).replace("?", "9"))

def solve(c, j):
    if len(c) == 0: return [], []
#    print(c,j)
    s = ""
    if c[0] == "?" and j[0] == "?":
        x1, x2 = solve_d(c[1:],j[1:])
        y2, y1 = solve_d(j[1:],c[1:])
        z1, z2 = solve(c[1:], j[1:])
        
        x1.insert(0, "1")
        x2.insert(0, "0")
        y1.insert(0, "0")
        y2.insert(0, "1")
        z1.insert(0, "0")
        z2.insert(0, "0")

        x = diff(x1, x2)
        y = diff(y1, y2)
        z = diff(z1, z2)

        if z <= y and z<=x:
            return z1, z2
        if y <= x:
            return y1, y2
        return x1, x2

    elif c[0] == "?" or j[0] == "?":
        if c[0] == "?":
            coders = True
            c1, c2 = c, j
        else:
            coders = False
            c2, c1 = c, j

        high = False
        if c2[0] != "9":
            x1,x2 = solve_d(c1[1:], c2[1:])
            high = True
        
        case = False

        if c2[0]!="0":
            case = True
            y2,y1 = solve_d(c2[1:], c1[1:])

        z1,z2 = solve(c1[1:],c2[1:])

        z1.insert(0, c2[0])
        z2.insert(0, c2[0])
        
        z = diff(z1, z2)
        
        if high:
            x1.insert(0, str(int(c2[0])+1))
            x2.insert(0, c2[0])
            
            x = diff(x1, x2)
        if case:
            y1.insert(0, str(int(c2[0])-1))
            y2.insert(0, c2[0])
            
            y = diff(y1, y2)
        
        if case and y <= z and (not high or y <= x):
            c1, c2 = y1, y2
        elif not high or z<=x:
            c1, c2 = z1, z2
        else:
            c1, c2 = x1, x2

        if coders:
            return c1, c2
        else:
            return c2,c1
    elif c[0] == j[0]:
        c1,c2 = solve(c[1:], j[1:])
        c1.insert(0, c[0])
        c2.insert(0, j[0])
        return c1, c2
    elif c[0] > j[0]:
        c1,c2 = solve_d(c[1:], j[1:])
        c1.insert(0, c[0])
        c2.insert(0, j[0])
        return c1, c2
    else:
        c2,c1 = solve_d(j[1:], c[1:])
        c1.insert(0, c[0])
        c2.insert(0, j[0])
        return c1, c2

def main():
    for _ in range(int(input())):
        c, j = input().split(" ")
        op(" ".join(map("".join, solve(list(c),list(j)))), _)

main()
