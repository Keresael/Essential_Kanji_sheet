from tkinter import *
from tkinter import ttk
#from pdf_builder import *

def main_gui(gui):
    gui.title("Essential Kanji sheet")

    mainframe = ttk.Frame(gui, padding=(3, 3, 12, 12))
    mainframe.grid(column=0, row=0, sticky=N)

    kanji_textbox = StringVar()
    kanji_textbox = ttk.Entry(mainframe, width=7, textvariable=kanji_textbox)
    kanji_textbox.grid(column=1, row=0, sticky=N)
    kanji_textbox.grid(column=1, row=1, sticky=N)
    ttk.Label(mainframe, text="Kanji").grid(column=2, row=1, sticky=W)

    add_info = StringVar()
    add_info = ttk.Checkbutton(mainframe, text='Add info',command=add_info, variable=add_info, onvalue='true', offvalue='false')
    add_info.grid(column=1, row=3, sticky=N)

    button = ttk.Button(mainframe, text='Genera PDF')
    button.grid(column=2, row=4, sticky=S)




