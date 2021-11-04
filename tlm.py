from tkinter.font import Font
from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
from tkinter import ttk
import os.path, getpass, pyodbc, threading, time, re, os
from modules import toolgetmod, tdmsql
from ctypes import windll


def tlm(oldframe, active_mode, mainframe, root, label_tlm1, label_exit1, label_dd1):
    global mpf_files
    global cnxn
    global tdm_connected
    global label_tlm
    global label_exit
    global label_dd
    global server_available


    if active_mode != "tlm":
        
        for child in oldframe.winfo_children():
            child.destroy()
            mainframe.configure(bg='#525252')

        mpf_files = None
        label_tlm = label_tlm1
        label_exit = label_exit1
        label_dd = label_dd1

        #call variables
        tool_mode_sel = IntVar()
        list_id_sel = IntVar()
        part_sel = IntVar()
        material_sel = IntVar()
        machine_sel = IntVar()
        fixture_sel = IntVar()
        list_type_sel = IntVar()
        desc_sel = IntVar()

        server_available = False
        
        #internal functions
        def select_mpf_file():
            global mpf_files
            mpf_files = filedialog.askopenfilenames(initialdir="M:/", title="Wybierz program", filetypes=(("Pliki MPF/SPF", ["*.mpf", "*.spf"]), ("Wszystkie pliki", "*")))
            source_entry.configure(state=NORMAL)
            source_entry.delete(0, END)
            source_entry.insert(0, mpf_files)
            source_entry.configure(state=DISABLED)
            
        def select_simple_file():
            global mpf_files
            mpf_files = filedialog.askopenfilenames(initialdir="M:/", title="Wybierz program", filetypes=(("Pliki SIMPL", "*.simpl"), ("Wszystkie pliki", "*")))
            source_entry.configure(state=NORMAL)
            source_entry.delete(0, END)
            source_entry.insert(0, mpf_files)
            source_entry.configure(state=DISABLED)

        def radio_switch():
            if tool_mode_sel.get() == 0:
                source_frame.configure(text="Wybierz plik(i) *.mpf/*.spf")
                source_butt.configure(command=select_mpf_file)
                    
            elif tool_mode_sel.get() == 1:
                source_frame.configure(text="Wybierz plik(i) *.simpl")
                source_butt.configure(command=select_simple_file)
                entry_machine_r2.configure(state=NORMAL)

            if tool_mode_sel.get() == 2:
                source_frame.configure(text="Wybierz plik(i) *.mpf")
                source_butt.configure(command=select_mpf_file)
                entry_machine_r2.configure(state=NORMAL)

            if part_sel.get() == 0 or part_sel.get() == 2:
                entry_part_r2.configure(state=DISABLED)
                part_r2_butt.configure(state=DISABLED)
            elif part_sel.get() == 1:
                entry_part_r2.configure(state=NORMAL)
                part_r2_butt.configure(state=NORMAL)

            if material_sel.get() == 0 or material_sel.get() == 2:
                entry_material_r2.configure(state=DISABLED)
                material_r2_butt_All.configure(state=DISABLED)
                material_r2_butt_Used.configure(state=DISABLED)
            elif material_sel.get() == 1:
                entry_material_r2.configure(state=NORMAL)
                material_r2_butt_All.configure(state=NORMAL)
                material_r2_butt_Used.configure(state=NORMAL)

            if machine_sel.get() == 0 or machine_sel.get() == 2:
                entry_machine_r2.configure(state=DISABLED)
                machine_r2_butt_All.configure(state=DISABLED)
            elif machine_sel.get() == 1:
                entry_machine_r2.configure(state=NORMAL)
                machine_r2_butt_All.configure(state=NORMAL)

            if fixture_sel.get() == 0 or fixture_sel.get() == 2:
                entry_fixture_r2.configure(state=DISABLED)
                #fixture_r2_butt_All.configure(state=DISABLED)
                fixture_r2_butt_Used.configure(state=DISABLED)
            elif fixture_sel.get() == 1:
                entry_fixture_r2.configure(state=NORMAL)
                fixture_r2_butt_Used.configure(state=NORMAL)

            if desc_sel.get() == 0 or desc_sel.get() == 2:
                entry_desc_r2.configure(state=DISABLED)
                desc_r2_butt.configure(state=DISABLED)
            elif desc_sel.get() == 1:
                entry_desc_r2.configure(state=NORMAL)
                desc_r2_butt.configure(state=NORMAL)

            if list_id_sel.get() == 0:
                entry_list_r2.configure(state=DISABLED)
                list_r2_butt.configure(state=DISABLED)
                for radio in radio_switches_3:
                    radio.configure(state=DISABLED)
                for var in radio_variables_3:
                    if var.get() == 2:
                        var.set(0)
            elif list_id_sel.get() == 1:
                entry_list_r2.configure(state=NORMAL)
                list_r2_butt.configure(state=NORMAL)
                for radio in radio_switches_3:
                    radio.configure(state=NORMAL)
                 
        def disable_side():
            global label_exit
            global label_tlm
            global label_dd

            label_exit.configure(state=DISABLED)
            label_tlm.configure(state=DISABLED)
            label_dd.configure(state=DISABLED)
        
        def enable_side():
            global label_exit
            global label_tlm
            global label_dd

            label_exit.configure(state=NORMAL)
            label_tlm.configure(state=NORMAL)
            label_dd.configure(state=NORMAL)

        def TDM_connect():
            global cnxn
            global material_list
            global machine_list
            global fixture_list
            global tdm_connected
            
            root.config(cursor="wait")
            #operations_butt_connect.configure(state=DISABLED)
            disable_side()
            disable_radios_buttons()
            output_label.configure(text="Łączenie z bazą danych TDM...", fg='white')
            try:
                cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER=uhlplvm03;DATABASE=TDMPROD;UID=tms;PWD=tms', timeout=1)
                output_label.configure(fg='green', text="Połączono")
                operations_butt_make.configure(state=NORMAL)
                tdm_connected = True
            except pyodbc.OperationalError:
                output_label.configure(fg='red', text="Błąd podczas łączenia się z bazą danych TDM")
                tdm_connected = False
            root.config(cursor="")
            #operations_butt_connect.configure(state=NORMAL)
            enable_side()
            enable_radios_buttons()
            radio_switch()
            '''for radio in radio_switches_3:
                radio.configure(state=DISABLED)'''
            if tdm_connected:
                return True
            else:
                return False


        def start_TDM_connect_thread(event):
            global TDM_connect_thread
            TDM_connect_thread = threading.Thread(target=TDM_connect)
            TDM_connect_thread.daemon = True
            TDM_connect_thread.start()

        def search(mode, widget):
            global col_names
            global ele_list
            global top
            global listbox
            global validate_cmd
            global server_available

            if not server_available:
                if os.system("ping -n 1  172.26.48.03") == 1:
                    messagebox.showerror("Brak połączenia", "Brak połączenia z serwerem bazy TDM")
                    return
                else:
                    server_available = True
            connection_valid = TDM_connect()
            if not connection_valid:
                messagebox.showwarning("Błąd połączenia", "Program nie mógł nazwiązać połączenia z bazą danych z niejasnych przyczyn.")
                return

            def create_treeview_content():
                global ele_list
                search_tree.delete(*search_tree.get_children())
                ele_list = clear_none_values(ele_list)
                for item in ele_list:
                    if len(item) == 1:
                        item_elements = item[0]
                    elif len(item) == 2:
                        item_elements = item[0] + ";|;" + item[1]
                    elif len(item) == 3:
                        item_elements = item[0] + ";|;" + item[1] + ";|;" + item[2]
                    search_tree.insert('', 'end', values=item, text=item_elements)

            def create_search_elements(selection_mode, widget):
                global container
                global s_container
                global search_tree
                global search_entry1
                global search_entry2
                global search_entry3
                global vsc
                global search_entries

                
                search_tree_style = ttk.Style()

                search_tree_style.theme_use('clam')
                
                search_tree_style.map('Treeview',
                background=[('selected', '#303030'), ('', '#aaaaaa')],
                foreground=[ ('selected', '#ffffff'), ('', '#000000')],
                fieldbackground=[('','#aaaaaa')],
                font=[('', ('Segoe UI', '12'))])

                search_tree_style.map('Treeview.Heading',
                foreground=[('', 'white')],
                background=[('active', '#555555'), ('', '#303030')],
                font=[('', ('Segoe UI', '10'))],
                bordercolor=[('', '#505050')],
                borderwidth=[('', 2)],
                lightcolor=[('', '#aaaaaa')],
                darkcolor=[('', '#111111')])

                search_tree_style.map('TEntry',
                font=[('', ('Segoe UI', '12'))],
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
                font=[('', ('Segoe UI', '16'))],
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

                container = ttk.Frame(top)
                s_container = ttk.Frame(top)
                search_tree = ttk.Treeview(container)
                search_tree['columns'] = col_names
                search_tree['show'] = 'headings'

                if len(col_names) == 3:
                    search_entry1 = ttk.Entry(top, width=21, font=('Segoe UI', 12))
                    search_entry2 = ttk.Entry(top, width=21, font=('Segoe UI', 12))
                    search_entry3 = ttk.Entry(top, width=21, font=('Segoe UI', 12))
                elif len(col_names) == 2:
                    search_entry1 = ttk.Entry(top, width=32, font=('Segoe UI', 12))
                    search_entry2 = ttk.Entry(top, width=32, font=('Segoe UI', 12))
                    search_entry3 = ttk.Entry(top, width=21, font=('Segoe UI', 12))
                elif len(col_names) == 1:
                    search_entry1 = ttk.Entry(top, width=64, font=('Segoe UI', 12))
                    search_entry2 = ttk.Entry(top, width=21, font=('Segoe UI', 12))
                    search_entry3 = ttk.Entry(top, width=21, font=('Segoe UI', 12))

                vsc = ttk.Scrollbar(container, orient="vertical", command=search_tree.yview)
                search_tree.configure(yscrollcommand=vsc.set)
                search_entries = [search_entry1, search_entry2, search_entry3]
                #define binds
                for element in search_entries:
                    element.bind('<Escape>', clear_search)
                    element.bind('<KeyRelease>', dynamic_search)

                search_tree.bind('<Button-1>', handle_click)
                top.bind('<Escape>', exit_window)

                search_tree.bind('<Double-Button-1>', 
                lambda event, widget=widget, selection_mode=selection_mode:
                select_list(event, widget, selection_mode))

                search_tree.bind('<Return>', 
                lambda event, widget=widget, selection_mode=selection_mode:
                select_list_enter(event, widget, selection_mode))
                
                for col in col_names:
                    search_tree.heading(col, text=col, command=lambda c=col : sortby(search_tree, c, 0))
                    search_tree.column(col, width=193)
                    #search_tree.column(col, width=Font().measure(col.title()))
                create_treeview_content()
                s_container.pack(fill="x", expand=False)
                container.pack(fill='both', expand=True)
                if len(col_names) == 3:
                    search_entry1.grid(row=0, column=0, sticky=EW, in_=s_container)
                    search_entry2.grid(row=0, column=1, sticky=EW, in_=s_container)
                    search_entry3.grid(row=0, column=2, sticky=EW, in_=s_container)
                elif len(col_names) == 2:
                    search_entry1.grid(row=0, column=0, sticky=EW, in_=s_container)
                    search_entry2.grid(row=0, column=1, sticky=EW, in_=s_container)
                elif len(col_names) == 1:
                    search_entry1.grid(row=0, column=0, sticky=EW, in_=s_container)

                search_entry1.focus_force()
                search_tree.grid(row=0, column=0, columnspan=3, rowspan=300, sticky=NSEW)
                vsc.grid(row=0, column=3, rowspan=300, sticky=NS)
                container.grid_columnconfigure(0, weight=1)
                container.grid_rowconfigure(0, weight=1)
                ok_button = ttk.Button(top, text="OK", command= lambda: select_list_button(selection_mode))
                ok_button.pack(side="left", padx=40, pady=5)
                cancel_button = ttk.Button(top, text="Cancel", command=top.destroy)
                cancel_button.pack(side="right", padx=40, pady=5)
            
            def sortby(tree, col, descending):
                #sort when header clicked
                #get column values
                data = [(tree.set(child, col), child) \
                    for child in tree.get_children('')]
                data.sort(reverse=descending)
                #sort
                for ix, item in enumerate(data):
                    tree.move(item[1], '', ix)
                #switch direction
                tree.heading(col, command=lambda col=col: sortby(tree, col, int(not descending)))

            def handle_click(event):
                if search_tree.identify_region(event.x, event.y) == "separator":
                    return "break"


            def exit_window(event):
                if re.findall('entry', str(top.focus_get())) == []:
                    top.destroy()

            def dynamic_search(event):
                create_treeview_content()
                for i, col in enumerate(search_entries):
                    for item_id in search_tree.get_children():
                        text = str(search_tree.item(item_id)['values'][i])
                        if i == 0:
                            while len(text) < 7:
                                text = "0" + text                            
                        if re.findall(str(col.get()), text) == []:
                            search_tree.detach(item_id)

            def clear_search(event):
                if event.widget.get() == '':
                    top.destroy()
                else:
                    event.widget.delete(0, END)
                    create_treeview_content()

            def select_list(event, widget, selection_mode):
                if search_tree.identify_region(event.x, event.y) != "heading":
                    widget.delete(0, END)
                    row_id = search_tree.identify_row(event.y)
                    item_tuple = search_tree.item(row_id)['text'].split(";|;")
                    widget.insert(0, item_tuple[selection_mode])
                    top.destroy()

            def select_list_enter(event, widget, selection_mode):
                if search_tree.focus() != "":
                    widget.delete(0, END)
                    item_tuple = search_tree.item(search_tree.focus())['text'].split(";|;")
                    widget.insert(0, str(item_tuple[selection_mode]))
                    top.destroy()

            def select_list_button(selection_mode):
                if search_tree.focus() != "":
                    widget.delete(0, END)
                    item_tuple = search_tree.item(search_tree.focus())['text'].split(";|;")
                    widget.insert(0, str(item_tuple[selection_mode]))
                    top.destroy()

            def clear_none_values(tuple_list):
                final_list = []
                for tuple_ in tuple_list:
                    new_tuple = []
                    for item in tuple_:
                        if item == 'None':
                            new_item = ""
                        else:
                            new_item = str(item)
                        new_tuple.append(new_item)
                    final_list.append(new_tuple)
                return final_list

            ele_list = []
            top = Toplevel()
            #top.wm_overrideredirect(True) 
            top.geometry("600x800+300+100")
            top.minsize(width=600, height=800)
            top.maxsize(width=600, height=800)
            top.configure(background='#303030')
            top.grab_set()

            if mode == "":
                col_names = ["List ID", "Description 1", "Description 2"]
                ele_list1 = []
                ele_list2 = []
                ele_list3 = []
                for num in range(1, 100):
                    ele_list1.append(str(num))
                for num in range(101, 200):
                    ele_list2.append(str(num))
                for num in range(201, 300):
                    ele_list3.append(str(num))
                for ele1, ele2, ele3 in zip(ele_list1, ele_list2, ele_list3):
                    ele_list.append((ele1, ele2, ele3))
                create_search_elements(0, widget)

            elif mode == "list_r2":
                col_names = ["List ID", "Description 1", "Description 2"]
                ele_list = tdmsql.tdm_get_list_tuple_TDM_LIST(cnxn)
                create_search_elements(0, widget)

            elif mode == "part_r2":
                col_names = ["List ID", "Description 1", "Description 2"]
                ele_list = tdmsql.tdm_get_list_tuple_TDM_LIST(cnxn)
                create_search_elements(1, widget)

            elif mode == "desc_r2":
                col_names = ["List ID", "Description 1", "Description 2"]
                ele_list = tdmsql.tdm_get_list_tuple_TDM_LIST(cnxn)
                create_search_elements(2, widget)

            elif mode == "material_r2_Used":
                col_names = ["Material ID", "Material Name"]
                ele_list = tdmsql.tdm_get_list_tuple_material_used(cnxn)
                create_search_elements(0, widget)

            elif mode == "material_r2_All":
                col_names = ["Material ID", "Material Name"]
                ele_list = tdmsql.tdm_get_list_tuple_TDM_MATERIAL(cnxn)
                create_search_elements(0, widget)

            elif mode == "machine_r2_Used":
                col_names = ["Machine ID", "Machine Name"]
                ele_list = tdmsql.tdm_get_list_tuple_TDM_MACHINE(cnxn)
                create_search_elements(0, widget)
            
            elif mode == "fixture_r2_Used":
                col_names = ["Fixture"]
                ele_list = tdmsql.tdm_get_list_tuple_fixture_used(cnxn)
                create_search_elements(0, widget)
            
            '''elif mode == "fixture_r2_All":
                col_names = ["List ID", "Description 1", "Description 2"]
                ele_list = tdmsql.tdm_get_list_tuple_TDM_FIXTURE(cnxn)
                create_search_elements(0, widget)'''

            tdmsql.tdmDisconnect(cnxn)

        
        def make_prompt():
            response = messagebox.askokcancel("Potwierdź wykonanie listy", "Jeżeli jesteś pewien co do wprowadzonych danych nie wahaj się potwierdzić stworzenia listy.\nJeśli nie jesteś przekonany lepiej sprawdź co wpisałeś.")
            if response == 1:
                make_list()
                try:
                    tdmsql.tdmDisconnect(cnxn)
                except NameError:
                    pass
            else:
                return None    
                    
            

        #replace old frame
        for child in oldframe.winfo_children():
            child.destroy()
        
        label_title = Label(mainframe, text="Tool List maker v2.0.1")
        intro = Label(mainframe, text="Witaj w pierwszym module paczek małych pomocników do pracy z programem TDM!\nW poniższym formularzu wybierz dane które chcesz, żeby były dodane do nowej listy narzędziowej", fg='white', bg='#303030')
        #sections
        top_frame = Frame(mainframe, bg='#404040', borderwidth=0, highlightthickness=0)
        bottom_frame = Frame(mainframe, bg='#404040', borderwidth=0, highlightthickness=0)
        left_frame = Frame(top_frame, bg='#404040', borderwidth=0, highlightthickness=0)
        right_frame = Frame(top_frame, bg='#404040', borderwidth=0, highlightthickness=0)
        #tool get mode
        tool_mode_frame = LabelFrame(text="Wybierz tryb zbierania narzędzi")
        tool_mode_r1 = Radiobutton(tool_mode_frame, text="CTX / DMC / DMF (NX)", variable=tool_mode_sel, value=0, command=radio_switch)
        tool_mode_r2 = Radiobutton(tool_mode_frame, text="DATRON", variable=tool_mode_sel, value=1, command=radio_switch)
        tool_mode_r3 = Radiobutton(tool_mode_frame, text="CTX (SHOPTURN)", variable=tool_mode_sel, value=2, command=radio_switch)

        #source file
        source_frame = LabelFrame(text="Wybierz plik(i) *.mpf/*.spf")
        source_label = Label(source_frame, text="UWAGA! Z wszystkich wybranych plików zostanie stworzona jedna lista!")
        source_entry = Entry(source_frame)
        source_entry.configure(state=DISABLED)
        source_butt = Button(source_frame, text="Przeglądaj...", command=select_mpf_file)

        #list id
        list_frame = LabelFrame(text="Wybierz Tool List ID:")
        list_r1 = Radiobutton(list_frame, text="Najwyższe wolne (stworzenie nowej listy)", variable=list_id_sel, value=0, command=radio_switch)
        list_r2 = Radiobutton(list_frame, text="Podaj ręcznie (nadpisanie istniejącej listy):", variable=list_id_sel, value=1, command=radio_switch)
        entry_list_r2 = Entry(list_frame)
        entry_list_r2.configure(state=DISABLED)
        list_r2_butt = Button(list_frame, text="▼", padx=3, command=lambda: search("list_r2", entry_list_r2))

        #part name
        part_frame = LabelFrame(text="Wybierz Nazwę programu (Tool List Desc. 1):")
        part_r1 = Radiobutton(part_frame, text="Automatycznie z nazwy pliku", variable=part_sel, value=0, command=radio_switch)
        part_r2 = Radiobutton(part_frame, text="Podaj ręcznie:", variable=part_sel, value=1, command=radio_switch)
        entry_part_r2 = Entry(part_frame)
        entry_part_r2.configure(state=DISABLED)
        part_r3 = Radiobutton(part_frame, text="Pozostaw bez zmian", variable=part_sel, value=2, command=radio_switch)
        part_r2_butt = Button(part_frame, text="▼", padx=3, command=lambda: search("part_r2", entry_part_r2))

        #desc
        desc_frame = LabelFrame(text="Opis programu (Tool List Desc. 2)")
        desc_r1 = Radiobutton(desc_frame, text="Nie chcę dodawać opisu", variable=desc_sel, value=0, command=radio_switch)
        desc_r2 = Radiobutton(desc_frame, text="Wprowadź opis:", variable=desc_sel, value=1, command=radio_switch)
        entry_desc_r2 = Entry(desc_frame)
        entry_desc_r2.configure(state=DISABLED)
        desc_r3 = Radiobutton(desc_frame, text="Pozostaw bez zmian", variable=desc_sel, value=2, command=radio_switch)
        desc_r2_butt = Button(desc_frame, text="▼", padx=3, command=lambda: search("desc_r2", entry_desc_r2))

        #material
        material_frame = LabelFrame(text="Wybierz materiał:")
        material_r1 = Radiobutton(material_frame, text="Nie chcę dodawać materiału", variable=material_sel, value=0, command=radio_switch)
        material_r2 = Radiobutton(material_frame, text="Wybierz z listy:", variable=material_sel, value=1, command=radio_switch)
        entry_material_r2 = Entry(material_frame)
        entry_material_r2.configure(state=DISABLED)
        material_r3 = Radiobutton(material_frame, text="Pozostaw bez zmian", variable=material_sel, value=2, command=radio_switch)
        material_r2_butt_Used = Button(material_frame, text="▼", padx=3, command=lambda: search("material_r2_Used", entry_material_r2))
        material_r2_butt_All = Button(material_frame, text="⧪", padx=3, command=lambda: search("material_r2_All", entry_material_r2))

        #machine
        machine_frame = LabelFrame(text="Wybierz maszynę:")
        machine_r1 = Radiobutton(machine_frame, text="Nie chcę dodawać maszyny", variable=machine_sel, value=0, command=radio_switch)
        machine_r2 = Radiobutton(machine_frame, text="Wybierz z listy:", variable=machine_sel, value=1, command=radio_switch)
        entry_machine_r2 = Entry(machine_frame)
        entry_machine_r2.configure(state=DISABLED)
        machine_r3 = Radiobutton(machine_frame, text="Pozostaw bez zmian", variable=machine_sel, value=2, command=radio_switch)
        machine_r2_butt_All = Button(machine_frame, text="▼", padx=3, command=lambda: search("machine_r2_Used", entry_machine_r2))

        #fixture
        fixture_frame = LabelFrame(text="Wybierz mocowanie:")
        fixture_r1 = Radiobutton(fixture_frame, text="Nie chcę dodawać mocowania", variable=fixture_sel, value=0, command=radio_switch)
        fixture_r2 = Radiobutton(fixture_frame, text="Wprowadź mocowanie:", variable=fixture_sel, value=1, command=radio_switch)
        entry_fixture_r2 = Entry(fixture_frame)
        entry_fixture_r2.configure(state=DISABLED)
        fixture_r3 = Radiobutton(fixture_frame, text="Pozostaw bez zmian", variable=fixture_sel, value=2, command=radio_switch)
        fixture_r2_butt_Used = Button(fixture_frame, text="▼", padx=3, command=lambda: search("fixture_r2_Used", entry_fixture_r2))
        #fixture_r2_butt_All = Button(fixture_frame, text="⧪", padx=3, command=lambda: search("fixture_r2_All", entry_fixture_r2))

        #listtype
        list_type_frame = LabelFrame(text="Wybierz typ listy narzędziowej:")
        list_type_r1 = Radiobutton(list_type_frame, text="Primary", variable=list_type_sel, value=0)
        list_type_r2 = Radiobutton(list_type_frame, text="Secondary", variable=list_type_sel, value=1)
        list_label = Label(list_type_frame)
        list_type_r3 = Radiobutton(list_type_frame, text="Pozostaw bez zmian", variable=list_type_sel, value=2, command=radio_switch)

        #username locked
        username = getpass.getuser()
        username_frame = LabelFrame(text="Nazwa użytkownika")
        username_label = Label(username_frame, text="Nazwy użytkownika nie można zmienić :)")
        entry_username = Entry(username_frame)
        entry_username.insert(0, username.upper())
        entry_username.configure(state=DISABLED)

        #operations
        operations_frame = LabelFrame(text="Działania")
        operations_label = Label(operations_frame, text="Do poprawnego funkcjonowania programu potrzebne jest połączenie z TDM")
        #operations_butt_connect = Button(operations_frame, text="Połącz z bazą TDM", command=lambda: start_TDM_connect_thread(None))
        operations_butt_make = Button(operations_frame, text="Stwórz Listę", command=make_prompt)

        #output
        output_frame = LabelFrame()
        output_label = Label(output_frame, text="Czekam na rozkazy")

        #styles
        radio_switches_3 = [part_r3, desc_r3, material_r3, machine_r3, fixture_r3, list_type_r3]
        radio_variables_3 = [part_sel, desc_sel, material_sel, machine_sel, fixture_sel, list_type_sel]

        tlm_title = [label_title]
        tlm_labels = [intro, username_label, operations_label, output_label, list_label, source_label]
        tlm_frames = [tool_mode_frame, source_frame, list_frame, part_frame, desc_frame, material_frame, machine_frame, fixture_frame, list_type_frame, username_frame, operations_frame, output_frame]
        tlm_radios = [tool_mode_r1, tool_mode_r2, tool_mode_r3, list_r1, list_r2, part_r1, part_r2, part_r3, material_r1, material_r2, material_r3, machine_r1, machine_r2, machine_r3, fixture_r1, fixture_r2, fixture_r3, list_type_r1, list_type_r2, list_type_r3, desc_r1, desc_r2, desc_r3]
        tlm_buttons = [source_butt, operations_butt_make]
        tlm_optionmenus = []
        tlm_entries = [source_entry, entry_list_r2, entry_part_r2, entry_desc_r2, entry_username, entry_material_r2, entry_machine_r2, entry_fixture_r2]
        tlm_list_butts = [part_r2_butt, desc_r2_butt, machine_r2_butt_All, material_r2_butt_All, material_r2_butt_Used, fixture_r2_butt_Used, list_r2_butt]

        tlm_components = [tlm_title, tlm_labels, tlm_frames, tlm_radios, tlm_buttons, tlm_optionmenus, tlm_entries, tlm_list_butts]


        #apply styles
        for group in tlm_components:
            for element in group:
                if group is tlm_title:
                    element.configure(fg='white', bg='#525252', font=('Segoe UI', 26))
                if group is tlm_labels:
                    element.configure(fg='white', bg='#404040', font=('Segoe UI', 10))
                if group is tlm_frames:
                    element.configure(fg='white', bg='#404040', borderwidth=1, highlightthickness=0, font=('Segoe UI', 10))
                if group is tlm_radios:
                    element.configure(fg='white', bg='#404040', activebackground='#404040', activeforeground='white', selectcolor='black', font=('Segoe UI', 10))
                if group is tlm_buttons:
                    element.configure(fg='white', bg='#464646', activeforeground='white', activebackground='#555555', font=('Segoe UI', 10))
                if group is tlm_optionmenus:
                    element.configure(width=25, foreground='black', background='#aaaaaa', activeforeground='black', activebackground='#aaaaaa', borderwidth=0, highlightthickness=0, font=('Segoe UI', 10))
                if group is tlm_entries:
                    element.configure(width=20, disabledforeground='black', disabledbackground='#aaaaaa', font=('Segoe UI', 10), borderwidth=2)
                if group is tlm_list_butts:
                    element.configure(fg='white', bg='#303030', activeforeground='white', activebackground='#555555')

        #modify styles apllied by loop
        source_label.configure(fg='#BB0000', font=('Segoe UI Semibold', 12), wraplength=330, justify='left')
        source_label.grid_configure(columnspan=2)
        source_entry.configure(width=40)
        operations_butt_make.configure(bg='#00c70a', activebackground='#00f20c', font=['Segoe UI Semibold', 20])
        output_label.configure(anchor=E)

        def enable_search_buttons():
            for ele in tlm_list_butts:
                ele.configure(state=NORMAL)

        def disable_search_buttons():
            for ele in tlm_list_butts:
                ele.configure(state=DISABLED)

        def disable_radios_buttons():
            for ele in tlm_radios:
                ele.configure(state=DISABLED)
            '''for ele in tlm_buttons:
                ele.configure(state=DISABLED)'''
            source_butt.configure(state=DISABLED)
        
        def enable_radios_buttons():
            for ele in tlm_radios:
                ele.configure(state=NORMAL)
            '''for ele in tlm_buttons:
                if ele != operations_butt_make:
                    ele.configure(state=NORMAL)'''
            source_butt.configure(state=NORMAL)

        #put elements on the screen
        #label_title.grid(row=0, column=1, ipadx=60)
        label_title.pack(fill='x', anchor=N, ipady=10)
        #mainframe.grid(row=1, column=1, rowspan=5000, sticky=N+E+W+S, padx=5, pady=(0, 5))
        #intro.grid(row=0, column=0, columnspan=6, pady=10)
        intro.pack(fill='x', expand=False, anchor=N)
        top_frame.pack(fill='both', expand=True, side='top')
        left_frame.pack(fill='both', expand=True, side='left')
        right_frame.pack(fill='both', expand=True, side='left')
        bottom_frame.pack(fill='both', expand=True, side='bottom')
        
        #tool_mode_frame.grid(row=1, column=0, pady=10, padx=10, ipady=3, ipadx=3, sticky=W+E)
        #tool_mode_frame.pack(fill='x', expand=True, anchor=NW, side='left')
        #tool_mode_r1.grid(row=0, column=0, padx=5, sticky=W)
        
        #tool_mode_r2.grid(row=1, column=0, padx=5, sticky=W)
        

        #source_frame.grid(row=1, column=1, columnspan=2, pady=10)
        #source_frame.pack(fill='x', expand=True, anchor=NW, side='right')
        #source_label.grid(row=0, column=0, columnspan=2, padx=10, pady=(10, 0))
        #source_entry.grid(row=1, column=0, padx= 10)
        #source_butt.grid(row=1, column=1, padx= 10, pady=10)

        tool_mode_elems = [tool_mode_frame, tool_mode_r1, tool_mode_r2, tool_mode_r3]
        source_elems = [source_frame, source_label, source_entry, source_butt]
        list_elems = [list_frame, list_r1, list_r2, entry_list_r2]
        part_elems = [part_frame, part_r1, part_r2, entry_part_r2, part_r3]
        desc_elems = [desc_frame, desc_r1, desc_r2, entry_desc_r2, desc_r3]
        material_elems = [material_frame, material_r1, material_r2, entry_material_r2, material_r3]
        machine_elems = [machine_frame, machine_r1, machine_r2, entry_machine_r2, machine_r3]
        fixture_elems = [fixture_frame, fixture_r1, fixture_r2, entry_fixture_r2, fixture_r3]
        list_type_elems = [list_type_frame, list_type_r1, list_type_r2, list_type_r3]
        username_elems = [username_frame, username_label, entry_username]
        operations_elems = [operations_frame, operations_label, operations_butt_make]

        tlm_sections = [tool_mode_elems, source_elems, list_elems, part_elems, desc_elems, material_elems, machine_elems, fixture_elems, list_type_elems, username_elems]
        
        j = 0
        for section in tlm_sections:
            i_row = 0
            i_column = 0
            
            for i, widget in enumerate(section):
                if i == 0:
                    if j % 2 == 0:
                        widget.pack(fill='both', expand=True, anchor=N, in_=left_frame, padx=10, pady=1)
                    else:
                        widget.pack(fill='both', expand=True, anchor=N, in_=right_frame, padx=10, pady=1)
                    j += 1
                elif i > 0:
                    '''if i_row == i_column:
                        widget.grid(row=i_row, column=i_column, padx=5, sticky=W)
                        i_row += 1
                    elif i_row > i_column:
                        widget.grid(row=i_row, column=i_column, padx=5, sticky=W)
                        i_column += 1
                    if i_row >= 2:
                        i_column = 0'''
                    if i != 3:
                        widget.grid(row=i_row, column=i_column, padx=5, sticky=W, columnspan=90)
                        i_row += 1
                    else:
                        widget.grid(row=i_row, column=i_column, padx=5, pady=(0,5), sticky=W)
                        i_row += 1
        operations_frame.pack(fill='x', expand=True, anchor=S, in_=bottom_frame, ipadx=5, ipady=5, padx=10, pady=10)
        for index, widget in enumerate(operations_elems):
            if index == 1:
                widget.grid_forget()
            elif index > 1:
                widget.grid_forget()
        operations_label.pack(fill='x')
        operations_butt_make.pack(side='right', padx=(15, 50), pady=5, anchor=NW)
        for i, widget in enumerate(source_elems):
            if i == 1:
                widget.grid_forget()
                widget.grid(row=0, column=0, columnspan=2)
            if i == 2:
                widget.grid_forget()
                widget.grid(row=1, column=0, columnspan=2, sticky=W)
            if i == 3:
                widget.grid_forget()
                widget.grid(row=2, column=0, sticky=W)
            if i > 0:
                widget.grid_configure(padx=5, pady=5)
        '''source_butt.grid_forget()
        source_butt.grid(row=2, column=40, sticky=E, pady=5, padx=5)'''

        output_frame.pack(fill='x', expand=False, anchor=E, in_=bottom_frame)
        output_label.grid(row=0, column=0, columnspan=3, sticky=E)
        list_r2_butt.grid(row=2, column=1, sticky=W, pady=(0,5))
        part_r2_butt.grid(row=2, column=1, sticky=W, pady=(0,5))
        desc_r2_butt.grid(row=2, column=1, sticky=W, pady=(0,5))
        material_r2_butt_Used.grid(row=2, column=1, sticky=W, pady=(0,5))
        material_r2_butt_All.grid(row=2, column=2, sticky=W, pady=(0,5))
        machine_r2_butt_All.grid(row=2, column=2, sticky=W, pady=(0,5))
        fixture_r2_butt_Used.grid(row=2, column=1, sticky=W, pady=(0,5))
        #fixture_r2_butt_All.grid(row=1, column=3)

        def update_source_label_wrap(event):
            source_frame.update_idletasks()
            source_label.configure(wraplength=(source_frame.winfo_width()-20))

        '''
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
        list_r2_butt.grid(row=1, column=2)
        part_r2_butt.grid(row=1, column=2)
        desc_r2_butt.grid(row=1, column=2)
        material_r2_butt_Used.grid(row=1, column=2)
        material_r2_butt_All.grid(row=1, column=3)
        machine_r2_butt_All.grid(row=1, column=3)
        fixture_r2_butt_Used.grid(row=1, column=2)
        fixture_r2_butt_All.grid(row=1, column=3)'''
        

        for radio in radio_switches_3:
            radio.configure(state=DISABLED)
        disable_search_buttons()

        def set_radio_variables_to_2(event):
            for var in radio_variables_3:
                if var.get() == 0:
                    var.set(2)

        def set_none(event):
                if entry_machine_r2.get() == "MMLCUBEB" or entry_machine_r2.get() == "MCTX125A":
                    entry_machine_r2.configure(state=NORMAL)
                    entry_machine_r2.delete(0, END)
                    entry_machine_r2.configure(state=DISABLED)
                    machine_sel.set(0)

        
        def set_mmlcubeb(event):
            if entry_machine_r2.get() == "" or entry_machine_r2.get() == "MCTX125A":
                entry_machine_r2.configure(state=NORMAL)
                entry_machine_r2.delete(0, END)
                entry_machine_r2.insert(0, "MMLCUBEB")
                machine_sel.set(1)

        def set_mctx125a(event):
                if entry_machine_r2.get() == "MMLCUBEB" or entry_machine_r2.get() == "":
                    entry_machine_r2.configure(state=NORMAL)
                    entry_machine_r2.delete(0, END)
                    entry_machine_r2.insert(0, "MCTX125A")
                    machine_sel.set(1)


        #binds
        list_r2.bind('<Button-1>', set_radio_variables_to_2)
        tool_mode_r1.bind('<Button-1>', set_none)
        tool_mode_r2.bind('<Button-1>', set_mmlcubeb)
        tool_mode_r3.bind('<Button-1>', set_mctx125a)
        source_frame.bind('<Configure>', update_source_label_wrap)

        
        def make_list():
            global server_available
            #form validation
            error_message = ""
            error_count = 1
            for entry in tlm_entries:
                if entry.cget('state') == NORMAL and entry.get() == "":
                    error_message += "%d. Zaznaczono pola do wprowadzenia danych, ale pozostawiono je puste\n" % error_count
                    error_count += 1
                    break
            if mpf_files == None:
                error_message += "%d. Nie wybrano pliku źródłowego\n" % error_count
                error_count += 1
            '''if list_id_sel == 1:
                if len(entry_list_r2.get()) < 7 or re.findall(r'[^0-9]' ,entry_list_r2.get()) != []:
                    error_message += "Wprowadzono numer listy narzędziowej w złym formacie"'''
            if len(error_message) > 0:
                messagebox.showerror("Błędy w formluarzu", "W formularzu znajdują się poniższe błędy:\n%s" % error_message)
                return
            if not server_available:
                if os.system("ping -n 1  172.26.48.03") == 1:
                    messagebox.showerror("Brak połączenia", "Brak połączenia z serwerem bazy TDM")
                    return
                else:
                    server_available = True
            connection_valid = TDM_connect()
            if not connection_valid:
                messagebox.showerror("Błąd połączenia", "Program nie mógł nazwiązać połączenia z bazą danych z niejasnych przyczyn.")
                return None
            error_message = ""
            error_count = 1
            if not tdmsql.validate_list_ID(cnxn, entry_list_r2.get()):
                error_message += "%d. Nie znaleziono numeru listy wskazanej do zaktualizowania w TDM.\n" % error_count
                error_count += 1
            if not tdmsql.validate_machine(cnxn, entry_machine_r2.get()):
                error_message += "%d. Nie znaleziono maszyny wskazanej do dodania w TDM.\n" % error_count
                error_count += 1
            if not tdmsql.validate_material(cnxn, entry_material_r2.get()):
                error_message += "%d. Nie znaleziono materiału wskazanego do dodania w TDM.\n" % error_count
                error_count += 1
            #tool get mode
            tlist = []
            if tool_mode_sel.get() == 0: #mpf
                try:
                    for file in mpf_files:
                        for tool in toolgetmod.get_tools_from_mpf_file(file):
                            tlist.append(tool)
                except:
                    messagebox.showerror("Błąd", "Zły plik źródłowy!")
                    return None
                if len(tlist) > 0:
                    print(tlist)
                    tlist = list(set(tlist))
                else:
                    messagebox.showerror("Błąd", "Brak narzędzi w pliku źródłowym!")
                    return None
            elif tool_mode_sel.get() == 1: #datron
                fusion_dict = {}
                dict_file = open("fusion_dict.txt")
                for line in dict_file:
                    key, value = line.split(": ")
                    val = ""
                    for char in value:
                        if char != "\n":
                            val = val + char
                        else:
                            break
                    fusion_dict[key] = val
                try:
                    for file in mpf_files:
                        elements = toolgetmod.fileTlistFUSION(file)
                        for tool in elements:
                            ele = toolgetmod.clearFUSION(tool)
                            tlist.append(ele)
                except TabError:
                    messagebox.showerror("Błąd", "Zły plik źródłowy!")
                    return None
                clist = list(set(tlist))
                tlist = []
                for ele in clist:
                    try:
                        ele = fusion_dict[ele]
                        tlist.append(ele)
                    except KeyError:
                        tlist.append(ele)
            elif tool_mode_sel.get() == 2:
                for file in mpf_files:
                    for tool in toolgetmod.get_tools_from_mpf_file_shopturn(file):
                        tlist.append(tool)
                '''except:
                    messagebox.showerror("Błąd", "Zły plik źródłowy!")
                    return None'''
                if len(tlist) > 0:
                    print(tlist)
                    tlist = list(set(tlist))
                else:
                    messagebox.showerror("Błąd", "Brak narzędzi w pliku źródłowym!")
                    return None

            if list_id_sel.get() == 0: #new list
                listID = tdmsql.tdmGetMaxListID(cnxn)
            elif list_id_sel.get() == 1: #update list
                listID = entry_list_r2.get()

            if part_sel.get() == 0:
                NCprogram = ""
                for char in os.path.basename(mpf_files[0]):
                    if char != '.':
                        NCprogram += char
                    else:
                        break
            elif part_sel.get() == 1:
                NCprogram = entry_part_r2.get()
            elif part_sel.get() == 2:
                NCprogram = False

            if desc_sel.get() == 0:
                desc = "null"
            elif desc_sel.get() == 1:
                desc = entry_desc_r2.get()
            elif desc_sel.get() == 2:
                desc = False

            if material_sel.get() == 0:
                material = "null"
            elif material_sel.get() == 1:
                material = entry_material_r2.get()
            elif material_sel.get() == 2:
                material = False

            if machine_sel.get() == 0:
                machine = "null"
            elif machine_sel.get() == 1:
                machine = entry_machine_r2.get()
            elif machine_sel.get() == 2:
                machine = False

            if fixture_sel.get() == 0:
                fixture = "null"
            elif fixture_sel.get() == 1:
                fixture = entry_fixture_r2.get()
            elif fixture_sel.get() == 2:
                fixture = False

            if list_type_sel.get() == 0:
                list_type = 1
            elif list_type_sel.get() == 1:
                list_type = 2
            elif list_type_sel.get() == 2:
                list_type = False

            if machine != "null":
                if machine != False:
                    machine_group = tdmsql.tdm_get_MACHINEGROUPID_by_MACHINEID(cnxn, machine)
                else:
                    machine_group = False
            else:
                machine_group = machine

            pos = 1
            
            date_dict = dict()
            for epoch, tdm in zip(range(1543100400, 1975096800, 86400), range(153000, 158000)):
                date_dict[epoch] = tdm
            user = getpass.getuser()
            user = user.upper()
            timestamp = round(time.time())
            changetime = timestamp % 86400
            try:
                changedate = date_dict[timestamp - changetime - 7200]
            except KeyError:
                changedate = date_dict[timestamp - changetime - 3600]
            username = tdmsql.tdmGetUserName(cnxn, user)
            changetime = changetime + 7200
            if list_id_sel.get() == 0: #nowa lista
                if tool_mode_sel.get() == 0 or tool_mode_sel.get() == 2: #mpf
                    invalid_tools = tdmsql.tdm_list_missing_tools(cnxn, tlist)
                    if len(invalid_tools) == 0:
                        tdmsql.tdmCreateListTLM2(cnxn, timestamp, listID, NCprogram, desc, material, machine, machine_group, fixture, list_type, username)
                        tdmsql.tdmAddTools(cnxn, listID, tlist, timestamp)
                        tdmsql.tdmAddLogfile(cnxn, listID, user, timestamp, pos, changedate, changetime)
                        messagebox.showinfo("Powodzenie", "Dodano listę narzędziową do TDM!")
                        return None
                    elif len(invalid_tools) != 0:
                        bad_list_string = str()
                        for tool in invalid_tools:
                            bad_list_string = bad_list_string + str(tool) + "\n"
                        response = messagebox.askokcancel("Lista zawiera błędne narzędzia", "W liście występują poniższe błędne narzędzia:\n%s\nCzy chcesz stworzyć listę bez tych narzędzi?" % bad_list_string)
                        if response == 1:
                            for tool in invalid_tools:
                                tlist.remove(tool)
                            tdmsql.tdmCreateListTLM2(cnxn, timestamp, listID, NCprogram, desc, material, machine, machine_group, fixture, list_type, username)
                            tdmsql.tdmAddTools(cnxn, listID, tlist, timestamp)
                            tdmsql.tdmAddLogfile(cnxn, listID, user, timestamp, pos, changedate, changetime)
                            messagebox.showinfo("Powodzenie", "Dodano listę bez następujących narzędzi:\n%s" % bad_list_string)
                            return None
                        else:
                            return None

                elif tool_mode_sel.get() == 1: #simple
                    invalid_tools = tdmsql.tdm_list_missing_comps(cnxn, tlist)
                    if len(invalid_tools) == 0:
                        tlist = tdmsql.tdmGetCompsID(cnxn, tlist)
                        tdmsql.tdmCreateListTLM2(cnxn, timestamp, listID, NCprogram, desc, material, machine, machine_group, fixture, list_type, username)
                        tdmsql.tdmAddComps(cnxn, listID, tlist, timestamp)
                        tdmsql.tdmAddLogfile(cnxn, listID, user, timestamp, pos, changedate, changetime)
                        messagebox.showinfo("Powodzenie", "Dodano listę narzędziową do TDM!")
                        return None
                    elif invalid_tools != 0:
                        bad_list_string = str()
                        for tool in invalid_tools:
                            bad_list_string = bad_list_string + str(tool) + "\n"
                        response = messagebox.askokcancel("Lista zawiera błędne narzędzia", "W liście występują poniższe błędne narzędzia:\n%s\nCzy chcesz stworzyć listę bez tych narzędzi?" % bad_list_string)
                        if response == 1:
                            for tool in invalid_tools:
                                tlist.remove(tool)
                            tlist = tdmsql.tdmGetCompsID(cnxn, tlist)
                            tdmsql.tdmCreateListTLM2(cnxn, timestamp, listID, NCprogram, desc, material, machine, machine_group, fixture, list_type, username)
                            tdmsql.tdmAddComps(cnxn, listID, tlist, timestamp)
                            tdmsql.tdmAddLogfile(cnxn, listID, user, timestamp, pos, changedate, changetime)
                            messagebox.showinfo("Powodzenie", "Dodano listę bez następujących narzędzi:\n%s" % bad_list_string)
                            return None
                        else:
                            return None
            elif list_id_sel.get() == 1: #update
                if tool_mode_sel.get() == 0 or tool_mode_sel.get() == 2: #mpf
                    invalid_tools = tdmsql.tdm_list_missing_tools(cnxn, tlist)
                    if len(invalid_tools) == 0:
                        tdmsql.tdm_update_list(cnxn, timestamp, listID, NCprogram, desc, material, machine, machine_group, fixture, list_type, username)
                        tdmsql.tdm_delete_list_positions(cnxn, listID)
                        tdmsql.tdmAddTools(cnxn, listID, tlist, timestamp)
                        pos = tdmsql.get_next_pos_for_logfile(cnxn, listID)
                        tdmsql.tdmAddLogfile(cnxn, listID, user, timestamp, pos, changedate, changetime)
                        messagebox.showinfo("Powodzenie", "Dodano listę narzędziową do TDM!")
                        return None
                    elif len(invalid_tools) != 0:
                        bad_list_string = str()
                        for tool in invalid_tools:
                            bad_list_string = bad_list_string + str(tool) + "\n"
                        response = messagebox.askokcancel("Lista zawiera błędne narzędzia", "W liście występują poniższe błędne narzędzia:\n%s\nCzy chcesz stworzyć listę bez tych narzędzi?" % bad_list_string)
                        if response == 1:
                            for tool in invalid_tools:
                                tlist.remove(tool)
                            tdmsql.tdm_update_list(cnxn, timestamp, listID, NCprogram, desc, material, machine, machine_group, fixture, list_type, username)
                            tdmsql.tdm_delete_list_positions(cnxn, listID)
                            tdmsql.tdmAddTools(cnxn, listID, tlist, timestamp)
                            pos = tdmsql.get_next_pos_for_logfile(cnxn, listID)
                            tdmsql.tdmAddLogfile(cnxn, listID, user, timestamp, pos, changedate, changetime)
                            messagebox.showinfo("Powodzenie", "Dodano listę bez następujących narzędzi:\n%s" % bad_list_string)
                            return None
                        else:
                            return None
                elif tool_mode_sel.get() == 1: #simple
                    invalid_tools = tdmsql.tdm_list_missing_tools(cnxn, tlist)
                    if len(invalid_tools) == 0:
                        tlist = tdmsql.tdmGetCompsID(cnxn, tlist)
                        tdmsql.tdm_update_list(cnxn, timestamp, listID, NCprogram, desc, material, machine, machine_group, fixture, list_type, username)
                        tdmsql.tdm_delete_list_positions(cnxn, listID)
                        tdmsql.tdmAddComps(cnxn, listID, tlist, timestamp)
                        pos = tdmsql.get_next_pos_for_logfile(cnxn, listID)
                        tdmsql.tdmAddLogfile(cnxn, listID, user, timestamp, pos, changedate, changetime)
                        messagebox.showinfo("Powodzenie", "Dodano listę narzędziową do TDM!")
                        return None
                    elif len(invalid_tools) != 0:
                        bad_list_string = str()
                        for tool in invalid_tools:
                            bad_list_string = bad_list_string + str(tool) + "\n"
                        response = messagebox.askokcancel("Lista zawiera błędne narzędzia", "W liście występują poniższe błędne narzędzia:\n%s\nCzy chcesz stworzyć listę bez tych narzędzi?" % bad_list_string)
                        if response == 1:
                            for tool in invalid_tools:
                                tlist.remove(tool)
                            tlist = tdmsql.tdmGetCompsID(cnxn, tlist)
                            tdmsql.tdm_update_list(cnxn, timestamp, listID, NCprogram, desc, material, machine, machine_group, fixture, list_type, username)
                            tdmsql.tdm_delete_list_positions(cnxn, listID)
                            tdmsql.tdmAddComps(cnxn, listID, tlist, timestamp)
                            pos = tdmsql.get_next_pos_for_logfile(cnxn, listID)
                            tdmsql.tdmAddLogfile(cnxn, listID, user, timestamp, pos, changedate, changetime)
                            messagebox.showinfo("Powodzenie", "Dodano listę bez następujących narzędzi:\n%s" % bad_list_string)
                            return None
                        else:
                            return None


