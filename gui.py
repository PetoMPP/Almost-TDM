from tkinter.font import Font
from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
from tkinter import ttk
from PIL import Image, ImageTk
import os.path, getpass, pyodbc, threading, time, re
from ctypes import windll
from modules import toolgetmod, tdmsql
import tlm

#root base
root = Tk()
root.title("Almost TDM © PetoMPP 2021")
root.iconphoto(True, ImageTk.PhotoImage(Image.open(os.path.dirname(os.path.realpath(__file__)) + "\img\icon.ico")))
root.configure(background='#525252')
root.geometry("1300x800+50+50")
root.minsize(width=1300, height=800)
#root.state("zoomed")
windll.shcore.SetProcessDpiAwareness(1) #THIS IS AMAZING


global active_mode

active_mode = "state_0"

def state_0(oldframe):
    global active_mode
    global mainframe
    if active_mode != "state_0":
        for child in oldframe.winfo_children():
            child.destroy()
            mainframe.configure(bg='#525252')
        active_mode = "state_0"






#mainframe placeholder
sideframe = LabelFrame(root)
sideframe.configure(borderwidth=0, highlightthickness=0, bg='#999999')
mainframe = LabelFrame(root)
mainframe.configure(borderwidth=0, highlightthickness=0, bg='#525252')

#define always on display
logo = ImageTk.PhotoImage(Image.open(os.path.dirname(os.path.realpath(__file__)) + "\img\logo.png"))
label_logo = Label(image=logo, background='#eeeeee')
label_side = Label(text="Applications Menu", width=16, font=('Microsoft JhengHei UI', 19), fg='white', bg='#303030')
label_tlm = Button(text="Tool List Maker", font=('Microsoft JhengHei UI', 16), fg='white', bg='#464646', activeforeground='white', activebackground='#555555', width=15, command=lambda: tlm.tlm(mainframe, active_mode, mainframe, root, label_tlm, label_exit))
label_exit = Button(text="Wyłącz moduł", font=('Microsoft JhengHei UI', 16), fg='red', bg='#464646', activeforeground='red', activebackground='#555555', width=15, command=lambda: state_0(mainframe))

#styles

#put what's always on display

sideframe.pack(side='left', anchor=W, fill='both', expand=False)
mainframe.pack(side='left', anchor=W,  fill='both', expand=True)
#label_logo.grid(row=0, column=0, rowspan=2, pady=(0, 5), ipadx=21, ipady=5)
label_logo.pack(expand=None, ipadx=5, ipady=5, fill='both', in_=sideframe)
#label_side.grid(row=2, column=0, ipady=5)
label_side.pack(expand=None, fill='x', ipadx=2, ipady=2, in_=sideframe)
#label_tlm.grid(row=3, column=0, sticky=N, pady=5)
label_tlm.pack(expand=None, padx=5, pady=5, in_=sideframe)
#label_exit.grid(row=4, column=0, sticky=N, pady=5)
label_exit.pack(expand=None, padx=5, pady=5, in_=sideframe)



root.mainloop()