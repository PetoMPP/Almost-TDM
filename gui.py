from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
from PIL import Image, ImageTk
import os.path, getpass, pyodbc, threading, time
from ctypes import windll
from modules import toolgetmod, tdmsql, dirmod

#root base
root = Tk()
root.title("Almost TDM © PetoMPP 2021")
root.iconphoto(True, ImageTk.PhotoImage(Image.open(os.path.dirname(os.path.realpath(__file__)) + "\img\icon.ico")))
root.configure(background='#525252')
root.geometry("1910x900+2+20")
#root.state("zoomed")
windll.shcore.SetProcessDpiAwareness(1) #THIS IS AMAZING

global active_mode

active_mode = "state_0"

def state_0(oldframe, oldtitle):
    global active_mode
    global mainframe
    if active_mode != "state_0":
        oldframe.destroy()
        oldtitle.destroy()
        active_mode = "state_0"

def tlm(oldframe, oldtitle):
    global active_mode
    global mainframe
    global label_title
    global tool_mode_sel
    global list_id_sel
    global part_sel
    global material_sel
    global material_selection
    global material_list
    global mpf_file
    global source_entry
    global machine_sel
    global machine_selection
    global machine_list
    global fixture_sel
    global fixture_selection
    global fixture_list
    global list_type_sel
    global desc_sel
    global source_entry_value
    global entry_list_r2_value
    global entry_part_r2_value
    global entry_desc_r2_value
    global entry_username_value
    global optionmenu_material_r2_value
    global optionmenu_machine_r2_value
    global optionmenu_fixture_r2_value
    global cnxn

    if active_mode != "tlm":
        active_mode = "tlm"

        #call variables
        tool_mode_sel = IntVar()
        list_id_sel = IntVar()
        part_sel = IntVar()
        material_sel = IntVar()
        material_selection = StringVar()
        material_list = ["<brak połączenia z TDM>"]
        machine_sel = IntVar()
        machine_selection = StringVar()
        machine_list = ["<brak połączenia z TDM>"]
        fixture_sel = IntVar()
        fixture_selection = StringVar()
        fixture_list = ["<brak połączenia z TDM>"]
        list_type_sel = IntVar()
        desc_sel = IntVar()
        source_entry_value = StringVar()
        entry_list_r2_value = StringVar()
        entry_part_r2_value = StringVar()
        entry_desc_r2_value = StringVar()
        entry_username_value = StringVar()
        optionmenu_material_r2_value = StringVar()
        optionmenu_machine_r2_value = StringVar()
        optionmenu_fixture_r2_value = StringVar()
        
        #internal functions


        def select_mpf_file():
            mpf_file = filedialog.askopenfilename(initialdir="C:/", title="Wybierz program", filetypes=(("Pliki MPF", "*.mpf"), ("Wszystkie pliki", "*")))
            source_entry.configure(state=NORMAL)
            source_entry.insert(0, mpf_file)
            source_entry.configure(state=DISABLED)
            
        def select_simple_file():
            simple_file = filedialog.askopenfilename(initialdir="C:/", title="Wybierz program", filetypes=(("Pliki SIMPLE", "*.simple"), ("Wszystkie pliki", "*")))
            source_entry.configure(state=NORMAL)
            source_entry.insert(0, simple_file)
            source_entry.configure(state=DISABLED)

        def radio_switch():
            if tool_mode_sel.get() == 0:
                source_frame.configure(text="Wybierz plik *.mpf")
                source_butt.configure(command=select_mpf_file)
            elif tool_mode_sel.get() == 1:
                source_frame.configure(text="Wybierz plik *.simple")
                source_butt.configure(command=select_simple_file)

            if part_sel.get() == 0 or part_sel.get() == 2:
                entry_part_r2.configure(state=DISABLED)
            elif part_sel.get() == 1:
                entry_part_r2.configure(state=NORMAL)

            if material_sel.get() == 0 or material_sel.get() == 2:
                optionmenu_material_r2.configure(state=DISABLED)
            elif material_sel.get() == 1:
                optionmenu_material_r2.configure(state=NORMAL)

            if machine_sel.get() == 0 or machine_sel.get() == 2:
                optionmenu_machine_r2.configure(state=DISABLED)
            elif machine_sel.get() == 1:
                optionmenu_machine_r2.configure(state=NORMAL)

            if fixture_sel.get() == 0 or fixture_sel.get() == 2:
                optionmenu_fixture_r2.configure(state=DISABLED)
            elif fixture_sel.get() == 1:
                optionmenu_fixture_r2.configure(state=NORMAL)

            if desc_sel.get() == 0 or desc_sel.get() == 2:
                entry_desc_r2.configure(state=DISABLED)
            elif desc_sel.get() == 1:
                entry_desc_r2.configure(state=NORMAL)

            if list_id_sel.get() == 0:
                entry_list_r2.configure(state=DISABLED)
                part_r3.configure(state=DISABLED)
                desc_r3.configure(state=DISABLED)
                material_r3.configure(state=DISABLED)
                machine_r3.configure(state=DISABLED)
                fixture_r3.configure(state=DISABLED)
                list_type_r3.configure(state=DISABLED)
            elif list_id_sel.get() == 1:
                entry_list_r2.configure(state=NORMAL)
                part_r3.configure(state=NORMAL)
                desc_r3.configure(state=NORMAL)
                material_r3.configure(state=NORMAL)
                machine_r3.configure(state=NORMAL)
                fixture_r3.configure(state=NORMAL)
                list_type_r3.configure(state=NORMAL)
            
        
        def disable_side():
            global label_exit
            global label_tlm

            label_exit.configure(state=DISABLED)
            label_tlm.configure(state=DISABLED)
        
        def enable_side():
            global label_exit
            global label_tlm

            label_exit.configure(state=NORMAL)
            label_tlm.configure(state=NORMAL)

        def TDM_connect():
            global cnxn
            global material_list
            global machine_list
            global fixture_list
            
            root.config(cursor="wait")
            operations_butt_connect.configure(state=DISABLED)
            disable_side()
            disable_radios_buttons()
            output_label.configure(text="Łączenie z bazą danych TDM...", fg='white')
            try:
                cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER=uhlplvm03;DATABASE=TDMTEST;UID=tms;PWD=tms')
                output_label.configure(fg='green', text="Połączono")
                material_list = []
                machine_list = []
                fixture_list = []
                operations_butt_make.configure(state=NORMAL)
            except pyodbc.OperationalError:
                output_label.configure(fg='red', text="Błąd podczas łączenia się z bazą danych TDM")
            root.config(cursor="")
            operations_butt_connect.configure(state=NORMAL)
            enable_side()
            enable_radios_buttons()

        def start_TDM_connect_thread(event):
            global TDM_connect_thread
            TDM_connect_thread = threading.Thread(target=TDM_connect)
            TDM_connect_thread.daemon = True
            TDM_connect_thread.start()

        def TDM_create_list(cnxn, id, part_name, desc2, material, machine, fixture, list_type, user):
            cursor = cnxn.cursor()



        #replace old frame
        oldframe.destroy()
        oldtitle.destroy()
        
        label_title = Label(root, text="Tool List maker v2.0.0")

        mainframe = LabelFrame(root, padx=5, pady=5)
        intro = Label(mainframe, text="Witaj w pierwszym module paczek małych pomocników do pracy z programem TDM!\nW poniższym formularzu wybierz dane które chcesz, żeby były dodane do nowej listy narzędziowej", fg='white', bg='#303030')
        #sections

        #tool get mode
        tool_mode_frame = LabelFrame(mainframe, text="Wybierz tryb zbierania narzędzi")
        tool_mode_r1 = Radiobutton(tool_mode_frame, text="CTX / DMC / DMF", variable=tool_mode_sel, value=0, command=radio_switch)
        tool_mode_r2 = Radiobutton(tool_mode_frame, text="DATRON", variable=tool_mode_sel, value=1, command=radio_switch)

        #source file
        source_frame = LabelFrame(mainframe, text="Wybierz plik *.mpf")
        source_entry = Entry(source_frame, textvariable=source_entry_value)
        source_entry.configure(state=DISABLED)
        source_butt = Button(source_frame, text="Przeglądaj...", command=select_mpf_file)

        #list id
        list_frame = LabelFrame(mainframe, text="Wybierz Tool List ID:")
        list_r1 = Radiobutton(list_frame, text="Najwyższe wolne (stworzenie nowej listy)", variable=list_id_sel, value=0, command=radio_switch)
        list_r2 = Radiobutton(list_frame, text="Podaj ręcznie (nadpisanie istniejącej listy):", variable=list_id_sel, value=1, command=radio_switch)
        entry_list_r2 = Entry(list_frame)
        entry_list_r2.configure(state=DISABLED)

        #part name
        part_frame = LabelFrame(mainframe, text="Wybierz Nazwę programu (Tool List Desc. 1):")
        part_r1 = Radiobutton(part_frame, text="Automatycznie z nazwy pliku", variable=part_sel, value=0, command=radio_switch)
        part_r2 = Radiobutton(part_frame, text="Podaj ręcznie:", variable=part_sel, value=1, command=radio_switch)
        entry_part_r2 = Entry(part_frame)
        entry_part_r2.configure(state=DISABLED)
        part_r3 = Radiobutton(part_frame, text="Pozostaw bez zmian", variable=part_sel, value=2, command=radio_switch)

        #desc
        desc_frame = LabelFrame(mainframe, text="Opis programu (Tool List Desc. 2)")
        desc_r1 = Radiobutton(desc_frame, text="Nie chcę dodawać opisu", variable=desc_sel, value=0, command=radio_switch)
        desc_r2 = Radiobutton(desc_frame, text="Wprowadź opis:", variable=desc_sel, value=1, command=radio_switch)
        entry_desc_r2 = Entry(desc_frame)
        entry_desc_r2.configure(state=DISABLED)
        desc_r3 = Radiobutton(desc_frame, text="Pozostaw bez zmian", variable=desc_sel, value=2, command=radio_switch)

        #material
        material_frame = LabelFrame(mainframe, text="Wybierz materiał:")
        material_r1 = Radiobutton(material_frame, text="Nie chcę dodawać materiału", variable=material_sel, value=0, command=radio_switch)
        material_r2 = Radiobutton(material_frame, text="Wybierz z listy:", variable=material_sel, value=1, command=radio_switch)
        optionmenu_material_r2 = OptionMenu(material_frame, material_selection, *material_list)
        material_selection.set(material_list[0])
        optionmenu_material_r2.configure(state=DISABLED)
        material_r3 = Radiobutton(material_frame, text="Pozostaw bez zmian", variable=material_sel, value=2, command=radio_switch)

        #machine
        machine_frame = LabelFrame(mainframe, text="Wybierz maszynę:")
        machine_r1 = Radiobutton(machine_frame, text="Nie chcę dodawać maszyny", variable=machine_sel, value=0, command=radio_switch)
        machine_r2 = Radiobutton(machine_frame, text="Wybierz z listy:", variable=machine_sel, value=1, command=radio_switch)
        optionmenu_machine_r2 = OptionMenu(machine_frame, machine_selection, *machine_list)
        machine_selection.set(machine_list[0])
        optionmenu_machine_r2.configure(state=DISABLED)
        machine_r3 = Radiobutton(machine_frame, text="Pozostaw bez zmian", variable=machine_sel, value=2, command=radio_switch)

        #fixture
        fixture_frame = LabelFrame(mainframe, text="Wybierz mocowanie:")
        fixture_r1 = Radiobutton(fixture_frame, text="Nie chcę dodawać mocowania", variable=fixture_sel, value=0, command=radio_switch)
        fixture_r2 = Radiobutton(fixture_frame, text="Wybierz z listy:", variable=fixture_sel, value=1, command=radio_switch)
        optionmenu_fixture_r2 = OptionMenu(fixture_frame, fixture_selection, *fixture_list)
        fixture_selection.set(fixture_list[0])
        optionmenu_fixture_r2.configure(state=DISABLED)
        fixture_r3 = Radiobutton(fixture_frame, text="Pozostaw bez zmian", variable=fixture_sel, value=2, command=radio_switch)
        #listtype
        list_type_frame = LabelFrame(mainframe, text="Wybierz typ listy narzędziowej:")
        list_type_r1 = Radiobutton(list_type_frame, text="Primary", variable=list_type_sel, value=0)
        list_type_r2 = Radiobutton(list_type_frame, text="Secondary", variable=list_type_sel, value=1)
        list_label = Label(list_type_frame)
        list_type_r3 = Radiobutton(list_type_frame, text="Pozostaw bez zmian", variable=list_type_sel, value=2, command=radio_switch)
        #username locked
        username = getpass.getuser()
        username_frame = LabelFrame(mainframe, text="Nazwa użytkownika")
        username_label = Label(username_frame, text="Nazwy użytkownika nie można zmienić :)")
        entry_username = Entry(username_frame)
        entry_username.insert(0, username.upper())
        entry_username.configure(state=DISABLED)

        #operations
        operations_frame = LabelFrame(mainframe, text="Działania")
        operations_label = Label(operations_frame, text="Do poprawnego funkcjonowania programu potrzebne jest połączenie z TDM")
        operations_butt_connect = Button(operations_frame, text="Połącz z bazą TDM", command=lambda: start_TDM_connect_thread(None))
        operations_butt_make = Button(operations_frame, text="Stwórz Listę", command= lambda: make_list())

        #output
        output_frame = LabelFrame(mainframe)
        output_label = Label(output_frame, text="sex")

        #styles
        tlm_title = [label_title]
        tlm_labels = [intro, username_label, operations_label, output_label, list_label]
        tlm_frames = [mainframe, tool_mode_frame, source_frame, list_frame, part_frame, desc_frame, material_frame, machine_frame, fixture_frame, list_type_frame, username_frame, operations_frame, output_frame]
        tlm_radios = [tool_mode_r1, tool_mode_r2, list_r1, list_r2, part_r1, part_r2, part_r3, material_r1, material_r2, material_r3, machine_r1, machine_r2, machine_r3, fixture_r1, fixture_r2, fixture_r3, list_type_r1, list_type_r2, list_type_r3, desc_r1, desc_r2, desc_r3]
        tlm_buttons = [source_butt, operations_butt_connect, operations_butt_make]
        tlm_optionmenus = [optionmenu_material_r2, optionmenu_machine_r2, optionmenu_fixture_r2]
        tlm_entries = [source_entry, entry_list_r2, entry_part_r2, entry_desc_r2, entry_username]

        tlm_components = [tlm_title, tlm_labels, tlm_frames, tlm_radios, tlm_buttons, tlm_optionmenus, tlm_entries]


        #apply styles
        for group in tlm_components:
            for element in group:
                if group is tlm_title:
                    element.configure(fg='white', bg='#525252', font=('', 26))
                if group is tlm_labels:
                    element.configure(fg='white', bg='#303030', font=('', 12))
                if group is tlm_frames:
                    element.configure(fg='white', bg='#303030', borderwidth=1, highlightthickness=0, font=('', 12))
                if group is tlm_radios:
                    element.configure(fg='white', bg='#303030', activebackground='#303030', activeforeground='white', selectcolor='black', font=('', 12))
                if group is tlm_buttons:
                    element.configure(fg='white', bg='#464646', activeforeground='white', activebackground='#555555', font=('', 12))
                if group is tlm_optionmenus:
                    element.configure(width=25, foreground='black', background='#aaaaaa', activeforeground='black', activebackground='#aaaaaa', borderwidth=0, highlightthickness=0, font=('', 12))
                if group is tlm_entries:
                    element.configure(width=15, disabledforeground='black', disabledbackground='#aaaaaa', font=('', 12), borderwidth=2)

        #modify styles apllied by loop
        source_entry.configure(width=80)
        operations_butt_make.configure(bg='#00c70a', activebackground='#00f20c', state=DISABLED)
        output_label.configure(anchor='e', width=180)

        
        def disable_radios_buttons():
            for ele in tlm_radios:
                ele.configure(state=DISABLED)
            for ele in tlm_buttons:
                ele.configure(state=DISABLED)
        
        def enable_radios_buttons():
            for ele in tlm_radios:
                ele.configure(state=NORMAL)
            for ele in tlm_buttons:
                if ele != operations_butt_make:
                    ele.configure(state=NORMAL)

        #put elements on the screen
        label_title.grid(row=0, column=1, ipadx=60)
        mainframe.grid(row=1, column=1, rowspan=5000, sticky=N+E+W+S, padx=5, pady=(0, 5))
        intro.grid(row=0, column=0, columnspan=6, pady=10)
        
        tool_mode_frame.grid(row=1, column=0, pady=10, padx=10, ipady=3, ipadx=3, sticky=W+E)
        tool_mode_r1.grid(row=0, column=0, padx=5, sticky=W)
        tool_mode_r2.grid(row=1, column=0, padx=5, sticky=W)

        source_frame.grid(row=1, column=1, columnspan=2, pady=10)
        source_entry.grid(row=0, column=0, padx= 10)
        source_butt.grid(row=0, column=1, padx= 10, pady=10)

        list_elems = [list_frame, list_r1, list_r2, entry_list_r2]
        part_elems = [part_frame, part_r1, part_r2, entry_part_r2, part_r3]
        desc_elems = [desc_frame, desc_r1, desc_r2, entry_desc_r2, desc_r3]
        material_elems = [material_frame, material_r1, material_r2, optionmenu_material_r2, material_r3]
        machine_elems = [machine_frame, machine_r1, machine_r2, optionmenu_machine_r2, machine_r3]
        fixture_elems = [fixture_frame, fixture_r1, fixture_r2, optionmenu_fixture_r2, fixture_r3]
        list_type_elems = [list_type_frame, list_type_r1, list_type_r2, list_label, list_type_r3]
        username_elems = [username_frame, username_label, entry_username]
        operations_elems = [operations_frame, operations_label, operations_butt_connect, operations_butt_make]

        tlm_sections = [list_elems, part_elems, desc_elems, material_elems, machine_elems, fixture_elems, list_type_elems, username_elems, operations_elems]

        i_section_row = 2
        i_section_column = 0
        for section in tlm_sections:
            i_row = 0
            i_column = 0
            for element, index in zip(section, range(len(section))):
                if index == 0:
                    element.grid(row=i_section_row, column=i_section_column, pady=10, padx=10, ipady=3, ipadx=3, sticky=W+E)
                if index > 0:
                    if i_row == i_column:
                        element.grid(row=i_row, column=i_column, padx=5, sticky=W)
                        i_row += 1
                    elif i_row > i_column:
                        element.grid(row=i_row, column=i_column, padx=5, sticky=W)
                        i_column += 1
                    if i_row >= 2:
                        i_column = 0
            if i_section_column == 2:
                i_section_row += 1
                i_section_column = 0
            else:
                i_section_column += 1
            
            for element in username_elems:
                element.grid(pady=2)
            
        for element, index in zip(operations_elems, range(len(operations_elems))):
            if index == 1:
                element.grid(columnspan=2)
            elif index > 1:
                element.grid_forget()
                element.grid(row=1, column=index-2)

        output_frame.grid(row=(tlm_sections[len(tlm_sections)-1])[0].grid_info()['row']+1, column=0, columnspan=3, sticky=W+E, padx=10)
        output_label.grid(row=0, column=0, columnspan=3, sticky=E)
        
        part_r3.configure(state=DISABLED)
        desc_r3.configure(state=DISABLED)
        material_r3.configure(state=DISABLED)
        machine_r3.configure(state=DISABLED)
        fixture_r3.configure(state=DISABLED)
        list_type_r3.configure(state=DISABLED)

        
        def make_list():
            #tool get mode
            tlist = []
            if tool_mode_sel == 0: #mpf
                source_path = source_entry_value.get()
                try:
                    tlist = toolgetmod.fileTlistLimited(source_path, 100)
                except:
                    messagebox.showerror("Błąd", "Zły plik źródłowy")
                    return None
                if list_id_sel == 0: #new list
                    listID = tdmsql.tdmGetMaxListID(cnxn)
                    if part_sel.get() == 0:
                        NCprogram = ""
                        for char in os.path.basename(source_path):
                            if char != '.':
                                NCprogram += char
                            else:
                                break
                    elif part_sel.get() == 1:
                        NCprogram = entry_part_r2.get()

                    user = getpass.getuser()
                    user = user.upper()
                    timestamp = round(time.time())
                    username = tdmsql.tdmGetUserName(cnxn, user)
                    validTools = tdmsql.tdmCheckIfToolsExists(cnxn, tlist)
                    if validTools:
                        tdmsql.tdmCreateList(cnxn, NCprogram, listID, username, timestamp)
                        tdmsql.tdmAddTools(cnxn, listID, tlist, timestamp)
                        tdmsql.tdmAddLogfile(cnxn, listID, user, timestamp)
                        tdmsql.tdmDisconnect(cnxn)
                elif list_id_sel == 1: #update list
                    pass
            elif tool_mode_sel == 1: #datron
                fusion_dict = {}
                dict_file = open("fusion_dict.txt")
                for line in dict_file:
                    key, value = line.split(": ")
                    fusion_dict[key] = value







#mainframe placeholder
mainframe = LabelFrame(root)
label_title = Label(root)

#define always on display
logo = ImageTk.PhotoImage(Image.open(os.path.dirname(os.path.realpath(__file__)) + "\img\logo.png"))
label_logo = Label(image=logo, background='#EEEEEE')
label_side = Label(text="Applications Menu", width=16, font=('', 19), fg='white', bg='#303030')
label_tlm = Button(text="Tool List Maker", font=('', 16), fg='white', bg='#464646', activeforeground='white', activebackground='#555555', width=15, command=lambda: tlm(mainframe, label_title))
label_exit = Button(text="Wyłącz moduł", font=('', 16), fg='red', bg='#464646', activeforeground='red', activebackground='#555555', width=15, command=lambda: state_0(mainframe, label_title))

#styles

#put what's always on display
label_logo.grid(row=0, column=0, rowspan=2, pady=(0, 5), ipadx=21, ipady=5)
label_side.grid(row=2, column=0, ipady=5)
label_tlm.grid(row=3, column=0, sticky=N, pady=5)
label_exit.grid(row=4, column=0, sticky=N, pady=5)



root.mainloop()