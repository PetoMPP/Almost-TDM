from tkinter import messagebox
import tlm, dd, pyodbc

global active_mode

def state_0(oldframe):
    global active_mode
    for child in oldframe.winfo_children():
        child.destroy()
        oldframe.configure(bg='#525252')
    active_mode = "state_0"

def tlm_(oldframe, active_mode1, mainframe, root, label_tlm1, label_exit1, label_dd1):
    global active_mode
    available_drivers = pyodbc.drivers()
    if available_drivers.count("ODBC Driver 17 for SQL Server") == 0:
        messagebox.showerror("Błąd sterownika", "Program nie mógł znaleźć na komputerze sterownika \"ODBC Driver 17 for SQL Server\", \
który jest niezbędny do poprawnej pracy programu Tool List Maker")
        return
    active_mode = "tlm"
    tlm.tlm(oldframe, active_mode1, mainframe, root, label_tlm1, label_exit1, label_dd1)

def dd_(oldframe, active_mode1, mainframe, root):
    global active_mode
    active_mode = "dd"
    dd.dd(oldframe, active_mode1, mainframe, root)
