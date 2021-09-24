from tkinter import *
from tkinter import font
from ctypes import windll


root = Tk()
windll.shcore.SetProcessDpiAwareness(1)
root.configure(background='#525252')
print(font.families())
i = 0
j = 0
for fon in font.families():
    label = Label(root, text="▼  : "+str(fon), font=(fon, 13), fg='white', bg='#525252')
    label.grid(row=i, column=j)
    i += 1
    if i % 30 == 0:
        j +=1
        i = 0

root.mainloop()