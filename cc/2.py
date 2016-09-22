# cook your dish here
import fractions

def lcm(a,b):
    return int(a*b/fractions.gcd(a,b))

n = int(input())
for _ in range(n):
    t = int(input())
    a = int(input())
    b = int(input())
    a1 = int(t/(a -1))
    b1 = int(t/(b -1))
    l = lcm(a1,b1)
    print(a + b - t/l -1)
