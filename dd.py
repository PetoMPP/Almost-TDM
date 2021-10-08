from re import T
from tkinter.font import Font
from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
from tkinter import ttk
import os.path, getpass, pyodbc, threading, time

def dd(oldframe, active_mode, mainframe, root):

    if active_mode != "dd":
    
        for child in oldframe.winfo_children():
            child.destroy()
            mainframe.configure(bg='#525252')

        def delete_entry(*arg):
            if dict_tree.focus() != "":
                dict_tree.delete(dict_tree.focus())

        def insert_entry(*arg):
            if fusion_entry.get() != "" and tdm_entry.get() != "":
                dict_tree.insert('', 'end', values=(fusion_entry.get(), tdm_entry.get()))
                tdm_entry.delete(0, END)
                fusion_entry.delete(0, END)
                fusion_entry.focus()

        def save_file():
            response = messagebox.askokcancel("Potwierdź nadpisanie listy", "Zapisanie listy spowoduje nadpisanie starego słownika.\
                \nCzy chcesz kontynuować?")
            if response == 1:
                dict_file = open("fusion_dict.txt", "w")
                for child in dict_tree.get_children():
                    data = dict_tree.item(child)['values']
                    line = "%s: %s\n" % (data[0], data[1])
                    dict_file.write(line)

        def refresh_dict(*arg):
            dict_tree.delete(*dict_tree.get_children())
            dict_file = open("fusion_dict.txt", "r+")
            for line in dict_file:
                fusion_name, tdm_name_lb = line.split(": ")
                tdm_name = ""
                for char in tdm_name_lb:
                    if char != "\n":
                        tdm_name = tdm_name + char
                    else:
                        break
                dict_tree.insert('', 'end', values=(fusion_name, tdm_name))
            dict_file.close()



        search_tree_style = ttk.Style()

        search_tree_style.theme_use('clam')
        
        search_tree_style.map('Treeview',
        background=[('selected', '#303030'), ('', '#aaaaaa')],
        foreground=[ ('selected', '#ffffff'), ('', '#000000')],
        fieldbackground=[('','#aaaaaa')],
        font=[('', ('Microsoft JhengHei UI', '12'))])

        search_tree_style.map('Treeview.Heading',
        foreground=[('', 'white')],
        background=[('active', '#555555'), ('', '#303030')],
        font=[('', ('Microsoft JhengHei UI', '10'))],
        bordercolor=[('', '#505050')],
        borderwidth=[('', 2)],
        lightcolor=[('', '#aaaaaa')],
        darkcolor=[('', '#111111')])

        search_tree_style.map('TEntry',
        font=[('', ('Microsoft JhengHei UI', '12'))],
        fieldbackground=[('', '#aaaaaa')],
        selectbackground=[('', 'blue')],
        foreground=[('', 'black')],
        borderwidth=[('', 2)])

        search_tree_style.map('TButton',
        foreground=[('', 'white')],
        background=[('pressed', '#464646'), ('', '#555555')],
        darkcolor=[('pressed', '#999999'), ('', '#050505')],
        lightcolor=[('pressed', '#050505'), ('', '#999999')],
        bordercolor=[('', '#525252')],
        focuscolor=[('', '#000000')],
        stipple=[('', '')],
        font=[('', ('Microsoft JhengHei UI', '16'))],
        borderwidth=[('', 2)])

        search_tree_style.map('Vertical.TScrollbar',
        background=[('pressed', '#555555'), ('active', '#464646'), ('', '#303030')],
        gripcount=[('', 0)],
        darkcolor=[('', '#999999')],
        lightcolor=[('', '#999999')],
        bordercolor=[('', '#666666')],
        arrowcolor=[('', 'white')],
        troughcolor=[('', '#aaaaaa')])

        search_tree_style.configure('TFrame',
        background='#303030')

        label_title = Label(mainframe, text="Datron Dictator v1.0.0")
        label_title.configure(fg='white', bg='#525252', font=('Microsoft JhengHei UI', 26))
        intro = Label(mainframe, text="Moduł do manipulacji słownikiem do automatycznej zamiany numerów katalogowych narzędzi w programach z Fusion")
        intro.configure(fg='white', bg='#404040', font=('Microsoft JhengHei UI', 10))
    
        left_frame = Frame(mainframe, bg='#404040', borderwidth=0, highlightthickness=0)
        right_frame = Frame(mainframe, bg='#404040', borderwidth=0, highlightthickness=0)

        col_names = ["Nazwa z pliku *.simpl", "Nazwa w TDM"]
        container = ttk.Frame(left_frame)

        dict_tree = ttk.Treeview(container)
        dict_tree['columns'] = col_names
        dict_tree['show'] = 'headings'
        dict_tree.column(col_names[0], minwidth=60, width=140)
        dict_tree.column(col_names[1], minwidth=60, width=220)
        for col in col_names:
            dict_tree.heading(col, text=col)

        button_del = Button(left_frame, text="Usuń wpis ze słownika")
        button_del.configure(fg='white', bg='#aa4646', activeforeground='white', activebackground='#aa5555', font=('Microsoft JhengHei UI', 10), command=delete_entry)
        button_save = Button(left_frame, text="Zapisz słownik")
        button_save.configure(fg='white', bg='#46aa46', activeforeground='white', activebackground='#55aa55', font=('Microsoft JhengHei UI', 10), command=save_file)

        vsc = ttk.Scrollbar(container, orient="vertical", command=dict_tree.yview)
        dict_tree.configure(yscrollcommand=vsc.set)

        refresh_button = Button(right_frame, text="Załaduj ponownie słownik")
        refresh_button.configure(fg='white', bg='#4646aa', activeforeground='white', activebackground='#5555aa', font=('Microsoft JhengHei UI', 12), command=refresh_dict)


        add_frame = LabelFrame(right_frame, text="Dodaj nowy wpis")
        add_frame.configure(fg='white', bg='#404040', font=('Microsoft JhengHei UI', 10))
        label_right = Label(add_frame, text="Dodaj nowy wpis")
        label_right.configure(fg='white', bg='#404040', font=('Microsoft JhengHei UI', 18))
        fusion_label = Label(add_frame, text="nazwa w Fusion")
        fusion_label.configure(fg='white', bg='#404040', font=('Microsoft JhengHei UI', 12))
        fusion_entry = Entry(add_frame, font=('Microsoft JhengHei UI', 12))
        tdm_label = Label(add_frame, text="Nazwa w TDM")
        tdm_label.configure(fg='white', bg='#404040', font=('Microsoft JhengHei UI', 12))
        tdm_entry = Entry(add_frame, font=('Microsoft JhengHei UI', 12))
        button_add = Button(add_frame, text="Dodaj wpis")
        button_add.configure(fg='white', bg='#464646', activeforeground='white', activebackground='#555555', font=('Microsoft JhengHei UI', 12), command=insert_entry)


        label_title.pack(fill='x', anchor=N, ipady=10)
        intro.pack(fill='x', expand=False, anchor=N, ipady=15)
        left_frame.pack(fill='both', expand=True, side='left')
        right_frame.pack(fill='both', expand=True, side='left')

        container.pack(fill='both', expand=True, padx=10)
        dict_tree.pack(side='left', fill='both', expand=True, anchor=NW)
        vsc.pack(side='right', fill='y', expand=False, anchor=NE)
        button_save.pack(side='left', anchor=W, padx=10, pady=10)
        button_del.pack(side='right', anchor=E, padx=10, pady=10)


        refresh_button.pack(side='top', anchor=NW, padx=10, pady=10)
        add_frame.pack(side='left', anchor=NW, padx=10, pady=10, fill='x')
        label_right.grid(row=0, column=0, columnspan=2, padx=10, pady=5)
        fusion_label.grid(row=1, column=0, padx=10, pady=5)
        tdm_label.grid(row=1, column=1, padx=10, pady=5)
        fusion_entry.grid(row=2, column=0, padx=10, pady=5)
        tdm_entry.grid(row=2, column=1, padx=10, pady=5)
        button_add.grid(row=3, column=1, padx=10, pady=5, ipadx=5, sticky=E)

        tdm_entry.bind('<Return>', insert_entry)
        fusion_entry.bind('<Return>', insert_entry)
        root.bind('<Delete>', delete_entry)
        
        '''for col in col_names:
            dict_tree.heading(col, text=col)
            print(Font().measure(col.title()))
            for child in dict_tree.get_children():
                data = dict_tree.set(child, col)
                print(data)
            dict_tree.column(col, width=Font().measure(col.title()))'''

        refresh_dict()



