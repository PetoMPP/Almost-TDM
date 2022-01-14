from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk
import os.path, os
from ctypes import windll
import threading, webbrowser, pyodbc, winsound
from modules import modes

#root base
root = Tk()
root.title("Almost TDM © PetoMPP 2021")
root.iconphoto(True, ImageTk.PhotoImage(Image.open(os.path.dirname(os.path.realpath(__file__)) + "\img\icon.ico")))
root.configure(background='#525252')
root.geometry("1100x950+50+50")
root.minsize(width=900, height=900)
#root.state("zoomed")
windll.shcore.SetProcessDpiAwareness(1) #THIS IS AMAZING


global active_mode

active_mode = "state_0"

def report_issue():
    webbrowser.open('mailto:pietrzyk.p@axito.pl', new=1)

def start_email_thread():
    email_thread = threading.Thread(target=report_issue)
    email_thread.daemon = True
    email_thread.start()

def playback_thread_start():
    winsound.PlaySound(os.path.dirname(os.path.realpath(__file__)) + '/modules/nothing.wav', winsound.SND_ASYNC)
    button_suprise.configure(text="I hate Xi Jinping", command=playback_thread_stop)


def playback_thread_stop():
    winsound.PlaySound(None, winsound.SND_PURGE)
    button_suprise.configure(text="Don't click me", command=playback_thread_start)

def launch_tlr():
    os.system(".\\ext\\tlr\\ToolListRemoverUI.exe")

def start_tlr_process():
    tlr_thread = threading.Thread(target=launch_tlr)
    tlr_thread.daemon = True
    tlr_thread.start()

#mainframe placeholder
sideframe = LabelFrame(root)
sideframe.configure(borderwidth=0, highlightthickness=0, bg='#999999')
mainframe = Canvas(root)
mainframe.configure(borderwidth=0, highlightthickness=0, bg='#525252')

#define always on display
logo = ImageTk.PhotoImage(Image.open(os.path.dirname(os.path.realpath(__file__)) + "\img\logo.png"))
label_logo = Label(image=logo, background='#eeeeee')
label_side = Label(text="Applications Menu", width=16, font=('Segoe UI', 19), fg='white', bg='#303030')
label_tlm = Button(text="Tool List Maker", font=('Segoe UI', 16), fg='white', bg='#464646', activeforeground='white', activebackground='#555555', width=15, command=lambda: modes.tlm_(mainframe, active_mode, mainframe, root, label_tlm, label_exit, label_dd))
label_dd = Button(text="Datron Dictator", font=('Segoe UI', 16), fg='white', bg='#464646', activeforeground='white', activebackground='#555555', width=15, command= lambda: modes.dd_(mainframe, active_mode, mainframe, root))
label_tlr = Button(text="Tool List Remover", font=('Segoe UI', 16), fg='white', bg='#464646', activeforeground='white', activebackground='#555555', width=15, command= start_tlr_process)
label_exit = Button(text="Wyłącz moduł", font=('Segoe UI', 16), fg='red', bg='#464646', activeforeground='red', activebackground='#555555', width=15, command=lambda: modes.state_0(mainframe))
label_report = Button(text="Zgłoś problem", font=('Segoe UI', 16), fg='#00cad9', bg='#464646', activeforeground='#00cad9', activebackground='#555555', width=15, command=start_email_thread)
button_suprise = Button(text="Don't click me", command= playback_thread_start, font=('Segoe UI', 16), fg='white', bg='#464646', activeforeground='white', activebackground='#555555', width=15)
sound_commands_frame = LabelFrame(sideframe, borderwidth=0, highlightthickness=0, bg='#999999')


#styles

#put what's always on display

sideframe.pack(side='left', anchor=W, fill='both', expand=False)
mainframe.pack(side='left', anchor=W,  fill='both', expand=True)
#label_logo.grid(row=0, column=0, rowspan=2, pady=(0, 5), ipadx=21, ipady=5)
label_logo.pack(expand=None, ipadx=5, ipady=5, fill='both', in_=sideframe)
#label_side.grid(row=2, column=0, ipady=5)
label_side.pack(expand=None, fill='x', ipadx=2, ipady=2, in_=sideframe)
#label_tlm.grid(row=3, column=0, sticky=N, pady=5)
label_tlm.pack(expand=None, padx=5, pady=(10, 5), in_=sideframe)
label_dd.pack(expand=None, padx=5, pady=5, in_=sideframe)
#label_exit.grid(row=4, column=0, sticky=N, pady=5)
label_tlr.pack(expand=None, padx=5, pady=5, in_=sideframe)
label_exit.pack(expand=None, padx=5, pady=5, in_=sideframe)
label_report.pack(expand=None, padx=5, pady=15, in_=sideframe, side="bottom")
sound_commands_frame.pack(in_=sideframe, side="bottom", fill='both')
button_suprise.pack(padx=5, pady=5, in_=sound_commands_frame)


root.mainloop()