import tkinter 
root = tkinter.Tk()
root.geometry("400x400+100+100") # 100 and 100 are offsets from x and y
root.configure(background="blue")
root.title("Lol")

label = tkinter.Label(root, text="Enter")
label.place(x=50, y=50)

tkinter.mainloop()

