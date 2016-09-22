from tkinter import *

top = Tk()
top.geometry("1000x1000+100+100")
button1 = Button(top, text='button1')
button1.place(relx = 0.5, rely = 0.5)
button2 = Button(top, text='button2')
button2.place(relx = 0, rely = 0)
button3 = Button(top, text='button3')
button3.place(relx = 0.8, rely = 0.8)
button4 = Button(top, text='button4')
button4.place(relx = 0, rely = 0.8)

mainloop()
