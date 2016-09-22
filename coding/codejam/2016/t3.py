import sys

def get_num(s):
    num = []
    for i in range(2, 11):
        sumi = 0
        for d in s:
            sumi*=i
            sumi+=1 if d == '1' else 0
        num.append(sumi)
    return num

input()

for _ in range(50):
    mline = input().split()
    line = mline[0]
    dl = mline[1:]
    if (len(dl)!=9): 
        print(line)
        continue
    if line[0] != '1' or line[-1] != '1': 
        print(line)
        continue
    f = False
    for i in line:
        if i != '1' and i != '0': 
            print(line)
            f = True
            break
    if f: continue
    num = get_num(line)
    for i in range(len(dl)):
        if num[i] % int(dl[i]) != 0:
            print(line, i, num[i], dl[i])
        

