import re
with open("num") as f:
    for i in [line.strip() for line in f]:
        p = re.compile(r"[a-zA-Z]+\s\d{2,3}-\d{8}\s\w+@\w+\.\w+$")
        p2 = re.compile(r"^[a-zA-Z]+(?=\s)")
        mat = p.match(i)
        if not mat:
            print(p2.match(i).group())
        else:
            print(mat, len(i))
        
