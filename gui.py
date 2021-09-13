from tkinter import *
from tkinter import filedialog
from PIL import Image, ImageTk
import os.path

#root base
root = Tk()
root.title("Almost TDM © PetoMPP 2021")
root.iconphoto(True, ImageTk.PhotoImage(Image.open(os.path.dirname(os.path.realpath(__file__)) + "\img\icon.ico")))
root.configure(background='#525252')


def state_0(oldframe, oldtitle):
    global mainframe
    oldframe.destroy()
    oldtitle.destroy()
    '''#elements
    mainframe = LabelFrame(root, text="Wybierz aplikacje z panelu po lewej", fg='white', bg='#303030', padx=5, pady=5)
    placeholder = Label(mainframe, text="...", fg='white', bg='#303030')

    #put elements on the screen
    mainframe.grid(row=1, column=1, rowspan=5, columnspan=7, sticky=E+W, padx=5, pady=(0, 5))
    placeholder.grid(row=0, column=0)'''

def tlm(oldframe, oldtitle):
    global mainframe
    global label_title
    global list_id_sel

    #call variables
    list_id_sel = IntVar()

    #replace old frame
    oldframe.destroy()
    oldtitle.destroy()
    
    label_title = Label(root, text="Tool List maker v2.0.0", fg='white', bg='#525252', font=('', 16))

    mainframe = LabelFrame(root, fg='white', bg='#303030', padx=5, pady=5, borderwidth= 0, highlightthickness=0)
    intro = Label(mainframe, text="Witaj w pierwszym module paczek małych pomocników do pracy z programem TDM!\nW poniższym formularzu wybierz dane które chcesz, żeby były dodane do nowej listy narzędziowej", fg='white', bg='#303030')
    #sections
    #list id
    list_frame = LabelFrame(mainframe, text="Wybierz Tool List ID:", fg='white', bg='#303030', borderwidth= 0)
    list_r1 = Radiobutton(list_frame, text="Automatycznie", fg='white', bg='#303030', activebackground='#303030', activeforeground='white', selectcolor='black', variable=list_id_sel, value=0)
    list_r2 = Radiobutton(list_frame, text="Podaj ręcznie (niezalecane)", fg='white', bg='#303030', activebackground='#303030', activeforeground='white', selectcolor='black', variable=list_id_sel, value=1)
    entry_r2 = Entry(list_frame, width=15, state=DISABLED)

    #part name


    #material


    #machine


    #fixture


    #listtype


    #username locked

    #put elements on the screen
    label_title.grid(row=0, column=1, ipadx=60)
    mainframe.grid(row=1, column=1, rowspan=5, sticky=N+E+W, padx=5, pady=(0, 5))
    intro.grid(row=0, column=0, columnspan=6)

    list_frame.grid(row=1, column=0)
    list_r1.grid(row=0, column=0, sticky=W)
    list_r2.grid(row=1, column=0, sticky=W)
    entry_r2.grid(row=1, column=1)






#mainframe placeholder
mainframe = LabelFrame(root)
label_title = Label(root)

#define always on display
logo = ImageTk.PhotoImage(Image.open(os.path.dirname(os.path.realpath(__file__)) + "\img\logo.png"))
label_logo = Label(image=logo, background='#EEEEEE')
label_side = Label(text="Applications Menu", width=15, font=('', 16), fg='white', bg='#303030')
label_tlm = Button(text="Tool List Maker", font=('', 12), fg='white', bg='#464646', activeforeground='white', activebackground='#555555', width=15, command=lambda: tlm(mainframe, label_title))
label_exit = Button(text="Wyłącz moduł", font=('', 12), fg='red', bg='#464646', activeforeground='red', activebackground='#555555', width=15, command=lambda: state_0(mainframe, label_title))

#put what's always on display
label_logo.grid(row=0, column=0, rowspan=2, pady=(0, 5))
label_side.grid(row=2, column=0)
label_tlm.grid(row=3, column=0, sticky=N, pady=5)
label_exit.grid(row=4, column=0, sticky=N, pady=5)




root.mainloop()