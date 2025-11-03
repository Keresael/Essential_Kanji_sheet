from tkinter import *
from tkinter import ttk
from pdf_builder import *

def main_gui(gui):
    gui.title("Essential Kanji sheet")

    mainframe = ttk.Frame(gui, padding=(3, 3, 12, 12))
    mainframe.grid(column=0, row=0, sticky=N)

    kanji_textbox_var = StringVar()
    kanji_textbox = ttk.Entry(mainframe, width=7, textvariable=kanji_textbox_var)
    kanji_textbox.grid(column=1, row=1, sticky=N)


    ttk.Label(mainframe, text="Kanji").grid(column=2, row=1, sticky=W)

    add_info_var = BooleanVar()
    add_info = ttk.Checkbutton(mainframe, text='Add info', variable=add_info_var)
    add_info.grid(column=1, row=3, sticky=N)


    def button_event_handler():
        kanji = kanji_textbox_var.get()
        status_info = add_info_var.get()
        if not kanji:
             ttk.Label(mainframe, text="Campo Kanji non valido").grid(column=2, row=3, sticky=W)
        pdf_builder(kanji)

    button = ttk.Button(mainframe, text='Genera PDF', command=button_event_handler)
    button.grid(column=2, row=4, sticky=S)








