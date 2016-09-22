import tkinter as tk
ctr = 0
def click():
    global ctr
    ctr+=1
    if (ctr==1):
        tv.set("1 click")
        l1["font"]="Times 20 bold"
    else:
        tv.set("%d clicks" % ctr)
    if (ctr%2==0):
        l1["bg"]="#FF00FF"
    else:
        l1["bg"] ="#00FF00"
root = tk.Tk()
root.geometry("250x200+100+100")
b1 = tk.Button(bg="#FF0000", text="Click me", command = click)
tv = tk.StringVar()
l1 = tk.Entry(bg = "#0000FF", textvariable=tv)

b2 = tk.Button(text="Exit",command = root.quit)
b1.pack()
l1.pack()
b2.pack()

tk.mainloop()
