import sys
import math

def sieve(n):
    pd = []
    s = [True] * (n+1)
    for i in range(2, n+1):
        if s[i]:
            pd.append(i)
            for j in range(2*i, n+1, i):
                s[j] = False
    return pd


def is_jam(l):
    dl = []
    for i in l:
        div = False
        for j in range(2, int(math.sqrt(i+1))):
            if i % j == 0:
                dl.append(j)
                div = True
                break
        if not div:
            return None
    return dl

def get_num(s):
    s = s[::-1]
    num = []
    for i in range(2, 11):
        sumi = 0 
        for d in range(len(s)):
            sumi+=il[i-2][d] if s[d] == '1' else 0
        num.append(sumi)
    return num

n = 16
il = [[i**j for j in range(n)] for i in range(2,11)]
# print(il)

def get_c_num(b):
    b = b[::-1]
    for i in range(1, len(b)):
        if b[i]=='0':
            return i
            

def next_list(l):
    ind = get_c_num(bin(l[0])[2:])
    l[0]+=2
    for i in range(1,len(l)):
        l[i]-=sum(il[i][1:ind])
        l[i]+=il[i][ind]

def main():
    j = 50
    l = [0] * 9
    for i in range(2,11):
        l[i-2] = 1 + i**(n-1)

    fl = []
    while j > 0:
        dl = is_jam(l)
        if dl is not None:
            j-=1
            dl.insert(0, l[-1])
            fl.append(dl)
        l[0]+=2
        l = get_num(bin(l[0])[2:])

    print("Case #1:")
    for i in fl:
        print(*i)

main()
