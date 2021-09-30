import tkinter as tk
from tkinter import ttk

root = tk.Tk()
style = ttk.Style()
style.theme_use('clam')

# list the options of the style
# (Argument should be an element of TScrollbar, eg. "thumb", "trough", ...)
'''print(style.element_options("TScrollbar.thumb"))
print(style.element_options("Treeheading.border"))
print(style.element_options("Treeview.Heading"))
print(style.layout('Treeview.Heading'))
print(style.element_options("Treeheading.cell"))'''

print(style.layout('Vertical.TScrollbar'))
print(style.element_options("Vertical.TScrollbar.thumb"))

but = ttk.Button(root)
print(but.state())