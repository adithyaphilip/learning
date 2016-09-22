import tkinter as tk
root = tk.Tk()
res = tk.StringVar()
res.set("result")
r1 =  tk.Entry(textvariable=res)
e1 = tk.Entry()
e2 = tk.Entry()
e1.pack()
e2.pack()
op = tk.StringVar()
op.set("a")
l = [("add", "+"), ("sub", "-"), ("mul", "*"), ("div", "/")]
def calc():
    res.set(str(eval(e1.get()+op.get()+e2.get())))
for i in l:
    r = tk.Radiobutton(text=i[0], value=i[1], variable=op, command = calc)
    r.pack(side="top")
r1.pack()
tk.mainloop()
