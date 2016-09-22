s = set()
while True:
    i = input()
    if i == "end": break
    val = i.replace("_","")
    if val in s: print(val)
    else: s.add(val)

